"""Run Hermes in eight reserved slots, sharing a total limit of 32 agents."""
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    capacity = load('capacity_utils', 'scripts/schedule_api_capacity.py')
    original = load('original_launcher', 'scripts/api_experiment/launch.py')
    plan_path = ROOT / 'experiments/api-multimodel-20260912/hermes-plan-v1.json'
    plan = json.loads(plan_path.read_text())
    lock = (ROOT / 'reports/hermes-plan-v1.scheduler.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    for rel, digest in plan['source_sha256'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != digest:
            raise ValueError('Frozen source differs: ' + rel)
    for case in plan['cases']:
        for rel, digest in case['files'].items():
            if hashlib.sha256((ROOT / 'data/cases' / case['case_id'] / rel).read_bytes()).hexdigest() != digest:
                raise ValueError('Frozen case differs: ' + case['case_id'])
    image = subprocess.check_output(['docker', 'image', 'inspect', plan['image'], '--format', '{{.Id}}'], text=True).strip()
    if image != plan['image_id']:
        raise ValueError('Hermes image differs')
    completed, pending = capacity.completed_and_pending(plan['jobs'], ROOT)
    digest = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    snapshot = ROOT / 'snapshots' / digest / 'scripts'
    if not snapshot.exists():
        shutil.copytree(ROOT / 'scripts/hermes_experiment', snapshot,
                        ignore=shutil.ignore_patterns('__pycache__'))
    dest = ROOT / 'reports/hermes-plan-v1_progress.json'
    report = {'plan_sha256': digest, 'started_unix': time.time(), 'planned': len(plan['jobs']),
              'results': completed, 'aggregate_concurrency_limit': 32}
    index, futures = 0, {}
    with ThreadPoolExecutor(max_workers=32) as pool:
        while index < len(pending) or futures:
            main_progress = json.loads((ROOT / 'reports/main-plan-v1_progress.json').read_text())
            other_done = bool(main_progress.get('finished_unix'))
            control = json.loads((ROOT / 'reports/capacity-control.json').read_text())
            target = 32 if other_done else 8
            permitted = other_done or control['agent_concurrency'] <= 24
            original.GATEWAY = control['gateway_name']
            while index < len(pending) and len(futures) < target and permitted and capacity.headroom():
                job = dict(pending[index], runner_snapshot=str(snapshot), image_id=image,
                    capacity_epoch='hermes-32' if other_done else 'four-frameworks-32',
                    agent_concurrency_target=target, aggregate_concurrency_limit=32,
                    gateway_max_inflight=control['gateway_max_inflight'])
                futures[pool.submit(original.run_one, job)] = job['run_id']
                index += 1
            report.update(concurrency=target, active_attempts=len(futures), checked_unix=time.time(),
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
    # If Hermes finishes first, release its reserved slots to the remaining jobs.
    main_progress = json.loads((ROOT / 'reports/main-plan-v1_progress.json').read_text())
    if not main_progress.get('finished_unix'):
        control_path = ROOT / 'reports/capacity-control.json'
        control = json.loads(control_path.read_text())
        if control['agent_concurrency'] == 24:
            control.update(agent_concurrency=32, epoch='capacity-32-hermes-complete')
            capacity.save(control_path, control)


if __name__ == '__main__':
    main()
