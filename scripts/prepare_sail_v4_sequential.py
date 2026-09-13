"""Freeze the same 6720 attempts with all main jobs before the ablation."""
import copy
import json
from pathlib import Path
import time

from prepare_sail_v4 import sources
from prepare_sail_v4_matched import matched_plan, MAPPING, sha

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'experiments/sail-v4-20260913'


def ordered_plan(parent):
    plan = matched_plan(parent)
    main = [j for j in plan['jobs'] if j['condition'] != 'sail_v4_no_human']
    ablation = [j for j in plan['jobs'] if j['condition'] == 'sail_v4_no_human']
    plan['jobs'] = main + ablation
    plan['execution_order'] = 'main_then_ablation'
    plan['main_attempts'], plan['ablation_attempts'] = len(main), len(ablation)
    plan['ordering'] = 'Preserve second-round relative order within each group; finish all main jobs before starting any no-human ablation job.'
    plan['analysis']['ablation_timing_limit'] = 'Ablation follows the main experiment; serving-time drift may affect its comparison to repeat-1 main results.'
    return plan


def main():
    scope = json.loads((DEST/'authorized_scope.json').read_text())
    if scope.get('execution_order') != 'main_then_ablation' or scope['formal_attempts'] != 6720:
        raise ValueError('Scope does not authorize the sequential 6720-attempt design')
    parent_path = ROOT/'experiments/sail-20260913/sail-main-v3.json'
    plan = ordered_plan(json.loads(parent_path.read_text()))
    gate = json.loads((DEST/'matched_engineering_gate.json').read_text())
    if not gate.get('passed'):
        raise ValueError('Engineering gate has not passed')
    plan.update(engineering_revision=gate['engineering_revision'],
                revision_basis='Frozen after protocol/provenance engineering validation; formal scope matches round two.')
    frozen = sources(formal=True)
    for rel in ('scripts/prepare_sail_v4_matched.py','scripts/prepare_sail_v4_sequential.py',
                'scripts/launch_sail_v4_sequential.py','scripts/sail_v4_capacity.py',
                'tests/test_sail_v4_capacity.py','tests/test_sail_v4_matched_plan.py','tests/test_sail_v4_sequential.py',
                'experiments/sail-v4-20260913/capacity-amendment-v1.json',
                'scripts/prepare_sail_v4_engineering_r3.py','tests/test_sail_v4_engineering_r3.py'):
        frozen[rel] = sha(ROOT/rel)
    plan.update(source_sha256=frozen,authorized_scope_sha256=sha(DEST/'authorized_scope.json'),
        matched_parent={'path':str(parent_path.relative_to(ROOT)),'sha256':sha(parent_path),
            'condition_mapping':MAPPING,'ordered_jobs_preserved':False,'relative_order_within_main_and_ablation_preserved':True})
    plan['execution_capacity'] = json.loads((DEST/'capacity-amendment-v1.json').read_text())
    # This is an analysis projection, not an additional execution plan.
    primary = copy.deepcopy(plan)
    primary.update(experiment='sail4-main-r2',jobs=plan['jobs'][:5760],
        conditions=['prompt_guard_v1','sail_v4'],repeats_by_condition={'prompt_guard_v1':3,'sail_v4':3},
        total_planned_runs=5760,scope='Main experiment only: 5760 attempts. All jobs are a subset of sail4-matched-r2; no extra model runs.',
        analysis_only=True)
    path=DEST/'sail4-matched-r2.json'; main_path=DEST/'sail4-main-r2.json'; lock=DEST/'matched_formal_freeze.json'
    if any(p.exists() for p in (path,main_path,lock)):
        raise FileExistsError('Refusing to overwrite frozen sequential artifacts')
    assert plan['main_attempts']==5760 and plan['ablation_attempts']==960
    for p,v in [(path,plan),(main_path,primary)]:p.write_text(json.dumps(v,indent=2)+'\n')
    freeze={'created_unix':time.time(),'source_sha256':frozen,'plans':{str(path.relative_to(ROOT)):sha(path)},
        'analysis_plans':{str(main_path.relative_to(ROOT)):sha(main_path)},'formal_attempts':6720,
        'main_attempts':5760,'ablation_attempts':960,'execution_order':'main_then_ablation',
        'launcher':'scripts/launch_sail_v4_sequential.py','authorized_scope_sha256':plan['authorized_scope_sha256'],
        'method_changes_after_start':'forbidden; retain all original attempts and failures'}
    lock.write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps({'formal_attempts':6720,'main_first':5760,'ablation_after':960}))


if __name__ == '__main__':
    main()
