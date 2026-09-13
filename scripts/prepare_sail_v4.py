"""Freeze third-round manifests without overwriting either completed experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'experiments/sail-v4-20260913'
MAIN = ('prompt_guard_v1', 'sail_v3', 'sail_v4')
CONDITIONS = MAIN + ('sail_v4_no_recovery', 'sail_v4_no_human')
SEED = 2026091303


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(formal=False):
    paths = []
    for folder in ('scripts/hil_guard_v4', 'scripts/hil_guard_v3', 'src/hil_safety_bench'):
        paths.extend((ROOT / folder).glob('*.py'))
    names = ['scripts/api_experiment/run_case.py', 'scripts/hermes_experiment/run_case.py',
             'scripts/prepare_sail_v4.py', 'scripts/api_experiment/analyze.py']
    if formal:
        names += ['scripts/analyze_sail_v4.py', 'scripts/audit_sail_v4.py', 'scripts/build_sail_v4_data.py',
                  'scripts/analyze_sail_v3.py', 'scripts/build_clean_controls.py',
                  'scripts/supervise_sail_v4.py', 'scripts/collect_sail_v4.py',
                  'scripts/promote_sail_v4.py', 'tests/test_hil_guard_v4.py', 'tests/test_sail_v4_analysis.py']
    paths.extend(ROOT / name for name in names)
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(paths)}


def build(phase, cases, revision=1, frozen_sources=None):
    old = json.loads((ROOT / 'experiments/sail-20260913/sail-main-v3.json').read_text())
    conditions = list(MAIN if phase == 'clean' else CONDITIONS)
    repeats = {c: (1 if phase == 'preflight' or c not in MAIN else 3) for c in conditions}
    stage = f'sail4-{phase}-r{revision}'
    jobs, blocks = [], []
    rng = random.Random(SEED)
    for repeat in range(1, max(repeats.values()) + 1):
        for config in old['configurations']:
            for case in cases:
                order = [c for c in conditions if repeats[c] >= repeat]
                rng.shuffle(order)
                block = []
                for condition in order:
                    key = [stage, config['agent'], config['model'], case['case_id'], condition, repeat]
                    rid = 'sail4_' + hashlib.sha256(json.dumps(key).encode()).hexdigest()[:24]
                    block.append(dict(config, case_id=case['case_id'], task_id=case['task_id'],
                        case_root=case.get('case_root', 'data/cases'), condition=condition,
                        repeat=repeat, stage=stage, run_id=rid, timeout=900))
                blocks.append(block)
    rng.shuffle(blocks)
    jobs = [j for block in blocks for j in block]
    plan = {'schema_version': 2, 'experiment': stage, 'phase': phase, 'engineering_revision': revision,
        'created_unix': time.time(), 'method_package': 'hil_guard_v4', 'conditions': conditions,
        'reviewer_model': 'deepseek-v4-flash', 'configurations': old['configurations'],
        'cases': cases, 'case_count': len(cases), 'task_cluster_count': len({c['task_id'] for c in cases}),
        'repeats_by_condition': repeats, 'jobs': jobs, 'total_planned_runs': len(jobs),
        'order_seed': SEED, 'ordering': 'Randomly shuffled case/configuration/repeat blocks; random condition order within each block.',
        'source_sha256': frozen_sources or sources(), 'limits': dict(old['limits'], max_recovery_events=4,
            max_finish_recovery_events=2, max_protocol_corrections_per_review=1),
        'scope': {'preflight': 'Engineering only: original invoice and resource-budget tasks, all four replies; excluded from formal evidence.',
            'regression': 'Previously used original80 development cases. Fresh same-round Prompt, SAIL v3 and v4 controls.',
            'heldout': '160 cases from 40 task IDs not previously used in real model experiments; 2 tasks per known attack family. All corpus cases previously received scripted validation; templates/families are not unseen.',
            'clean': '20 separately reported clean counterparts, one per old development attack family. Legacy ASR/HIL labels do not apply. Agent-reviewed draft controls, not independent human gold.'}[phase],
        'analysis': {'primary': 'Same-round Prompt versus v4: lower ASR and higher BCR. Old v3 and ablations are secondary comparisons.',
            'scorer': 'Frozen legacy scorer; independent effect/cumulative/deliverable audit must disclose disagreements.',
            'pairing': 'Both-valid same framework/model/case/repeat; no whole-attempt retries.',
            'bootstrap_draws': 10000, 'bootstrap_cluster': 'task_id', 'sensitivity_cluster': 'attack_family',
            'failures': 'All attempts retained with observed-unsafe/missing-outcome bounds, usage and failure causes.',
            'launch_gate': 'Engineering validity and resource health only; no outcome threshold.',
            'method_freeze': 'No method/data/scorer changes after formal regression begins; finish every frozen condition regardless of outcome.'}}
    path = DEST / (stage + '.json')
    if path.exists():
        raise FileExistsError('Refusing to overwrite frozen plan: ' + str(path))
    DEST.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2) + '\n')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['preflight', 'formal'], required=True)
    parser.add_argument('--revision', type=int, default=1)
    args = parser.parse_args()
    if not 1 <= args.revision <= 3:
        raise ValueError('At most three documented engineering versions')
    old = json.loads((ROOT / 'experiments/sail-20260913/sail-main-v3.json').read_text())
    if args.phase == 'preflight':
        cases = [c for c in old['cases'] if c['task_id'] in ('invoice_reconciliation', 'policy_revision__resource_budget')]
        assert len(cases) == 8
        path = build('preflight', cases, args.revision)
        print(json.dumps({'plan': str(path.relative_to(ROOT)), 'jobs': 480, 'sha256': sha(path)}))
    else:
        manifest = json.loads((DEST / 'split_manifest.json').read_text())
        frozen = sources(formal=True)
        paths = [build('regression', old['cases'], args.revision, frozen),
                 build('heldout', manifest['heldout_cases'], args.revision, frozen),
                 build('clean', manifest['clean_cases'], args.revision, frozen)]
        lock = DEST / 'formal_freeze.json'
        if lock.exists():
            raise FileExistsError(lock)
        value = {'created_unix': time.time(), 'source_sha256': frozen, 'plans': {str(p.relative_to(ROOT)): sha(p) for p in paths},
            'split_manifest_sha256': sha(DEST / 'split_manifest.json'), 'formal_attempts': 33840,
            'method_changes_after_start': 'forbidden; any deviation must be reported separately, with no replacement of frozen outcomes'}
        lock.write_text(json.dumps(value, indent=2) + '\n')
        print(json.dumps({'formal_attempts': 33840, 'plans': list(value['plans'])}))


if __name__ == '__main__':
    main()
