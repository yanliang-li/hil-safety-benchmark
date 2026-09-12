from collections import Counter, deque
import importlib.util
from pathlib import Path

import pytest


def scheduler():
    path = Path(__file__).resolve().parents[1] / 'scripts/schedule_four_frameworks.py'
    spec = importlib.util.spec_from_file_location('unified_capacity', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_64_shared_slots_preserve_cohort_order_and_initial_allocation():
    module = scheduler()
    pending = {name: deque(range(100)) for name in ['main', 'hermes']}
    active = Counter(main=0, hermes=0)
    weights = {'main': 48, 'hermes': 16}
    selected = {name: [] for name in pending}
    for _ in range(64):
        name = module.choose_cohort(pending, active, weights)
        selected[name].append(pending[name].popleft())
        active[name] += 1
    assert active == Counter(main=48, hermes=16)
    assert selected == {'main': list(range(48)), 'hermes': list(range(16))}


def test_exhausted_cohort_releases_slots_without_repeating_jobs():
    module = scheduler()
    pending = {'main': deque(), 'hermes': deque(['next'])}
    active = Counter(main=3, hermes=16)
    assert module.choose_cohort(pending, active, {'main': 48, 'hermes': 16}) == 'hermes'
    pending['hermes'].popleft()
    assert module.choose_cohort(pending, active, {'main': 48, 'hermes': 16}) is None


def test_unrecorded_or_inconsistent_concurrency_is_rejected():
    module = scheduler()
    control = {'aggregate_agent_target': 64, 'main_workers': 48, 'hermes_workers': 16}
    assert module.validate_control(control, [64]) == (64, {'main': 48, 'hermes': 16})
    with pytest.raises(ValueError, match='amendment'):
        module.validate_control(control, [32, 40])
    with pytest.raises(ValueError, match='sum'):
        module.validate_control(dict(control, hermes_workers=32), [64])
