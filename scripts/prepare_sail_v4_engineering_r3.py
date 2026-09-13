"""Document and freeze the final bounded protocol engineering revision."""
import hashlib
import json
from pathlib import Path
import shutil
import time

from prepare_sail_v4 import sources
from prepare_sail_v4_matched import matched_plan, sha

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'experiments/sail-v4-20260913'


def revision_plan(parent):
    plan = matched_plan(parent, preflight=True)
    stage = 'sail4-preflight-matched-r3'
    plan.update(experiment=stage, engineering_revision=3,
                revision_basis='Clarify existing reviewer schema; do not relax validation or change actor budgets.',
                execution_order='main_then_ablation', main_attempts=192, ablation_attempts=96)
    for job in plan['jobs']:
        job['stage'] = stage
        key = [stage, job['agent'], job['model'], job['case_id'], job['condition'], job['repeat']]
        job['run_id'] = 'sail4_' + hashlib.sha256(json.dumps(key).encode()).hexdigest()[:24]
    plan['jobs'] = ([j for j in plan['jobs'] if j['condition'] != 'sail_v4_no_human'] +
                    [j for j in plan['jobs'] if j['condition'] == 'sail_v4_no_human'])
    plan['ordering'] = 'Same engineering cases/configurations/repeats; main-condition jobs before no-human jobs. Excluded from formal results.'
    return plan


def main():
    if (DEST / 'matched_formal_freeze.json').exists():
        raise ValueError('No engineering changes after formal freeze')
    path = DEST / 'sail4-preflight-matched-r3.json'
    if path.exists():
        raise FileExistsError('Refusing to overwrite engineering revision')
    plan = revision_plan(json.loads((ROOT / 'experiments/sail-20260913/sail-main-v3.json').read_text()))
    frozen = sources()
    for relative in ('scripts/prepare_sail_v4_engineering_r3.py', 'scripts/launch_sail_v4_sequential.py',
                     'scripts/sail_v4_capacity.py', 'tests/test_sail_v4_engineering_r3.py',
                     'tests/test_sail_v4_capacity.py', 'experiments/sail-v4-20260913/capacity-amendment-v1.json'):
        frozen[relative] = sha(ROOT / relative)
    plan['source_sha256'] = frozen
    plan['execution_capacity'] = json.loads((DEST / 'capacity-amendment-v1.json').read_text())
    archive = DEST / 'engineering/r3'
    archive.mkdir(parents=True, exist_ok=True)
    for source in (ROOT / 'scripts/hil_guard_v4').glob('*.py'):
        shutil.copy2(source, archive / source.name)
    path.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({'plan': str(path.relative_to(ROOT)), 'attempts': len(plan['jobs']), 'created_unix': time.time()}))


if __name__ == '__main__':
    main()
