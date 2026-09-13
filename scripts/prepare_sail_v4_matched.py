"""Replace the second-round defense, preserving its cases and ordered design."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time

from prepare_sail_v4 import sources

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'experiments/sail-v4-20260913'
PARENT = ROOT / 'experiments/sail-20260913/sail-main-v3.json'
MAPPING = {'prompt_guard_v1': 'prompt_guard_v1', 'sail_v3': 'sail_v4',
           'sail_v3_no_human': 'sail_v4_no_human'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matched_plan(parent, *, preflight=False):
    plan = copy.deepcopy(parent)
    stage = 'sail4-preflight-matched-r2' if preflight else 'sail4-matched-r2'
    cases = parent['cases']
    if preflight:
        cases = [c for c in cases if c['task_id'] in ('invoice_reconciliation', 'policy_revision__resource_budget')]
    allowed = {c['case_id'] for c in cases}
    jobs = []
    for original in parent['jobs']:
        if original['case_id'] not in allowed or (preflight and original['repeat'] != 1):
            continue
        job = dict(original, condition=MAPPING[original['condition']], stage=stage)
        key = [stage, job['agent'], job['model'], job['case_id'], job['condition'], job['repeat']]
        job['run_id'] = 'sail4_' + hashlib.sha256(json.dumps(key).encode()).hexdigest()[:24]
        jobs.append(job)
    plan.update(schema_version=2, experiment=stage, phase='preflight' if preflight else 'matched',
        engineering_revision=2, created_unix=time.time(), method_package='hil_guard_v4',
        conditions=list(MAPPING.values()), cases=cases, case_count=len(cases),
        task_cluster_count=len({c['task_id'] for c in cases}), jobs=jobs, total_planned_runs=len(jobs),
        repeats_by_condition={MAPPING[c]: 1 if preflight else n for c,n in parent['repeats_by_condition'].items()},
        scope='Engineering only; excluded from formal evidence.' if preflight else
            'Same 80 development cases, four frameworks, three model routes and 6720-attempt design as round two. '
            'Replace SAIL v3 with SAIL v4 and replace its no-human ablation correspondingly. '
            'Prompt is rerun in this round. No extra tasks, clean controls, fresh v3, or no-recovery ablation.',
        revision_basis='User corrected experiment scope before any expanded formal phase started. '
            'The runtime remains engineering revision 2; only the experiment selection is corrected.',
        ordering='Exact second-round job order with condition names mapped; preflight selects its eight cases from repeat 1.')
    plan['analysis']['primary'] = 'Fresh Prompt versus SAIL v4 within this round; lower ASR and higher BCR together.'
    plan['analysis']['ablation'] = 'SAIL v4 versus its no-human ablation, matched repeat 1 only.'
    plan['analysis']['cross_round_limit'] = 'Earlier v3 results are historical; changes across rounds are not a concurrent causal comparison.'
    plan['analysis']['method_freeze'] = 'No method/data/scorer changes after formal start; no replacement retries.'
    plan['limits'].update(max_recovery_events=4, max_finish_recovery_events=2, max_protocol_corrections_per_review=1)
    return plan


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('preflight','formal'), required=True)
    args = parser.parse_args()
    scope = json.loads((DEST/'authorized_scope.json').read_text())
    if scope['scope'] != 'match_second_round' or scope['formal_attempts'] != 6720:
        raise ValueError('The active scope must match the second round')
    preflight = args.phase == 'preflight'
    parent = json.loads(PARENT.read_text())
    plan = matched_plan(parent, preflight=preflight)
    frozen = sources(formal=not preflight)
    for rel in ('scripts/prepare_sail_v4_matched.py', 'tests/test_sail_v4_matched_plan.py'):
        frozen[rel] = sha(ROOT/rel)
    plan['source_sha256'] = frozen
    plan['matched_parent'] = {'path':str(PARENT.relative_to(ROOT)), 'sha256':sha(PARENT),
        'condition_mapping':MAPPING, 'ordered_jobs_preserved':True}
    plan['authorized_scope_sha256'] = sha(DEST/'authorized_scope.json')
    path = DEST/(plan['experiment']+'.json')
    lock = DEST/'matched_formal_freeze.json'
    if path.exists() or (not preflight and lock.exists()):
        raise FileExistsError('Refusing to overwrite a frozen matched design')
    expected = 288 if preflight else 6720
    assert len(plan['jobs']) == expected
    path.write_text(json.dumps(plan,indent=2)+'\n')
    if not preflight:
        freeze = {'created_unix':time.time(), 'source_sha256':frozen,
            'plans':{str(path.relative_to(ROOT)):sha(path)}, 'formal_attempts':6720,
            'authorized_scope_sha256':plan['authorized_scope_sha256'], 'matched_parent':plan['matched_parent'],
            'method_changes_after_start':'forbidden; deviations require separate disclosure, never replacement of frozen outcomes'}
        lock.write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps({'plan':str(path.relative_to(ROOT)), 'attempts':expected, 'sha256':sha(path)}))


if __name__ == '__main__':
    main()
