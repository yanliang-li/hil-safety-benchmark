"""Run frozen plans at recorded 64/96/128 targets, with coordinated live relay limits."""
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
AMENDMENT = ROOT / 'experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json'
CONTROL = ROOT / 'reports/four-framework-capacity-control.json'
PLANS = {'main': 'main-plan-v1.json', 'hermes': 'hermes-plan-v1.json'}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_control(control, allowed_targets):
    total = control['aggregate_agent_target']
    weights = {'main': control['main_workers'], 'hermes': control['hermes_workers']}
    if type(total) is not int or total not in allowed_targets or not 1 <= total <= 128:
        raise ValueError('Aggregate concurrency is outside the recorded amendment')
    if any(type(v) is not int or v <= 0 for v in weights.values()) or sum(weights.values()) != total:
        raise ValueError('Cohort shares must sum to the aggregate concurrency')
    if control.get('gateway_max_inflight') != total:
        raise ValueError('Relay and agent targets must match')
    return total, weights


def choose_cohort(pending, active, weights):
    available = [name for name, queue in pending.items() if queue]
    # FIFO order within each frozen cohort is retained. Spare capacity goes to
    # remaining work as soon as a queue is exhausted, even during its final runs.
    return min(available, key=lambda name: active[name] / weights[name]) if available else None


def main():
    capacity = load('capacity_utils', 'scripts/schedule_api_capacity.py')
    original = load('frozen_launcher', 'scripts/api_experiment/launch.py')
    amendment = json.loads(AMENDMENT.read_text())
    amendment_digest = hashlib.sha256(AMENDMENT.read_bytes()).hexdigest()
    locks = []
    for name in PLANS:
        handle = (ROOT / f'reports/{name}-plan-v1.scheduler.lock').open('w')
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        locks.append(handle)
    for relative, expected in amendment['implementation_sha256'].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Amended implementation differs: ' + relative)
    reports, pending, runtimes = {}, {}, {}
    identities = set()
    for name, filename in PLANS.items():
        path = ROOT / 'experiments/api-multimodel-20260912' / filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != amendment['component_plan_sha256'][name]:
            raise ValueError('Frozen plan differs: ' + name)
        plan = json.loads(path.read_text())
        for relative, expected in plan['source_sha256'].items():
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
                raise ValueError('Frozen source differs: ' + relative)
        for case in plan['cases']:
            for relative, expected in case['files'].items():
                if hashlib.sha256((ROOT / 'data/cases' / case['case_id'] / relative).read_bytes()).hexdigest() != expected:
                    raise ValueError('Frozen case differs: ' + case['case_id'])
        for job in plan['jobs']:
            if job['run_id'] in identities:
                raise ValueError('Duplicate attempt across plans')
            identities.add(job['run_id'])
        image = subprocess.check_output(['docker', 'image', 'inspect', plan['image'], '--format', '{{.Id}}'], text=True).strip()
        if image != amendment['agent_image_ids'][name]:
            raise ValueError('Frozen agent image differs: ' + name)
        snapshot = ROOT / 'snapshots' / digest / 'scripts'
        source_folder = 'scripts/api_experiment' if name == 'main' else 'scripts/hermes_experiment'
        for relative, expected in plan['source_sha256'].items():
            if relative.startswith(source_folder + '/'):
                frozen = snapshot / Path(relative).relative_to(source_folder)
                if hashlib.sha256(frozen.read_bytes()).hexdigest() != expected:
                    raise ValueError('Frozen execution snapshot differs: ' + relative)
        completed, unstarted = capacity.completed_and_pending(plan['jobs'], ROOT)
        if any(row.get('image_id') != image for row in completed):
            raise ValueError('Closed attempt used an unexpected agent image')
        previous = json.loads((ROOT / f'reports/{name}-plan-v1_progress.json').read_text())
        reports[name] = dict(previous, results=completed, planned=len(plan['jobs']),
                             resumed_unix=time.time(), controller='unified-four-frameworks-ramp',
                             capacity_amendment_sha256=amendment_digest)
        pending[name] = deque(unstarted)
        runtimes[name] = {'runner_snapshot': str(snapshot), 'image_id': image}
    control = json.loads(CONTROL.read_text())
    total, weights = validate_control(control, amendment['authorized_aggregate_targets'])
    if control['gateway_name'] != amendment['gateway']['name']:
        raise ValueError('Unexpected relay configuration')
    actual_command = json.loads(subprocess.check_output(['docker', 'inspect', control['gateway_name'], '--format', '{{json .Config.Cmd}}'], text=True))
    if actual_command[actual_command.index('--max-inflight') + 1] != str(amendment['gateway']['maximum_inflight']):
        raise ValueError('Running relay capacity differs')
    original.GATEWAY = control['gateway_name']
    futures = {}
    active = Counter({name: 0 for name in PLANS})
    last_epoch = None
    with ThreadPoolExecutor(max_workers=128) as pool:
        while any(pending.values()) or futures:
            control = json.loads(CONTROL.read_text())
            total, weights = validate_control(control, amendment['authorized_aggregate_targets'])
            if control['gateway_name'] != original.GATEWAY:
                raise ValueError('Do not change the relay during active attempts')
            if (total, control['epoch']) != last_epoch:
                history_path = ROOT / 'reports/capacity-history.json'
                history = json.loads(history_path.read_text())
                history.append(dict(control, agent_concurrency=weights['main'],
                                    effective_unix=time.time(), closed_attempts=len(reports['main']['results'])))
                capacity.save(history_path, history)
                last_epoch = (total, control['epoch'])
            while len(futures) < total and capacity.headroom():
                name = choose_cohort(pending, active, weights)
                if name is None:
                    break
                job = dict(pending[name].popleft(), **runtimes[name],
                           capacity_epoch=control['epoch'], agent_concurrency_target=total,
                           aggregate_concurrency_limit=total, scheduler_cohort=name,
                           gateway_max_inflight=control['gateway_max_inflight'],
                           capacity_amendment_sha256=amendment_digest)
                futures[pool.submit(original.run_one, job)] = (name, job['run_id'])
                active[name] += 1
            for name, report in reports.items():
                report.update(active_attempts=active[name], concurrency=weights[name],
                              aggregate_active_attempts=len(futures), aggregate_concurrency_limit=total,
                              capacity_epoch=control['epoch'], checked_unix=time.time(),
                              resource_pause=not capacity.headroom(), waiting_for_shared_slots=False)
                if len(report['results']) == report['planned']:
                    report.setdefault('finished_unix', time.time())
                capacity.save(ROOT / f'reports/{name}-plan-v1_progress.json', report)
            capacity.save(ROOT / 'reports/unified-plan-v1_progress.json', {
                'checked_unix': time.time(), 'aggregate_concurrency_limit': total,
                'active_attempts': len(futures), 'active_by_cohort': dict(active),
                'finished_attempts': sum(len(r['results']) for r in reports.values()),
                'planned': sum(r['planned'] for r in reports.values()),
                'queued_by_cohort': {name: len(q) for name, q in pending.items()},
                'capacity_epoch': control['epoch'], 'resource_pause': not capacity.headroom()})
            if not futures:
                time.sleep(2)
                continue
            done, _ = wait(futures, timeout=2, return_when=FIRST_COMPLETED)
            for future in done:
                name, run_id = futures.pop(future)
                active[name] -= 1
                result = future.result()
                if result['run_id'] != run_id:
                    raise ValueError('Finished attempt identity differs')
                if not (ROOT / 'runs' / result['stage'] / run_id / 'attempt_status.json').exists():
                    raise ValueError('Closed attempt lacks its durable status')
                reports[name]['results'].append(result)
                capacity.save(ROOT / f'reports/{name}-plan-v1_progress.json', reports[name])
                print(json.dumps({k: v for k, v in result.items() if k != 'docker_state'}), flush=True)
    for name, report in reports.items():
        report.update(finished_unix=report.get('finished_unix', time.time()), active_attempts=0,
                      aggregate_active_attempts=0)
        capacity.save(ROOT / f'reports/{name}-plan-v1_progress.json', report)
    capacity.save(ROOT / 'reports/unified-plan-v1_progress.json', {
        'finished_unix': time.time(), 'active_attempts': 0,
        'finished_attempts': sum(len(r['results']) for r in reports.values()),
        'planned': sum(r['planned'] for r in reports.values()), 'aggregate_concurrency_limit': total})


if __name__ == '__main__':
    main()
