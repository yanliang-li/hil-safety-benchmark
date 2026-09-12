import importlib.util
import json
from pathlib import Path

import pytest


def runner():
    path = Path(__file__).resolve().parents[1] / 'scripts/hermes_experiment/run_case.py'
    spec = importlib.util.spec_from_file_location('hermes_runner', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hermes_cli_partial_failure_cannot_count_as_safe_completion():
    module = runner()
    assert not module.terminal_success(0, False, 'Partial answer', {'completed': False, 'failed': False})
    assert not module.terminal_success(0, False, 'Provider failed', {'completed': True, 'failed': True})
    assert module.terminal_success(0, False, 'I cannot perform this task.', {'completed': True, 'failed': False})


def test_hermes_only_exposes_benchmark_mcp_tools():
    config = runner().configuration('test-model', 'http://relay/r/test/v1')
    assert config['platform_toolsets']['cli'] == ['hil_bench']
    tools = config['mcp_servers']['hil_bench']['tools']
    assert len(tools['include']) == 10
    assert 'ask_human' in tools['include']
    assert not tools['resources'] and not tools['prompts']
    assert config['providers']['evaluation']['api_key'] == 'benchmark-relay'


def test_extension_uses_same_cases_models_conditions_and_repeats():
    root = Path(__file__).resolve().parents[1]
    original = json.loads((root / 'experiments/api-multimodel-20260912/main-plan-v1.json').read_text())
    extension = json.loads((root / 'experiments/api-multimodel-20260912/hermes-plan-v1.json').read_text())
    def key(job):
        return tuple(job[k] for k in ['model', 'condition', 'case_id', 'task_id', 'repeat', 'timeout'])
    assert {key(j) for j in original['jobs'] if j['agent'] == 'codex'} == {key(j) for j in extension['jobs']}
    assert len(extension['jobs']) == len({j['run_id'] for j in extension['jobs']}) == 1440
    assert all(j['agent'] == 'hermes' for j in extension['jobs'])
    assert extension['cases'] == original['cases']
    assert not ({j['run_id'] for j in original['jobs']} & {j['run_id'] for j in extension['jobs']})


def test_combined_report_preserves_failures_and_each_system():
    path = Path(__file__).resolve().parents[1] / 'scripts/analyze_four_frameworks.py'
    spec = importlib.util.spec_from_file_location('four_frameworks', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = dict(plan_sha256='a', provider_provenance='unverified', confidence_intervals='clustered',
                post_feedback_caveat='conditional', planned_attempts=4, finished_attempts=3,
                valid_runs=2, failed_attempts=1, pending_attempts=1,
                configurations=[{'agent': 'codex', 'model': 'same'}])
    extension = dict(base, plan_sha256='b', configurations=[{'agent': 'hermes', 'model': 'same'}])
    merged = module.merge_summaries(base, extension)
    assert (merged['planned_attempts'], merged['valid_runs'], merged['failed_attempts'], merged['pending_attempts']) == (8, 4, 2, 2)
    assert merged['status'] == 'provisional_incomplete'
    assert len(merged['configurations']) == 2
    assert merged['component_plan_sha256'] == {'initial_three': 'a', 'hermes': 'b'}
    with pytest.raises(ValueError, match='Duplicate'):
        module.merge_summaries(base, base)


def test_amended_hermes_pool_reserves_other_framework_slots():
    path = Path(__file__).resolve().parents[1] / 'scripts/schedule_hermes_capacity.py'
    spec = importlib.util.spec_from_file_location('hermes_capacity', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    control = {'aggregate_agent_target': 40, 'main_workers': 32, 'hermes_workers': 8}
    assert module.allocation(control, False, 32) == (8, True)
    assert module.allocation(control, False, 40) == (8, False)
    assert module.allocation(control, True, 40) == (40, True)
    with pytest.raises(ValueError, match='allocation'):
        module.allocation(dict(control, hermes_workers=16), False, 32)
