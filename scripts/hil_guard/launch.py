"""Run a frozen HIL comparison with fresh native containers and bounded load."""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
GATEWAY = 'hil-api-gateway-capacity-ramp-20260912'
NETWORK = 'hil-api-internal-20260912'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def ready():
    mem = int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:'))) / 1024**2
    return (mem >= 64 and shutil.disk_usage(ROOT).free >= 30 * 1024**3
            and os.getloadavg()[0] < .75 * os.cpu_count()
            and not (ROOT / 'STOP_NEW_SAIL').exists())


def run_one(job, snapshot):
    folder = ROOT / 'runs' / job['stage'] / job['run_id']
    status = folder / 'attempt_status.json'
    if status.exists():
        return json.loads(status.read_text())
    folder.mkdir(parents=True, exist_ok=True)
    registration = ROOT / 'registry' / (job['run_id'] + '.json')
    if registration.exists():
        raise RuntimeError('Registered unfinished attempt cannot be retried: ' + job['run_id'])
    save(registration, {'model': job['model'], 'max_requests': 48, 'purpose': job['stage'], 'agent': job['agent']})
    if job['condition'] != 'prompt_guard_v1':
        save(ROOT / 'registry' / (job['run_id'] + '_guard.json'),
             {'model': 'deepseek-v4-flash', 'max_requests': 24, 'purpose': job['stage'], 'agent': 'sail-reviewer'})
    save(folder / 'job.json', job)
    result = dict(job, started_unix=time.time(), completed=False)
    uid = f'{os.getuid()}:{os.getgid()}'
    command = ['docker', 'run', '--name', job['run_id'], '--label', 'org.hilbench.experiment=sail-20260913',
        '--network', NETWORK, '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
        '--memory', '1536m', '--memory-swap', '1536m', '--cpus', '1', '--pids-limit', '160', '--user', uid,
        '--tmpfs', '/tmp:rw,nosuid,nodev,size=512m',
        '--tmpfs', f'/home/benchmark:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}',
        '--tmpfs', f'/home/node:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}',
        '--mount', f'type=bind,src={ROOT/"data/cases"/job["case_id"]},dst=/case,readonly',
        '--mount', f'type=bind,src={folder},dst=/run-output',
        '--mount', f'type=bind,src={snapshot/"method"},dst=/opt/hil-method,readonly',
        '--mount', f'type=bind,src={snapshot/"frozen-runners"},dst=/opt/frozen-runners,readonly',
        '--env', 'PYTHONPATH=/opt/hil-method:/opt/hilbench-src/src',
        '--entrypoint', '/opt/hilbench-venv/bin/python', job['image_id'],
        '-m', 'hil_guard.run_case', '--agent', job['agent'], '--model', job['model'],
        '--condition', job['condition'], '--run-id', job['run_id'], '--repeat', str(job['repeat']),
        '--timeout', str(job['timeout']), '--base-url', f'http://{GATEWAY}:8080/r/{job["run_id"]}/v1']
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=job['timeout'] + 90)
        (folder / 'container_stdout.log').write_text(process.stdout)
        (folder / 'container_stderr.log').write_text(process.stderr)
        result['container_returncode'] = process.returncode
        meta_path = folder / 'run_metadata.json'
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
            result.update(completed=meta.get('scorable', False) and process.returncode == 0,
                          guard_invalid=meta.get('guard_invalid', False), event_count=meta.get('benchmark_event_count', 0))
        state = subprocess.run(['docker', 'inspect', job['run_id'], '--format', '{{json .State}}'],
            capture_output=True, text=True, timeout=20)
        if state.returncode == 0:
            docker = json.loads(state.stdout)
            save(folder / 'docker_state.json', docker)
            result['oom_killed'] = docker.get('OOMKilled', False)
            if result['oom_killed']:
                result['completed'] = False
    except Exception as error:
        result['scheduler_failure'] = type(error).__name__
    finally:
        try:
            subprocess.run(['docker', 'rm', '-f', job['run_id']], capture_output=True, timeout=30)
        except subprocess.TimeoutExpired:
            result['container_cleanup_timeout'] = True
    result['finished_unix'] = time.time()
    save(status, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('plan', type=Path)
    parser.add_argument('--concurrency', type=int, default=32)
    args = parser.parse_args()
    if not 1 <= args.concurrency <= 96:
        raise ValueError('Agent concurrency must be between 1 and 96')
    plan = json.loads(args.plan.read_text())
    digest = hashlib.sha256(args.plan.read_bytes()).hexdigest()
    lock = (ROOT / 'reports' / (args.plan.stem + '.lock')).open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    for relative, expected in plan['source_sha256'].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source mismatch: ' + relative)
    for case in plan['cases']:
        for relative, expected in case['files'].items():
            if hashlib.sha256((ROOT / 'data/cases' / case['case_id'] / relative).read_bytes()).hexdigest() != expected:
                raise ValueError('Frozen case mismatch: ' + case['case_id'])
    if len({j['run_id'] for j in plan['jobs']}) != len(plan['jobs']):
        raise ValueError('Duplicate run IDs')
    snapshot = ROOT / 'snapshots' / digest
    if not snapshot.exists():
        (snapshot / 'method').mkdir(parents=True)
        shutil.copytree(ROOT / 'scripts/hil_guard', snapshot / 'method/hil_guard', ignore=shutil.ignore_patterns('__pycache__'))
        (snapshot / 'frozen-runners').mkdir()
        shutil.copy2(ROOT / 'scripts/api_experiment/run_case.py', snapshot / 'frozen-runners/run_case.py')
        shutil.copy2(ROOT / 'scripts/hermes_experiment/run_case.py', snapshot / 'frozen-runners/hermes_run_case.py')
    results, queue = [], []
    for job in plan['jobs']:
        status = ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json'
        if status.exists():
            results.append(json.loads(status.read_text()))
        else:
            if (ROOT / 'registry' / (job['run_id'] + '.json')).exists():
                raise RuntimeError('Refusing automatic retry of an unfinished registration')
            queue.append(job)
    progress = ROOT / 'reports' / (args.plan.stem + '_progress.json')
    report = {'plan_sha256': digest, 'started_unix': time.time(), 'planned': len(plan['jobs']),
        'concurrency': args.concurrency, 'results': results, 'active': 0, 'queued': len(queue)}
    pool = ThreadPoolExecutor(max_workers=args.concurrency)
    active = {}
    while queue or active:
        can_launch = ready()
        while can_launch and queue and len(active) < args.concurrency:
            job = queue.pop(0)
            active[pool.submit(run_one, job, snapshot)] = job
        done, _ = wait(active, timeout=3, return_when=FIRST_COMPLETED) if active else (set(), set())
        for future in done:
            job = active.pop(future)
            try:
                result = future.result()
            except Exception as error:
                result = dict(job, completed=False, finished_unix=time.time(), scheduler_failure=type(error).__name__)
                save(ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json', result)
            results.append(result)
        report.update(active=len(active), queued=len(queue), finished_attempts=len(results),
                      valid_runs=sum(x.get('completed', False) for x in results),
                      checked_unix=time.time(), resource_pause=not can_launch)
        save(progress, report)
        if done:
            print(json.dumps({k:v for k,v in report.items() if k != 'results'}), flush=True)
        if not active and queue:
            time.sleep(3)
    pool.shutdown()
    report['finished_unix'] = time.time()
    save(progress, report)


if __name__ == '__main__':
    main()
