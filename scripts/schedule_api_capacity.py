"""Resume the frozen attempt list with an explicitly amended, adjustable capacity.

Per-attempt execution remains the hash-verified original run_one implementation.
Change reports/capacity-control.json atomically to adjust future launches.
"""
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

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'experiments/api-multimodel-20260912/main-plan-v1.json'
PROGRESS = ROOT / 'reports/main-plan-v1_progress.json'
CONTROL = ROOT / 'reports/capacity-control.json'
HISTORY = ROOT / 'reports/capacity-history.json'


def save(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    temp.replace(path)


def completed_and_pending(jobs, root):
    completed, pending = [], []
    seen = set()
    for job in jobs:
        run_id = job['run_id']
        if run_id in seen:
            raise ValueError('Duplicate attempt ID')
        seen.add(run_id)
        status = root / 'runs' / job['stage'] / run_id / 'attempt_status.json'
        if status.exists():
            result = json.loads(status.read_text())
            for field in ['run_id', 'agent', 'model', 'condition', 'repeat', 'case_id']:
                if result[field] != job[field]:
                    raise ValueError('Existing attempt identity differs: ' + run_id)
            completed.append(result)
        elif (root / 'registry' / (run_id + '.json')).exists():
            raise ValueError('Registered attempt has not closed; drain first: ' + run_id)
        else:
            pending.append(job)
    return completed, pending


def capacity():
    control = json.loads(CONTROL.read_text())
    target = control['agent_concurrency']
    if not isinstance(target, int) or not 1 <= target <= 48:
        raise ValueError('Agent capacity must be 1..48')
    if not 1 <= control['gateway_max_inflight'] <= 64:
        raise ValueError('Unexpected gateway capacity')
    return control


def headroom():
    mem = int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines()
                   if l.startswith('MemAvailable:'))) * 1024
    return (mem >= 64 * 1024**3 and shutil.disk_usage(ROOT).free >= 30 * 1024**3
            and os.getloadavg()[0] < .75 * os.cpu_count()
            and not (ROOT / 'STOP_NEW_RUNS').exists())


def main():
    lock = (ROOT / 'reports/main-plan-v1.scheduler.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    plan = json.loads(PLAN.read_text())
    digest = hashlib.sha256(PLAN.read_bytes()).hexdigest()
    for rel, expected in plan['source_sha256'].items():
        if hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source differs: ' + rel)
    for case in plan['cases']:
        for rel, expected in case['files'].items():
            if hashlib.sha256((ROOT / 'data/cases' / case['case_id'] / rel).read_bytes()).hexdigest() != expected:
                raise ValueError('Frozen case differs: ' + case['case_id'])
    completed, pending = completed_and_pending(plan['jobs'], ROOT)
    snapshot = ROOT / 'snapshots' / digest / 'scripts'
    if not snapshot.exists():
        raise ValueError('Original frozen runner snapshot is absent')
    image_id = subprocess.check_output(['docker', 'image', 'inspect', plan['image'], '--format', '{{.Id}}'], text=True).strip()
    if completed and any(r.get('image_id') != image_id for r in completed):
        raise ValueError('Original runtime image differs')
    spec = importlib.util.spec_from_file_location('frozen_launch', ROOT / 'scripts/api_experiment/launch.py')
    launch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launch)
    previous = json.loads(PROGRESS.read_text())
    report = {'plan_sha256': digest, 'started_unix': previous['started_unix'],
              'resumed_unix': time.time(), 'planned': len(plan['jobs']),
              'results': completed, 'capacity_amendment': 'capacity-amendment-v1.json'}
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else []
    index, futures, last_epoch = 0, {}, None
    with ThreadPoolExecutor(max_workers=48) as pool:
        while index < len(pending) or futures:
            control = capacity()
            epoch = (control['agent_concurrency'], control['epoch'])
            if epoch != last_epoch:
                history.append(dict(control, effective_unix=time.time(), closed_attempts=len(report['results'])))
                save(HISTORY, history)
                last_epoch = epoch
            launch.GATEWAY = control['gateway_name']
            while index < len(pending) and len(futures) < control['agent_concurrency'] and headroom():
                job = dict(pending[index], runner_snapshot=str(snapshot), image_id=image_id,
                           capacity_epoch=control['epoch'], agent_concurrency_target=control['agent_concurrency'],
                           gateway_max_inflight=control['gateway_max_inflight'])
                futures[pool.submit(launch.run_one, job)] = job['run_id']
                index += 1
            report.update(concurrency=control['agent_concurrency'], active_attempts=len(futures),
                          capacity_epoch=control['epoch'], checked_unix=time.time(), resource_pause=not headroom())
            save(PROGRESS, report)
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
            save(PROGRESS, report)
    report.update(finished_unix=time.time(), active_attempts=0)
    save(PROGRESS, report)


if __name__ == '__main__':
    main()
