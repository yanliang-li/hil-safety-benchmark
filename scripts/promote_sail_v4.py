"""Drain r1, validate r2, then replace the second-round defense at equal scale.

The launch gate uses protocol/provenance and configuration coverage, never
ASR/BCR outcomes. Any blocked gate is recorded for review rather than bypassed.
"""
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--engineering-revision', type=int, choices=(2, 3), default=2)
    args = parser.parse_args()
    revision = args.engineering_revision
    lock = (ROOT / 'reports/sail4-promotion.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state_path = ROOT / 'reports/sail4-promotion.json'
    scope = json.loads((ROOT / 'experiments/sail-v4-20260913/authorized_scope.json').read_text())
    if scope.get('scope') != 'match_second_round' or scope.get('formal_attempts') != 6720:
        raise ValueError('Only the user-corrected 6720-attempt scope may launch')
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + ':' + str(ROOT / 'scripts'))
    while True:
        preceding = 'sail4-preflight-r1' if revision == 2 else 'sail4-preflight-matched-r2'
        path = ROOT / 'reports' / (preceding + '_progress.json')
        progress = json.loads(path.read_text()) if path.exists() else {}
        if progress.get('finished_unix'):
            break
        save(state_path, {'state': 'waiting_for_previous_engineering_to_drain', 'previous_phase': preceding,
            'checked_unix': time.time(), 'closed_attempts': progress.get('finished_attempts', 0),
            'planned': progress.get('planned')})
        time.sleep(30)
    save(state_path, {'state': f'engineering_r{revision}', 'started_unix': time.time()})
    stage = f'sail4-preflight-matched-r{revision}'
    plan_rel = f'experiments/sail-v4-20260913/{stage}.json'
    progress_path = ROOT / 'reports' / (stage + '_progress.json')
    progress = json.loads(progress_path.read_text()) if progress_path.exists() else {}
    # A restarted coordinator must wait for an existing preflight launcher,
    # not start a duplicate or replace any attempt.
    while not progress.get('finished_unix'):
        with (ROOT/'reports'/(stage+'.lock')).open('a') as handle:
            try:
                fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
                running=False
            except BlockingIOError:
                running=True
        if not running:
            break
        time.sleep(30)
        progress=json.loads(progress_path.read_text()) if progress_path.exists() else {}
    if not progress.get('finished_unix'):
        with (ROOT / 'reports' / (stage + '.log')).open('ab') as log:
            launcher = 'scripts/hil_guard_v4/launch.py' if revision == 2 else 'scripts/launch_sail_v4_sequential.py'
            capacity = ['--concurrency', '32'] if revision == 2 else ['--concurrency', '96', '--adaptive']
            subprocess.run([sys.executable, launcher, plan_rel, *capacity],
                cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
    output = 'reports/sail-v4-20260913/' + stage
    for command in ([sys.executable, 'scripts/analyze_sail_v4.py', '--plan', plan_rel, '--output', output, '--bootstrap', '10000'],
                    [sys.executable, 'scripts/audit_sail_v4.py', '--plan', plan_rel, '--output', output + '/input_audit.json']):
        subprocess.run(command, cwd=ROOT, env=env, check=True)
    summary = json.loads((ROOT / output / 'summary.json').read_text())
    audit = json.loads((ROOT / output / 'input_audit.json').read_text())
    missing = []
    for config in summary['configurations']:
        for condition in ('prompt_guard_v1', 'sail_v4', 'sail_v4_no_human'):
            if config['conditions'][condition]['benign_completion']['denominator'] == 0:
                missing.append({'agent': config['agent'], 'model': config['model'], 'condition': condition})
    gate = {'complete_288_attempts': summary['finished_attempts'] == 288,
        'valid_input_violation_runs': audit['valid_violation_runs'], 'configurations_without_valid_controller_episode': missing,
        'outcome_threshold_used': False, 'whole_episode_retries': False,
        'engineering_revision': revision, 'checked_unix': time.time(), 'preflight_plan': plan_rel}
    gate['passed'] = gate['complete_288_attempts'] and not missing and audit['valid_violation_runs'] == 0
    save(ROOT / 'experiments/sail-v4-20260913/matched_engineering_gate.json', gate)
    if not gate['passed']:
        save(state_path, {'state': 'engineering_gate_requires_review', 'gate': gate})
        return
    freeze = ROOT / 'experiments/sail-v4-20260913/matched_formal_freeze.json'
    if not freeze.exists():
        subprocess.run([sys.executable, 'scripts/prepare_sail_v4_sequential.py'], cwd=ROOT, env=env, check=True)
    save(state_path, {'state': 'formal_phases', 'started_unix': time.time(), 'gate': gate})
    subprocess.run([sys.executable, 'scripts/supervise_sail_v4.py', '--freeze', str(freeze)], cwd=ROOT, env=env, check=True)
    save(state_path, {'state': 'formal_experiments_complete', 'finished_unix': time.time(), 'gate': gate})


if __name__ == '__main__':
    main()
