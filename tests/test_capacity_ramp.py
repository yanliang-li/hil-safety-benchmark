from collections import Counter, deque
import importlib.util
import json
from pathlib import Path

import pytest


def load(name):
    path = Path(__file__).resolve().parents[1] / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_control(path, limit):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps({'gateway_max_inflight': limit}))
    temporary.replace(path)


def test_live_relay_increase_and_decrease_do_not_drop_active_requests(tmp_path):
    control = tmp_path/'control.json'
    write_control(control, 64)
    semaphore = load('gateway_capacity_ramp').AdjustableSemaphore(control)
    assert all(semaphore.acquire(False) for _ in range(64))
    assert not semaphore.acquire(False)
    write_control(control, 96)
    assert all(semaphore.acquire(False) for _ in range(32))
    assert not semaphore.acquire(False)
    write_control(control, 128)
    assert all(semaphore.acquire(False) for _ in range(32))
    assert not semaphore.acquire(False)
    write_control(control, 64)
    assert semaphore.active == 128
    for _ in range(64):
        semaphore.release()
    assert not semaphore.acquire(False)
    semaphore.release()
    assert semaphore.acquire(False)


def test_relay_rejects_unrecorded_target_and_unmatched_release(tmp_path):
    control = tmp_path/'control.json'
    write_control(control, 192)
    semaphore = load('gateway_capacity_ramp').AdjustableSemaphore(control)
    with pytest.raises(ValueError, match='Unrecorded'):
        semaphore.acquire(False)
    with pytest.raises(ValueError, match='Unmatched'):
        semaphore.release()


@pytest.mark.parametrize('total', [64, 96, 128])
def test_ramp_scheduler_allocates_exact_global_capacity(total):
    module = load('schedule_four_frameworks_ramp')
    weights = {'main': total * 3 // 4, 'hermes': total // 4}
    control = dict(aggregate_agent_target=total, gateway_max_inflight=total,
                   main_workers=weights['main'], hermes_workers=weights['hermes'])
    assert module.validate_control(control, [64, 96, 128]) == (total, weights)
    queues = {name: deque(range(200)) for name in weights}
    active = Counter(main=0, hermes=0)
    for _ in range(total):
        name = module.choose_cohort(queues, active, weights)
        queues[name].popleft()
        active[name] += 1
    assert dict(active) == weights
    with pytest.raises(ValueError, match='must match'):
        module.validate_control(dict(control, gateway_max_inflight=total//2), [64, 96, 128])
