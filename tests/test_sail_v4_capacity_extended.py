import hashlib
import json
from pathlib import Path
import sys
import threading

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import sail_v4_capacity as frozen
from sail_v4_capacity_extended import ExtendedCapacityPolicy
from gateway_capacity_extended import ExtendedSemaphore
from launch_sail_v4_sequential import MainFirstPool
from supervise_sail_v4_extended import extended_command


def window(n=100, errors=0, closed=40, failed=4):
    return dict(requests=n, errors=errors, error_rate=errors/n, elapsed_s=300,
                closed_attempts=closed, valid_attempts=closed-failed, failed_attempts=failed,
                oom_attempts=0)


def test_extension_requires_gain_and_backs_off_without_dropping_requests():
    policy = ExtendedCapacityPolicy()
    for now in (300, 600):
        policy.observe(window(), True, 150, 128, now)
    assert policy.target == 160
    for now in (900, 1200):
        reason = policy.observe(window(), True, 150, 160, now)
    assert policy.target == 128 and 'backoff' in reason
    for now in (1500, 1800):
        policy.observe(window(140), True, 150, 128, now)
    assert policy.target == 128


def test_extension_cannot_jump_levels_or_ignore_failures_or_memory():
    policy = ExtendedCapacityPolicy()
    policy.observe(window(), True, 150, 128, 300)
    policy.observe(window(), True, 100, 128, 600)
    assert policy.target == 128
    policy.observe(window(), True, 150, 128, 900)
    assert policy.target == 160
    for now in (1200, 1500):
        policy.observe(window(130, failed=20), True, 150, 160, now)
    assert policy.target == 128
    policy.observe(window(errors=5), True, 150, 128, 1800)
    assert policy.target == 96


def test_trial_draining_tail_is_not_a_throughput_comparison():
    policy = ExtendedCapacityPolicy()
    for now in (300, 600, 900):
        policy.observe(window(), True, 150, 2, now)
    assert policy.target == 128 and not policy.healthy


def test_all_four_steps_can_reach_256_with_measured_gains():
    policy = ExtendedCapacityPolicy()
    expected = [160, 192, 224, 256]
    now = 0
    for index, target in enumerate(expected):
        for _ in range(2):
            now += 300
            policy.observe(window(100 + 30*index, closed=40+10*index), True, 180, policy.target, now)
        assert policy.target == target


def test_gateway_admission_256_and_live_reduction(tmp_path):
    path = tmp_path / 'control.json'
    path.write_text(json.dumps({'gateway_max_inflight':256}))
    semaphore = ExtendedSemaphore(path)
    assert all(semaphore.acquire(blocking=False) for _ in range(256))
    assert not semaphore.acquire(blocking=False)
    path.write_text(json.dumps({'gateway_max_inflight':160}))
    for _ in range(96):
        semaphore.release()
    assert not semaphore.acquire(blocking=False)
    semaphore.release()
    assert semaphore.acquire(blocking=False)
    path.write_text(json.dumps({'gateway_max_inflight':512}))
    with pytest.raises(ValueError):
        semaphore.limit()


def test_only_launcher_command_changes():
    original = ['python3','scripts/launch_sail_v4_sequential.py','plan.json','--concurrency','96','--adaptive']
    changed = extended_command(original)
    assert changed == ['python3','scripts/launch_sail_v4_extended.py','plan.json','--concurrency','128','--adaptive']
    assert original[1] == 'scripts/launch_sail_v4_sequential.py'
    analysis = ['python3','scripts/analyze_sail_v4.py','--bootstrap','10000']
    assert extended_command(analysis) is analysis


def test_frozen_plan_and_sources_remain_exact():
    root = Path(__file__).resolve().parents[1]
    freeze = json.loads((root / 'experiments/sail-v4-20260913/matched_formal_freeze.json').read_text())
    for relative, expected in {**freeze['source_sha256'], **freeze['plans'], **freeze['analysis_plans']}.items():
        assert hashlib.sha256((root/relative).read_bytes()).hexdigest() == expected


def test_256_workers_preserve_failed_outcomes_and_main_barrier(tmp_path, monkeypatch):
    jobs = [dict(run_id=str(i), stage='test', condition='sail_v4') for i in range(256)]
    jobs += [dict(run_id='ablation', stage='test', condition='sail_v4_no_human')]
    barrier = threading.Barrier(256)
    done = []
    def run(job, snapshot):
        if job['condition'] == 'sail_v4_no_human':
            assert len(done) == 256
            assert json.loads((tmp_path/'reports/plan_progress.json').read_text())['finished_attempts'] == 256
        else:
            barrier.wait(timeout=10)
            done.append(job['run_id'])
        return dict(job, completed=job['run_id'] != '0')
    class Pool(MainFirstPool):
        expected_main = 256
        already_closed_main = 0
        checkpoint = tmp_path/'reports/main.json'
        check_resources = staticmethod(lambda:True)
    (tmp_path/'reports').mkdir()
    monkeypatch.setattr(frozen, 'CapacityPolicy', ExtendedCapacityPolicy)
    monkeypatch.setattr(frozen.native, 'ROOT', tmp_path)
    monkeypatch.setattr(frozen.native, 'ready', lambda:True)
    monkeypatch.setattr(frozen.native, 'run_one', run)
    monkeypatch.setattr(frozen, 'set_gateway', lambda *args:None)
    monkeypatch.setattr(frozen, 'prepare', lambda _:({'jobs':jobs,'experiment':'test'},'hash',tmp_path,[],list(jobs)))
    monkeypatch.setattr(sys,'argv',['launcher',str(tmp_path/'plan.json'),'--concurrency','256'])
    frozen.main(pool_type=Pool)
    result = json.loads((tmp_path/'reports/plan_progress.json').read_text())
    assert result['finished_attempts'] == 257 and result['valid_runs'] == 256
    assert len({r['run_id'] for r in result['results']}) == 257
