"""Replay both frozen cohorts, then combine their reports without pooling systems."""
import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports/api-multimodel-20260912'


def merge_summaries(main, hermes):
    result = {'experiment': 'four-framework-api-evaluation',
              'component_plan_sha256': {'initial_three': main['plan_sha256'], 'hermes': hermes['plan_sha256']},
              'provider_provenance': main['provider_provenance'],
              'confidence_intervals': main['confidence_intervals'],
              'post_feedback_caveat': main['post_feedback_caveat'],
              'cohort_caveat': 'Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.'}
    for key in ['planned_attempts', 'finished_attempts', 'valid_runs', 'failed_attempts', 'pending_attempts']:
        result[key] = main[key] + hermes[key]
    result['status'] = 'complete' if result['pending_attempts'] == 0 else 'provisional_incomplete'
    result['configurations'] = sorted(main['configurations'] + hermes['configurations'], key=lambda r: (r['agent'], r['model']))
    identities = [(r['agent'], r['model']) for r in result['configurations']]
    if len(set(identities)) != len(identities):
        raise ValueError('Duplicate system configuration across cohorts')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap', type=int, default=1000)
    args = parser.parse_args()
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))
    for name, plan_name in [('main', 'main-plan-v1.json'), ('hermes', 'hermes-plan-v1.json')]:
        plan = ROOT / 'experiments/api-multimodel-20260912' / plan_name
        output = REPORTS / name
        for script, more in [('scripts/api_experiment/analyze.py', ['--bootstrap', str(args.bootstrap)]),
                             ('scripts/audit_api_attempts.py', [])]:
            subprocess.run([sys.executable, script, '--plan', str(plan), '--output', str(output), *more],
                           cwd=ROOT, env=env, check=True, capture_output=True, text=True)
        if name == 'hermes':
            path = output / 'README.md'
            path.write_text(path.read_text().replace('# Three-harness API experiment', '# Hermes extension', 1))
    summaries = {name: json.loads((REPORTS / name / 'summary.json').read_text()) for name in ['main', 'hermes']}
    combined = merge_summaries(summaries['main'], summaries['hermes'])
    output = REPORTS / 'four-frameworks'
    output.mkdir(exist_ok=True)
    (output / 'summary.json').write_text(json.dumps(combined, indent=2) + '\n')
    lines = ['# Four-framework API experiment', '',
        f"Status: **{combined['status']}**. {combined['finished_attempts']}/{combined['planned_attempts']} attempts closed; {combined['valid_runs']} valid, {combined['failed_attempts']} failed, {combined['pending_attempts']} pending.", '',
        '| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |',
        '|---|---|---|---:|---:|---:|---:|']
    def fmt(value):
        n, d = value['numerator'], value['denominator']
        return f'{n}/{d} ({100*n/d:.1f}%)' if d else 'N/A'
    for config in combined['configurations']:
        for condition, metrics in config['conditions'].items():
            lines.append('| ' + ' | '.join([config['agent'], config['model'], condition,
                *[fmt(metrics[k]) for k in ['unsafe_asr', 'benign_completion', 'hil_recall', 'strict_post_feedback']]]) + ' |')
    lines += ['', combined['cohort_caveat'], '', combined['post_feedback_caveat'], '',
              'The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.']
    (output / 'README.md').write_text('\n'.join(lines) + '\n')
    for filename in ['per_case.csv', 'all_attempts.csv']:
        rows = []
        for cohort in ['main', 'hermes']:
            path = REPORTS / cohort / filename
            if path.exists():
                with path.open() as f:
                    rows.extend(dict(cohort=cohort, **row) for row in csv.DictReader(f))
        if rows:
            if len({r['run_id'] for r in rows}) != len(rows):
                raise ValueError('Duplicate attempt ID in combined export')
            with (output / filename).open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    audits = {name: json.loads((REPORTS / name / 'attempt_audit.json').read_text()) for name in ['main', 'hermes']}
    (output / 'attempt_audit.json').write_text(json.dumps(audits, indent=2) + '\n')
    replays = [entry for name in ['main', 'hermes'] for entry in json.loads((REPORTS / name / 'replay_audit.json').read_text())]
    (output / 'replay_audit.json').write_text(json.dumps(replays, indent=2) + '\n')
    print(json.dumps({k: combined[k] for k in ['status', 'finished_attempts', 'planned_attempts', 'valid_runs', 'failed_attempts']}))


if __name__ == '__main__':
    main()
