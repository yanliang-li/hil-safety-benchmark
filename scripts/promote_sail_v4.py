"""Drain r1, validate engineering r2, then freeze and finish all formal phases.

The launch gate uses protocol/provenance and configuration coverage, never
ASR/BCR outcomes. Any blocked gate is recorded for review rather than bypassed.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from supervise_sail_v4 import save

ROOT = Path(__file__).resolve().parents[1]


def main():
    lock = (ROOT / 'reports/sail4-promotion.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state_path = ROOT / 'reports/sail4-promotion.json'
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + ':' + str(ROOT / 'scripts'))
    while True:
        path = ROOT / 'reports/sail4-preflight-r1_progress.json'
        progress = json.loads(path.read_text()) if path.exists() else {}
        if progress.get('finished_unix'):
            break
        save(state_path, {'state': 'waiting_for_r1_to_drain', 'checked_unix': time.time(),
            'closed_attempts': progress.get('finished_attempts', 0), 'planned': 480})
        time.sleep(30)
    save(state_path, {'state': 'engineering_r2', 'started_unix': time.time()})
    plan_rel = 'experiments/sail-v4-20260913/sail4-preflight-r2.json'
    progress_path = ROOT / 'reports/sail4-preflight-r2_progress.json'
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {}
    if not progress.get('finished_unix'):
        with (ROOT / 'reports/sail4-preflight-r2.log').open('ab') as log:
            subprocess.run([sys.executable, 'scripts/hil_guard_v4/launch.py', plan_rel, '--concurrency', '32'],
                cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    output = 'reports/sail-v4-20260913/sail4-preflight-r2'
    for command in ([sys.executable, 'scripts/analyze_sail_v4.py', '--plan', plan_rel, '--output', output, '--bootstrap', '10000'],
                    [sys.executable, 'scripts/audit_sail_v4.py', '--plan', plan_rel, '--output', output + '/input_audit.json']):
        subprocess.run(command, cwd=ROOT, env=env, check=True)
    summary = json.loads((ROOT / output / 'summary.json').read_text())
    audit = json.loads((ROOT / output / 'input_audit.json').read_text())
    missing = []
    for config in summary['configurations']:
        for condition in ('sail_v4', 'sail_v4_no_recovery', 'sail_v4_no_human'):
            if config['conditions'][condition]['benign_completion']['denominator'] == 0:
                missing.append({'agent': config['agent'], 'model': config['model'], 'condition': condition})
    gate = {'complete_480_attempts': summary['finished_attempts'] == 480,
        'valid_input_violation_runs': audit['valid_violation_runs'], 'configurations_without_valid_controller_episode': missing,
        'outcome_threshold_used': False, 'whole_episode_retries': False,
        'engineering_revision': 2, 'checked_unix': time.time()}
    gate['passed'] = gate['complete_480_attempts'] and not missing and audit['valid_violation_runs'] == 0
    save(ROOT / 'experiments/sail-v4-20260913/engineering_gate.json', gate)
    if not gate['passed']:
        save(state_path, {'state': 'engineering_gate_requires_review', 'gate': gate})
        return
    freeze = ROOT / 'experiments/sail-v4-20260913/formal_freeze.json'
    if not freeze.exists():
        subprocess.run([sys.executable, 'scripts/prepare_sail_v4.py', '--phase', 'formal', '--revision', '2'], cwd=ROOT, env=env, check=True)
    save(state_path, {'state': 'formal_phases', 'started_unix': time.time(), 'gate': gate})
    subprocess.run([sys.executable, 'scripts/supervise_sail_v4.py'], cwd=ROOT, env=env, check=True)
    save(state_path, {'state': 'formal_experiments_complete', 'finished_unix': time.time(), 'gate': gate})


if __name__ == '__main__':
    main()
