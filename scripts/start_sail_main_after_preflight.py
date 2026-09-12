"""Start the frozen main comparison after engineering audit and container drain."""
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]


def run(args, **kwargs):
    return subprocess.run(args,text=True,capture_output=True,check=True,**kwargs)


def main():
    lock=(ROOT/'reports/sail-main-start.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    plan=ROOT/'experiments/sail-20260913/sail-main-v3.json'
    if (ROOT/'reports/sail-main-v3_progress.json').exists() or (ROOT/'reports/sail-main-v3-controller.json').exists():
        raise RuntimeError('Main experiment already started')
    while True:
        progress=json.loads((ROOT/'reports/sail-preflight-v3_progress.json').read_text())
        if progress.get('finished_unix'):
            break
        print(json.dumps({'waiting_for_preflight':progress['finished_attempts'],'active':progress['active']}),flush=True)
        time.sleep(60)
    assert progress['finished_attempts']==progress['planned']==72
    output='reports/sail-20260913/preflight-v3'
    run(['python3','scripts/analyze_sail_v3.py','--plan','experiments/sail-20260913/sail-preflight-v3.json',
         '--output',output,'--bootstrap','10000'],cwd=ROOT,timeout=120)
    run(['python3','scripts/audit_sail_inputs.py','--plan','experiments/sail-20260913/sail-preflight-v3.json',
         '--output',output+'/input_audit.json'],cwd=ROOT,timeout=120)
    summary=json.loads((ROOT/output/'summary.json').read_text())
    frameworks={j['agent'] for j in progress['results'] if j.get('completed') and j['condition']=='sail_v3'}
    assert frameworks=={'codex','claude-code','deepseek-harness','hermes'}
    active=run(['docker','ps','-q','--filter','label=org.hilbench.experiment=sail-20260913'],timeout=20).stdout.strip()
    assert not active,'Preflight containers have not drained'
    gate={'preflight_complete':True,'attempts':72,'valid_runs':summary['valid_runs'],
          'native_frameworks_with_valid_sail_runs':sorted(frameworks),'score_replay':'passed',
          'reviewer_wire_input_and_permit_audit':'passed','active_preflight_containers':0,
          'selection_rule':'Engineering checks only; no threshold on ASR, utility, or treatment differences.',
          'main_plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'checked_unix':time.time()}
    (ROOT/'reports/sail-20260913/preflight_gate.json').write_text(json.dumps(gate,indent=2)+'\n')
    log=(ROOT/'reports/sail-main-v3-controller.log').open('a')
    child=subprocess.Popen(['python3','scripts/hil_guard_v3/launch.py',str(plan),'--concurrency','96'],
        cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    record={'pid':child.pid,'started_unix':time.time(),'plan_sha256':gate['main_plan_sha256'],
            'concurrency':96,'planned':6720}
    (ROOT/'reports/sail-main-v3-controller.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)


if __name__=='__main__':
    main()
