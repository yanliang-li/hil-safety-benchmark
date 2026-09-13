"""Scheduling-only capacity amendment; reuse frozen native episode execution."""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import time

from hil_guard_v4 import launch as native


class CapacityPolicy:
    levels = (32, 64, 96, 128)

    def __init__(self, initial=96, maximum=128):
        if initial not in self.levels or maximum not in self.levels or initial > maximum:
            raise ValueError('Unsupported capacity')
        self.target, self.maximum = initial, maximum
        self.healthy = []
        self.trial = []
        self.baseline = None
        self.retry_128_after = 0

    def observe(self, window, resource_ready, memory_gib, active, now):
        requests = window['requests']
        rate = (requests - window['errors']) / max(window['elapsed_s'], 1)
        if not resource_ready or (requests and window['error_rate'] >= .05):
            previous = self.target
            self.target = self.levels[max(0, self.levels.index(self.target) - 1)]
            self.healthy.clear()
            self.trial.clear()
            if previous == 128:
                self.retry_128_after = now + 1800
            return 'resource_or_api_backoff'
        if requests < 50:
            return 'insufficient_requests'
        if self.target == 128 and self.baseline is not None:
            self.trial.append(rate)
            if len(self.trial) < 2:
                return 'measuring_128_throughput'
            if sum(self.trial[-2:]) / 2 < self.baseline * 1.05:
                self.target = 96
                self.retry_128_after = now + 1800
                self.healthy.clear()
                self.trial.clear()
                self.baseline = None
                return 'no_measured_throughput_gain_backoff'
            self.baseline = None
            self.trial.clear()
            return 'retain_128_measured_gain'
        self.healthy.append(rate)
        if len(self.healthy) < 2 or self.target == self.maximum:
            return 'hold'
        candidate = self.levels[self.levels.index(self.target) + 1]
        if candidate > self.maximum or (candidate == 128 and now < self.retry_128_after):
            return 'hold'
        # Reserve 64 GiB for the host, plus the full 1.5 GiB container limit
        # for each additional simultaneous episode at the proposed target.
        if memory_gib < 64 + max(0, candidate - active) * 1.5:
            return 'insufficient_ramp_memory_headroom'
        if candidate == 128:
            self.baseline = sum(self.healthy[-2:]) / 2
            self.trial.clear()
        self.target = candidate
        self.healthy.clear()
        return 'healthy_capacity_increase'


def available_memory():
    return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines()
                    if x.startswith('MemAvailable:'))) / 1024**2


def set_gateway(target, stage):
    path = native.ROOT / 'reports/four-framework-capacity-control.json'
    value = json.loads(path.read_text())
    if value.get('gateway_capacity_ceiling') != 128:
        raise ValueError('Gateway does not have the audited 128-request ceiling')
    value.update(gateway_max_inflight=max(64, target), aggregate_agent_target=target,
                 active_experiment=stage, effective_unix=time.time(),
                 capacity_authorization='experiments/sail-v4-20260913/capacity-amendment-v1.json')
    native.save(path, value)


def prepare(plan_path):
    plan = json.loads(plan_path.read_text())
    if plan.get('analysis_only') or plan.get('execution_order') != 'main_then_ablation':
        raise ValueError('A frozen main-then-ablation plan is required')
    for relative, expected in plan['source_sha256'].items():
        if hashlib.sha256((native.ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source mismatch: ' + relative)
    for case in plan['cases']:
        for relative, expected in case['files'].items():
            path = native.ROOT / case.get('case_root', 'data/cases') / case['case_id'] / relative
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError('Frozen case mismatch: ' + case['case_id'])
    if len({j['run_id'] for j in plan['jobs']}) != len(plan['jobs']):
        raise ValueError('Duplicate run IDs')
    digest = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    snapshot = native.ROOT / 'snapshots' / digest
    if not snapshot.exists():
        (snapshot / 'method').mkdir(parents=True)
        for package in ('hil_guard_v3', 'hil_guard_v4'):
            shutil.copytree(native.ROOT / 'scripts' / package, snapshot / 'method' / package,
                            ignore=shutil.ignore_patterns('__pycache__'))
        (snapshot / 'frozen-runners').mkdir()
        shutil.copy2(native.ROOT / 'scripts/api_experiment/run_case.py', snapshot / 'frozen-runners/run_case.py')
        shutil.copy2(native.ROOT / 'scripts/hermes_experiment/run_case.py', snapshot / 'frozen-runners/hermes_run_case.py')
    results, queue = [], []
    for job in plan['jobs']:
        status = native.ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json'
        if status.exists():
            results.append(json.loads(status.read_text()))
        elif (native.ROOT / 'registry' / (job['run_id'] + '.json')).exists():
            raise RuntimeError('Refusing automatic retry of an unfinished registration')
        else:
            queue.append(job)
    return plan, digest, snapshot, results, queue


def main(pool_type=ThreadPoolExecutor):
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    parser.add_argument('--concurrency', type=int, default=96)
    parser.add_argument('--adaptive', action='store_true')
    args = parser.parse_args()
    policy = CapacityPolicy(args.concurrency)
    lock = (native.ROOT / 'reports' / (args.plan.stem + '.lock')).open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    plan, digest, snapshot, results, queue = prepare(args.plan)
    progress = native.ROOT / 'reports' / (args.plan.stem + '_progress.json')
    previous = json.loads(progress.read_text()) if progress.exists() else {}
    report = {'plan_sha256': digest, 'started_unix': previous.get('started_unix', time.time()),
              'planned': len(plan['jobs']), 'concurrency': policy.target, 'results': results,
              'active': 0, 'queued': len(queue), 'capacity_ceiling': policy.maximum}
    history_path = native.ROOT / 'reports' / (args.plan.stem + '_capacity.json')
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    set_gateway(policy.target, plan['experiment'])
    history.append({'time_unix': time.time(), 'target': policy.target, 'reason': 'authorized_start'})
    native.save(history_path, history)
    capacity_at = time.time()
    active = {}
    with pool_type(max_workers=policy.maximum if args.adaptive else policy.target) as pool:
        while queue or active:
            now = time.time()
            if args.adaptive and now - capacity_at >= 300:
                window = native.api_window(plan['jobs'], capacity_at)
                window['elapsed_s'] = now - capacity_at
                resources, memory = native.ready(), available_memory()
                reason = policy.observe(window, resources, memory, len(active), now)
                set_gateway(policy.target, plan['experiment'])
                history.append(dict(window, time_unix=now, target=policy.target, reason=reason,
                                    resource_ready=resources, available_memory_gib=memory,
                                    active=len(active), finished_attempts=len(results)))
                native.save(history_path, history)
                capacity_at = now
            can_launch = native.ready()
            while can_launch and queue and len(active) < policy.target:
                # Drain and account for all main futures before submitting
                # an ablation. MainFirstPool additionally verifies this barrier.
                if queue[0]['condition'] == 'sail_v4_no_human' and any(
                        j['condition'] != 'sail_v4_no_human' for j in active.values()):
                    break
                job = queue.pop(0)
                active[pool.submit(native.run_one, job, snapshot)] = job
                can_launch = native.ready()
            done, _ = wait(active, timeout=3, return_when=FIRST_COMPLETED) if active else (set(), set())
            for future in done:
                job = active.pop(future)
                try:
                    result = future.result()
                except Exception as error:
                    result = dict(job, completed=False, finished_unix=time.time(),
                                  scheduler_failure=type(error).__name__)
                    native.save(native.ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json', result)
                results.append(result)
            report.update(active=len(active), queued=len(queue), finished_attempts=len(results),
                          valid_runs=sum(x.get('completed', False) for x in results),
                          checked_unix=time.time(), resource_pause=not can_launch,
                          concurrency=policy.target)
            native.save(progress, report)
            if done:
                print(json.dumps({k:v for k,v in report.items() if k != 'results'}), flush=True)
            if not active and queue:
                time.sleep(3)
    report['finished_unix'] = time.time()
    native.save(progress, report)
