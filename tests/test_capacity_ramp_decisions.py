import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location('capacity_observer', ROOT / 'scripts/observe_capacity_ramp.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample():
    return dict(window_seconds=300, recent_closed=160, valid_per_hour=1800,
                host_available_memory_gib=130, free_project_disk_gib=100,
                host_load_1m=15, logical_cpus=152, failure_categories={},
                transport_error_rate=.002, http_error_rate=0, failed_attempt_rate=.03)


def test_more_valid_results_with_stable_resources_and_errors_pass():
    rule = json.loads((ROOT / 'experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json').read_text())['checkpoint_rule']
    assert load().assess(sample(), dict(valid_per_hour=1272, failed_attempt_rate=.036), rule) == []


def test_higher_failure_rate_blocks_promotion_even_if_throughput_increases():
    rule = json.loads((ROOT / 'experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json').read_text())['checkpoint_rule']
    failures = load().assess(dict(sample(), transport_error_rate=.1, failed_attempt_rate=.2),
                             dict(valid_per_hour=1272, failed_attempt_rate=.036), rule)
    assert set(failures) == {'transport_error_rate', 'increased_failed_attempt_rate'}


def test_startup_window_and_insufficient_memory_block_promotion():
    rule = json.loads((ROOT / 'experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json').read_text())['checkpoint_rule']
    failures = load().assess(dict(sample(), window_seconds=100, host_available_memory_gib=80),
                             dict(valid_per_hour=1272, failed_attempt_rate=.036), rule)
    assert set(failures) == {'insufficient_observation', 'host_resource_pressure'}
