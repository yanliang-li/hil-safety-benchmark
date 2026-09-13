import hashlib
import json
from pathlib import Path
import sys
import threading

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from sail_v4_capacity import CapacityPolicy, prepare, native
import sail_v4_capacity as scheduler
from launch_sail_v4_sequential import MainFirstPool


def window(requests=100, errors=0):
    return {'requests': requests, 'errors': errors, 'error_rate': errors / requests, 'elapsed_s': 300}


def test_128_requires_two_healthy_windows_and_memory_headroom():
    p = CapacityPolicy()
    p.observe(window(), True, 150, 96, 300)
    assert p.target == 96
    p.observe(window(), True, 100, 96, 600)
    assert p.target == 96
    p.observe(window(), True, 150, 96, 900)
    assert p.target == 128


def test_128_without_throughput_gain_backs_off_and_cools_down():
    p = CapacityPolicy()
    for now in (300, 600):
        p.observe(window(), True, 150, 96, now)
    assert p.target == 128
    p.observe(window(), True, 150, 128, 900)
    assert p.target == 128
    assert p.observe(window(), True, 150, 128, 1200) == 'no_measured_throughput_gain_backoff'
    assert p.target == 96
    for now in (1500, 1800):
        p.observe(window(140), True, 150, 96, now)
    assert p.target == 96


def test_errors_back_off_and_successful_trial_retains_128():
    p = CapacityPolicy()
    for now in (300, 600):
        p.observe(window(), True, 150, 96, now)
    for now in (900, 1200):
        p.observe(window(120), True, 150, 128, now)
    assert p.target == 128
    p.observe(window(errors=5), True, 150, 128, 1500)
    assert p.target == 96
    p.observe(window(), False, 60, 96, 1800)
    assert p.target == 64


def test_resume_retains_failed_attempt_and_refuses_unfinished_registration(tmp_path, monkeypatch):
    monkeypatch.setattr(native, 'ROOT', tmp_path)
    job = {'run_id': 'one', 'stage': 'test', 'condition': 'sail_v4'}
    data = {'execution_order': 'main_then_ablation', 'source_sha256': {}, 'cases': [], 'jobs': [job]}
    plan = tmp_path / 'plan.json'
    plan.write_text(json.dumps(data))
    digest = hashlib.sha256(plan.read_bytes()).hexdigest()
    (tmp_path / 'snapshots' / digest).mkdir(parents=True)
    status = tmp_path / 'runs/test/one/attempt_status.json'
    status.parent.mkdir(parents=True)
    status.write_text(json.dumps(dict(job, completed=False)))
    result = prepare(plan)
    assert len(result[3]) == 1 and not result[3][0]['completed'] and not result[4]
    status.unlink()
    (tmp_path / 'registry').mkdir()
    (tmp_path / 'registry/one.json').write_text('{}')
    with pytest.raises(RuntimeError, match='unfinished registration'):
        prepare(plan)


def test_scheduler_runs_128_and_accounts_all_main_before_ablation(tmp_path, monkeypatch):
    jobs = [dict(run_id=str(i), stage='test', condition='sail_v4') for i in range(128)]
    jobs.append(dict(run_id='ablation', stage='test', condition='sail_v4_no_human'))
    barrier = threading.Barrier(128)
    completed = []
    def run(job, snapshot):
        if job['condition'] == 'sail_v4_no_human':
            assert len(completed) == 128
            progress = json.loads((tmp_path / 'reports/plan_progress.json').read_text())
            assert progress['finished_attempts'] == 128
        else:
            barrier.wait(timeout=5)
            completed.append(job['run_id'])
        return dict(job, completed=job['run_id'] != '0')
    class Pool(MainFirstPool):
        expected_main = 128
        already_closed_main = 0
        checkpoint = tmp_path / 'reports/main.json'
        check_resources = staticmethod(lambda: True)
    (tmp_path / 'reports').mkdir()
    monkeypatch.setattr(native, 'ROOT', tmp_path)
    monkeypatch.setattr(native, 'ready', lambda: True)
    monkeypatch.setattr(native, 'run_one', run)
    monkeypatch.setattr(scheduler, 'set_gateway', lambda *args: None)
    monkeypatch.setattr(scheduler, 'prepare', lambda _: (
        {'jobs': list(jobs), 'experiment': 'test'}, 'hash', tmp_path, [], list(jobs)))
    monkeypatch.setattr(sys, 'argv', ['launcher', str(tmp_path / 'plan.json'), '--concurrency', '128'])
    scheduler.main(pool_type=Pool)
    progress = json.loads((tmp_path / 'reports/plan_progress.json').read_text())
    assert progress['finished_attempts'] == 129 and progress['valid_runs'] == 128
    assert len({r['run_id'] for r in progress['results']}) == 129
    assert progress['finished_unix'] and Pool.checkpoint.exists()
