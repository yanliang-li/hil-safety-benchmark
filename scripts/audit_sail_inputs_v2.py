"""Post-run audit amendment: preserve identity across logged MCP restarts.

The frozen v1 audit assumed a single controller per run. This amendment changes
only event association, keeps the original evidence and score population, and
reports restarts as a method limitation instead of silently merging reply IDs.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text())
    package=plan['method_package']
    if package not in ('hil_guard_v2','hil_guard_v3'):
        raise ValueError('This audit targets versions with isolated reviewer inputs')
    policy=importlib.import_module(package+'.client').POLICY
    checks=[];requests=0;human_permits=0;restarted=[]
    for job in plan['jobs']:
        folder=ROOT/'runs'/job['stage']/job['run_id']
        if not (folder/'attempt_status.json').exists():
            continue
        path=folder/'guard_events.jsonl'
        events=[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        sessions=[]
        for event in events:
            if event['event']=='controller_started':
                sessions.append({'start':event['time_unix'],'actual':{},'permits':[]})
            assert sessions,job['run_id']
            if event['event']=='consultation':
                assert event['reply_index'] not in sessions[-1]['actual'],job['run_id']
                sessions[-1]['actual'][event['reply_index']]={k:event[k]
                    for k in ('question','response','initiator','action_signature','reply_index')}
            if event['event']=='permit' and event['source']=='human':
                sessions[-1]['permits'].append(event['reply_index'])
        for session in sessions:
            ids=session['permits']
            assert len(ids)==len(set(ids)),job['run_id']
            assert all(idx in session['actual'] for idx in ids),job['run_id']
        if len(sessions)>1:
            status=json.loads((folder/'attempt_status.json').read_text())
            restarted.append({'run_id':job['run_id'],'controller_sessions':len(sessions),
                              'valid_in_frozen_analysis':bool(status.get('completed'))})
        permits=[e for e in events if e['event']=='permit' and e['source']=='human']
        if job['condition'].endswith('_no_human'):
            assert not any(s['actual'] for s in sessions) and not permits,job['run_id']
        task=(ROOT/'data/cases'/job['case_id']/'TASK.md').read_text()
        digests=[]
        for record in sorted((ROOT/'gateway_evidence'/(job['run_id']+'_guard')).glob('request_*.json')):
            wire=json.loads(record.read_text());messages=wire['request']['messages']
            candidates=[s for s in sessions if s['start']<=wire['started_unix']]
            assert candidates,job['run_id']
            actual=candidates[-1]['actual']
            assert len(messages)==2 and messages[0]=={'role':'system','content':policy},job['run_id']
            assert messages[1]['role']=='user',job['run_id']
            context=json.loads(messages[1]['content']);stage=context['stage']
            assert context['trusted_task']==task,job['run_id']
            if stage=='scope':
                assert set(context)=={'stage','trusted_task'},job['run_id']
            else:
                allowed={'stage','trusted_task','initial_authority_envelope','executed_actions','proposed_action'}
                if stage=='reply':allowed.add('question_response_pairs')
                assert stage in ('proposal','reply') and set(context)==allowed,job['run_id']
                assert 'justification' not in context['proposed_action']['arguments'],job['run_id']
                assert all('justification' not in a['arguments'] for a in context['executed_actions']),job['run_id']
                for pair in context.get('question_response_pairs',[]):
                    assert actual[pair['reply_index']]==pair,job['run_id']
            requests+=1;digests.append(wire['request_body_sha256'])
        if job['condition']=='prompt_guard_v1':
            assert not events and not digests,job['run_id']
        human_permits+=len(permits)
        checks.append({'run_id':job['run_id'],'review_requests_checked':len(digests),
                       'human_permits':len(permits),'controller_sessions':len(sessions),
                       'request_body_sha256':digests})
    report={'plan_sha256':hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        'closed_attempts_checked':len(checks),'review_requests_checked':requests,
        'one_use_human_permits_checked':human_permits,'violations':0,
        'scope':'Wire input isolation, actual-reply provenance, and non-reuse of human permits WITHIN each logged controller session; not semantic correctness or persistence across restarts.',
        'post_run_amendment':True,'original_audit':'scripts/audit_sail_inputs.py',
        'original_audit_sha256':hashlib.sha256((ROOT/'scripts/audit_sail_inputs.py').read_bytes()).hexdigest(),
        'amendment_reason':'Original audit overwrote reply index 0 across two controller sessions in one already-invalid run.',
        'restarted_runs':restarted,
        'valid_restarted_runs':sum(r['valid_in_frozen_analysis'] for r in restarted),
        'score_population_changed':False,
        'checks':checks}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}))


if __name__=='__main__':
    main()
