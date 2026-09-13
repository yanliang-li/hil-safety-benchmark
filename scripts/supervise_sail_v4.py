"""Run all frozen formal phases sequentially, retaining failures and audit evidence."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', type=Path, default=Path('experiments/sail-v4-20260913/matched_formal_freeze.json'))
    args = parser.parse_args()
    freeze = json.loads(args.freeze.read_text())
    scope = json.loads((ROOT / 'experiments/sail-v4-20260913/authorized_scope.json').read_text())
    if scope.get('scope') != 'match_second_round' or freeze.get('formal_attempts') != 6720:
        raise ValueError('Expanded formal evaluation is outside the current user scope')
    lock = (ROOT / 'reports/sail4-formal-supervisor.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    for rel, expected in freeze['source_sha256'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source changed: ' + rel)
    for rel, expected in freeze.get('analysis_plans',{}).items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError('Frozen analysis projection changed: '+rel)
    path = ROOT / 'reports/sail4-formal-supervisor.json'
    state = json.loads(path.read_text()) if path.exists() else {'started_unix': time.time(), 'phases': {}}
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + ':' + str(ROOT / 'scripts'))
    for relative, expected in freeze['plans'].items():
        plan_path = ROOT / relative
        if hashlib.sha256(plan_path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen plan changed')
        plan = json.loads(plan_path.read_text())
        stage = plan['experiment']
        if state['phases'].get(stage, {}).get('analyzed'):
            continue
        state.update(active_phase=stage, checked_unix=time.time(), complete=False)
        save(path, state)
        progress_path = ROOT / 'reports' / (plan_path.stem + '_progress.json')
        progress = json.loads(progress_path.read_text()) if progress_path.exists() else {}
        if not progress.get('finished_unix'):
            with (ROOT / 'reports' / (stage + '.log')).open('ab') as log:
                subprocess.run([sys.executable, freeze.get('launcher','scripts/hil_guard_v4/launch.py'), relative,
                    '--concurrency', '64', '--adaptive'], cwd=ROOT, env=env, stdout=log,
                    stderr=subprocess.STDOUT, check=True)
        output = 'reports/sail-v4-20260913/' + stage
        with (ROOT / 'reports' / (stage + '-analysis.log')).open('ab') as log:
            subprocess.run([sys.executable, 'scripts/analyze_sail_v4.py', '--plan', relative,
                '--output', output, '--bootstrap', '10000'], cwd=ROOT, env=env,
                stdout=log, stderr=subprocess.STDOUT, check=True)
            subprocess.run([sys.executable, 'scripts/audit_sail_v4.py', '--plan', relative,
                '--output', output + '/input_audit.json'], cwd=ROOT, env=env,
                stdout=log, stderr=subprocess.STDOUT, check=True)
        summary = json.loads((ROOT / output / 'summary.json').read_text())
        audit = json.loads((ROOT / output / 'input_audit.json').read_text())
        state['phases'][stage] = {'finished_attempts': summary['finished_attempts'],
            'valid_runs': summary['valid_runs'], 'failed_attempts': summary['failed_attempts'],
            'input_violation_runs': audit['violation_runs'], 'analyzed': True, 'finished_unix': time.time()}
        save(path, state)
        # Outcome or semantic audit flags do not tune the frozen method or
        # remove an unfavorable phase. Preserve them and complete the matrix.
    state.update(complete=True, active_phase=None, finished_unix=time.time())
    save(path, state)
    print(json.dumps(state), flush=True)


if __name__ == '__main__':
    main()
