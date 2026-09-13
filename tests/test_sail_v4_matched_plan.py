import json
from pathlib import Path
import sys
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from prepare_sail_v4_matched import matched_plan, MAPPING


def parent():
    return json.loads((Path(__file__).resolve().parents[1] / 'experiments/sail-20260913/sail-main-v3.json').read_text())


def test_third_round_preserves_every_ordered_second_round_job_except_defense_and_identity():
    old = parent()
    new = matched_plan(old)
    assert new['cases'] == old['cases'] and new['configurations'] == old['configurations']
    assert len(new['jobs']) == 6720
    assert Counter(j['condition'] for j in new['jobs']) == {'prompt_guard_v1':2880,'sail_v4':2880,'sail_v4_no_human':960}
    assert len({j['run_id'] for j in new['jobs']}) == 6720
    assert not {j['run_id'] for j in new['jobs']} & {j['run_id'] for j in old['jobs']}
    for a,b in zip(old['jobs'],new['jobs']):
        assert b['condition'] == MAPPING[a['condition']]
        assert {k:v for k,v in a.items() if k not in ('condition','stage','run_id')} == {k:v for k,v in b.items() if k not in ('condition','stage','run_id')}
    for k,v in old['limits'].items():assert new['limits'][k] == v


def test_preflight_only_checks_active_conditions_on_eight_original_cases():
    plan = matched_plan(parent(), preflight=True)
    assert len(plan['jobs']) == 288 and len(plan['cases']) == 8
    assert {j['repeat'] for j in plan['jobs']} == {1}
    assert set(plan['conditions']) == set(MAPPING.values())
    assert len({c['task_id'] for c in plan['cases']}) == 2
