import copy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from prepare_sail_v4_matched import matched_plan
from prepare_sail_v4_engineering_r3 import revision_plan
from hil_guard_v4.protocol import validate


def test_engineering_r3_has_same_cases_and_limits_without_replacing_r2():
    parent = json.loads((Path(__file__).resolve().parents[1] / 'experiments/sail-20260913/sail-main-v3.json').read_text())
    old, new = matched_plan(parent, preflight=True), revision_plan(parent)
    assert len(new['jobs']) == 288 and new['cases'] == old['cases'] and new['limits'] == old['limits']
    assert not ({j['run_id'] for j in new['jobs']} & {j['run_id'] for j in old['jobs']})
    def keys(plan):
        return {tuple(sorted((k, str(v)) for k, v in j.items() if k not in ('run_id', 'stage'))) for j in plan['jobs']}
    assert keys(new) == keys(old)


def test_local_report_is_still_not_accepted_as_consequential_authority():
    task = 'Write outputs/report.md.'
    obligation = {'id': 'report', 'tool': 'write_output', 'task_quote': 'Write outputs/report.md', 'description': 'Save report'}
    contract = {'effects': [], 'obligations': [obligation], 'pending_extensions': []}
    assert validate('contract', contract, {'trusted_task': task}) == contract
    invalid = copy.deepcopy(contract)
    invalid['effects'] = [dict(obligation, required=True, object='report', purpose='report', scope='local', max_total=1)]
    with pytest.raises(ValueError, match='consequential_effect_tool'):
        validate('contract', invalid, {'trusted_task': task})
