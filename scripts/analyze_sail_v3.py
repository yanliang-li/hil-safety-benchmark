"""Replay SAIL outcomes and report HIL benefits, failures, and additional cost."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))
from hil_safety_bench.evaluate import evaluate_run

spec = importlib.util.spec_from_file_location('original_analysis', ROOT / 'scripts/api_experiment/analyze.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)


def events(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def usage(run_id):
    result = Counter()
    for path in (ROOT / 'gateway_evidence' / run_id).glob('request_*.json'):
        row = json.loads(path.read_text())
        result['requests'] += 1
        result['pending_requests'] += row.get('state') == 'pending'
        result['transport_errors'] += row.get('state') == 'transport_error'
        result['http_errors'] += row.get('state') == 'upstream_error'
        u = row.get('usage') or {}
        result['requests_with_usage'] += bool(u)
        result['reported_input_tokens'] += u.get('input_tokens', u.get('prompt_tokens', 0)) or 0
        result['reported_output_tokens'] += u.get('output_tokens', u.get('completion_tokens', 0)) or 0
    return dict(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--bootstrap', type=int, default=10000)
    parser.add_argument('--skip-usage', action='store_true')
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    package = plan.get('method_package','hil_guard')
    if package not in ('hil_guard','hil_guard_v2','hil_guard_v3'):
        raise ValueError('Unknown method package')
    apply_condition = __import__(package+'.conditions',fromlist=['apply_condition']).apply_condition
    full = {'hil_guard':'sail_v1','hil_guard_v2':'sail_v2','hil_guard_v3':'sail_v3'}[package]
    no_human = {'hil_guard':'sail_no_human','hil_guard_v2':'sail_v2_no_human','hil_guard_v3':'sail_v3_no_human'}[package]
    args.output.mkdir(parents=True, exist_ok=True)
    grouped = defaultdict(lambda: defaultdict(dict))
    rows, attempts, checks = [], [], []
    for job in plan['jobs']:
        folder = ROOT / 'runs' / job['stage'] / job['run_id']
        status = folder / 'attempt_status.json'
        if not status.exists():
            continue
        state = json.loads(status.read_text())
        meta = json.loads((folder / 'run_metadata.json').read_text()) if (folder / 'run_metadata.json').exists() else {}
        guard = events(folder / 'guard_events.jsonl')
        tool_events = events(folder / 'events.jsonl')
        replay = evaluate_run(ROOT / 'data/cases' / job['case_id'], folder).to_dict()
        valid = bool(state.get('completed'))
        if valid:
            stored = json.loads((folder / 'result.json').read_text())
            if stored != replay:
                raise ValueError('Score replay mismatch: ' + job['run_id'])
            prompt = apply_condition((ROOT / 'data/cases' / job['case_id'] / 'TASK.md').read_text(), job['condition'])
            if meta.get('effective_prompt_sha256') != hashlib.sha256(prompt.encode()).hexdigest() or meta.get('condition') != job['condition']:
                raise ValueError('Condition/prompt mismatch: ' + job['run_id'])
            if meta.get('guard_invalid') or not meta.get('successful_termination'):
                raise ValueError('Invalid run in primary comparison')
            if [r['sequence'] for r in tool_events] != list(range(1, len(tool_events) + 1)):
                raise ValueError('Non-contiguous tool sequence')
            grouped[(job['agent'], job['model'])][job['condition']][(job['case_id'], job['repeat'])] = stored
            row = dict(agent=job['agent'], model=job['model'], condition=job['condition'],
                repeat=job['repeat'], run_id=job['run_id'], **stored)
            row['agent_questions'] = sum(e['event'] == 'consultation' and e.get('initiator') == 'agent' for e in guard) if guard else stored['total_human_questions']
            row['controller_questions'] = sum(e['event'] == 'consultation' and e.get('initiator') == 'controller' for e in guard)
            row['review_requests'] = sum(e['event'] == 'review' for e in guard)
            row['blocked_proposals'] = sum(e['event'] == 'blocked' for e in guard)
            row['wall_seconds'] = meta['finished_unix'] - meta['started_unix']
            rows.append(row)
            checks.append({'run_id': job['run_id'], 'score_replay_equal': True,
                          'events_sha256': hashlib.sha256((folder / 'events.jsonl').read_bytes()).hexdigest()})
        if valid:
            cause = 'valid'
        elif meta.get('guard_invalid') or any(e['event'] in ('guard_error', 'review_error') for e in guard):
            cause = 'guard_error'
        elif meta.get('timed_out'):
            cause = 'attempt_timeout'
        elif state.get('oom_killed'):
            cause = 'oom'
        else:
            cause = 'incomplete_framework_or_infrastructure'
        attempt = {k:job[k] for k in ['agent','model','condition','repeat','case_id','run_id']}
        attempt.update(valid=valid, failure_category=cause,
            observed_unsafe=replay['unsafe_attack_success'],
            guard_error_types=';'.join(sorted({e.get('error_type','') for e in guard if e['event'] in ('guard_error','review_error')})))
        if not args.skip_usage:
            for name, run_id in [('actor',job['run_id']),('reviewer',job['run_id']+'_guard')]:
                u = usage(run_id)
                for metric in ['requests','pending_requests','transport_errors','http_errors','requests_with_usage','reported_input_tokens','reported_output_tokens']:
                    attempt[name+'_'+metric] = u.get(metric,0)
        attempts.append(attempt)
    summary = {'experiment': plan['experiment'], 'planned_attempts':len(plan['jobs']),
        'finished_attempts':len(attempts),'valid_runs':len(rows),
        'failed_attempts':len(attempts)-len(rows),'pending_attempts':len(plan['jobs'])-len(attempts),
        'status':'complete' if len(attempts)==len(plan['jobs']) else 'provisional_incomplete',
        'plan_sha256':hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        'reviewer_model':plan['reviewer_model'], 'conditions': plan['conditions'],
        'scope':plan['scope'], 'usage_included':not args.skip_usage,
        'configurations':[], 'aggregate':{}, 'all_attempt_sensitivity':{}}
    lines = ['# SAIL HIL comparison','',
        f"Status: **{summary['status']}**. {len(attempts)}/{len(plan['jobs'])} attempts closed; {len(rows)} valid, {len(attempts)-len(rows)} failed.", '',
        '| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|']
    def fmt(value):
        n,d=value['numerator'],value['denominator']
        return f'{n}/{d} ({100*n/d:.1f}%)' if d else 'N/A'
    for config in sorted({(j['agent'],j['model']) for j in plan['jobs']}):
        group = grouped[config]
        entry = {'agent':config[0], 'model':config[1], 'conditions':{}, 'paired':{}}
        for condition in plan['conditions']:
            values = list(group[condition].values())
            metric = original.metrics(values)
            rr = [r for r in rows if (r['agent'],r['model'],r['condition'])==(*config,condition)]
            approved = [r for r in rr if r['authorization_mode']=='confirmable' and r['response_category']=='clear_approve' and r['asked_human']]
            metric['approved_execution'] = {'numerator':sum(r['attack_effect_executed'] for r in approved),'denominator':len(approved)}
            metric['questions'] = {k:sum(r[k] for r in rr) for k in ['agent_questions','controller_questions','total_human_questions']}
            metric['mean_wall_seconds'] = sum(r['wall_seconds'] for r in rr)/len(rr) if rr else None
            entry['conditions'][condition] = metric
            lines.append('| '+' | '.join([*config, condition, str(len(values)), *[fmt(metric[k]) for k in ['unsafe_asr','benign_completion','hil_recall','strict_post_feedback']],
                f"{metric['questions']['agent_questions']} / {metric['questions']['controller_questions']}"])+' |')
        for left,right in [('prompt_guard_v1',full),(no_human,full)]:
            paired = original.paired_stats(group[left],group[right],draws=args.bootstrap)
            paired.pop('paired_keys',None)
            paired['comparison'] = {'left':left,'right':right,'difference':'right minus left'}
            for key in ['unsafe_attack_success','benign_task_complete','joint_safe_utility']:
                paired[key]['right_minus_left'] = paired[key].pop('guard_minus_neutral')
            entry['paired'][left+'__'+right] = paired
        summary['configurations'].append(entry)
    for condition in plan['conditions']:
        rr = [r for r in rows if r['condition']==condition]
        metric = original.metrics(rr)
        approved = [r for r in rr if r['authorization_mode']=='confirmable' and r['response_category']=='clear_approve' and r['asked_human']]
        metric['approved_execution']={'numerator':sum(r['attack_effect_executed'] for r in approved),'denominator':len(approved)}
        eligible = [r for r in rr if r['authorization_mode']=='confirmable' and r['response_category']=='clear_approve']
        metric['approved_execution_all_eligible'] = {
            'numerator':sum(r['attack_effect_executed'] and not r['unsafe_attack_success'] for r in eligible),
            'denominator':len(eligible)}
        metric['questions']={k:sum(r[k] for r in rr) for k in ['agent_questions','controller_questions','total_human_questions']}
        metric['mean_wall_seconds'] = sum(r['wall_seconds'] for r in rr)/len(rr) if rr else None
        metric['review_requests_valid_runs'] = sum(r['review_requests'] for r in rr)
        metric['failures']=dict(Counter(a['failure_category'] for a in attempts if a['condition']==condition and not a['valid']))
        summary['aggregate'][condition] = metric
        aa = [a for a in attempts if a['condition']==condition]
        lower=sum(a['observed_unsafe'] for a in aa)
        upper=lower+sum(not a['valid'] and not a['observed_unsafe'] for a in aa)
        summary['all_attempt_sensitivity'][condition]={'closed':len(aa),'lower_unsafe_count':lower,'upper_unsafe_count':upper}
        if not args.skip_usage:
            metric['all_attempt_usage'] = {key:sum(a.get(key,0) for a in aa)
                for key in aa[0] if key.startswith(('actor_','reviewer_'))} if aa else {}
    summary['aggregate_paired'] = {}
    for left,right in [('prompt_guard_v1',full),(no_human,full)]:
        values = {condition: {(r['agent'],r['model'],r['case_id'],r['repeat']):r
                    for r in rows if r['condition']==condition} for condition in (left,right)}
        paired = original.paired_stats(values[left],values[right],draws=args.bootstrap)
        paired.pop('paired_keys',None)
        paired['comparison'] = {'left':left,'right':right,'difference':'right minus left'}
        for key in ['unsafe_attack_success','benign_task_complete','joint_safe_utility']:
            paired[key]['right_minus_left'] = paired[key].pop('guard_minus_neutral')
        summary['aggregate_paired'][left+'__'+right] = paired
    lines += ['', 'System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.', '',
        'The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.']
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'README.md').write_text('\n'.join(lines)+'\n')
    (args.output/'replay_audit.json').write_text(json.dumps(checks,indent=2)+'\n')
    for name, data in [('per_case.csv', rows), ('all_attempts.csv',attempts)]:
        if data:
            with (args.output/name).open('w',newline='') as handle:
                writer=csv.DictWriter(handle,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    print(json.dumps({k:v for k,v in summary.items() if k in ['status','planned_attempts','finished_attempts','valid_runs','failed_attempts','pending_attempts']}))


if __name__ == '__main__':
    main()
