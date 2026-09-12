"""Resume the frozen Hermes cases under an explicit aggregate capacity amendment."""
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def allocation(control, main_done, main_target):
    total = control['aggregate_agent_target']
    main, hermes = control['main_workers'], control['hermes_workers']
    if not (isinstance(total, int) and 1 <= total <= 48 and main >= 1 and hermes >= 1 and main + hermes == total):
        raise ValueError('Invalid aggregate allocation')
    return (total, True) if main_done else (hermes, main_target <= main)


def main():
    capacity = load('capacity_utils', 'scripts/schedule_api_capacity.py')
    original = load('original_launcher', 'scripts/api_experiment/launch.py')
    plan_path = ROOT / 'experiments/api-multimodel-20260912/hermes-plan-v1.json'
    amendment_path = ROOT / 'experiments/api-multimodel-20260912/four-framework-capacity-amendment-v1.json'
    plan, amendment = json.loads(plan_path.read_text()), json.loads(amendment_path.read_text())
    lock = (ROOT / 'reports/hermes-plan-v1.scheduler.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    for rel, digest in dict(plan['source_sha256'], **amendment['source_sha256']).items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != digest:
            raise ValueError('Frozen source differs: ' + rel)
    for case in plan['cases']:
        for rel, digest in case['files'].items():
            if hashlib.sha256((ROOT / 'data/cases' / case['case_id'] / rel).read_bytes()).hexdigest() != digest:
                raise ValueError('Frozen case differs: ' + case['case_id'])
    image = subprocess.check_output(['docker', 'image', 'inspect', plan['image'], '--format', '{{.Id}}'], text=True).strip()
    if image != plan['image_id']:
        raise ValueError('Hermes image differs')
    digest = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    if amendment['hermes_plan_sha256'] != digest:
        raise ValueError('Amendment refers to a different plan')
    snapshot = ROOT / 'snapshots' / digest / 'scripts'
    if hashlib.sha256((snapshot / 'run_case.py').read_bytes()).hexdigest() != plan['source_sha256']['scripts/hermes_experiment/run_case.py']:
        raise ValueError('Hermes execution snapshot differs')
    completed, pending = capacity.completed_and_pending(plan['jobs'], ROOT)
    dest = ROOT / 'reports/hermes-plan-v1_progress.json'
    prior = json.loads(dest.read_text())
    report = dict(prior, results=completed, resumed_unix=time.time(),
                  capacity_amendment_sha256=hashlib.sha256(amendment_path.read_bytes()).hexdigest())
    index, futures = 0, {}
    with ThreadPoolExecutor(max_workers=48) as pool:
        while index < len(pending) or futures:
            main_progress = json.loads((ROOT / 'reports/main-plan-v1_progress.json').read_text())
            other_done = bool(main_progress.get('finished_unix'))
            control = json.loads((ROOT / 'reports/capacity-control.json').read_text())
            shared = json.loads((ROOT / 'reports/four-framework-capacity-control.json').read_text())
            if shared['aggregate_agent_target'] not in amendment['authorized_aggregate_targets']:
                raise ValueError('Aggregate target is outside this amendment')
            target, permitted = allocation(shared, other_done, control['agent_concurrency'])
            original.GATEWAY = control['gateway_name']
            while index < len(pending) and len(futures) < target and permitted and capacity.headroom():
                job = dict(pending[index], runner_snapshot=str(snapshot), image_id=image,
                    capacity_epoch=shared['epoch'], agent_concurrency_target=target,
                    aggregate_concurrency_limit=shared['aggregate_agent_target'],
                    gateway_max_inflight=control['gateway_max_inflight'])
                futures[pool.submit(original.run_one, job)] = job['run_id']
                index += 1
            report.update(concurrency=target, active_attempts=len(futures), checked_unix=time.time(),
                          aggregate_concurrency_limit=shared['aggregate_agent_target'],
                          waiting_for_shared_slots=not permitted, resource_pause=not capacity.headroom())
            capacity.save(dest, report)
            if not futures:
                time.sleep(2)
                continue
            done, _ = wait(futures, timeout=2, return_when=FIRST_COMPLETED)
            for future in done:
                run_id = futures.pop(future)
                result = future.result()
                if result['run_id'] != run_id:
                    raise ValueError('Finished attempt identity differs')
                report['results'].append(result)
                print(json.dumps({k: v for k, v in result.items() if k != 'docker_state'}), flush=True)
            capacity.save(dest, report)
    report.update(finished_unix=time.time(), active_attempts=0)
    capacity.save(dest, report)
    main_progress = json.loads((ROOT / 'reports/main-plan-v1_progress.json').read_text())
    if not main_progress.get('finished_unix'):
        control_path = ROOT / 'reports/capacity-control.json'
        control = json.loads(control_path.read_text())
        shared = json.loads((ROOT / 'reports/four-framework-capacity-control.json').read_text())
        if control['agent_concurrency'] <= shared['main_workers']:
            control.update(agent_concurrency=shared['aggregate_agent_target'], epoch=shared['epoch'] + '-hermes-complete')
            capacity.save(control_path, control)


if __name__ == '__main__':
    main()
