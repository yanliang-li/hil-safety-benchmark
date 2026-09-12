"""Bounded Docker scheduler. Immutable attempt directories; failures remain failures."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
IMAGE = 'hil-api-harnesses:20260912-v1'
LABEL = 'org.hilbench.experiment=api-20260912'
NETWORK = 'hil-api-internal-20260912'
GATEWAY = 'hil-api-gateway-20260912'


def save(path, obj):
    temp = path.with_suffix('.tmp'); temp.write_text(json.dumps(obj, indent=2)+'\n'); temp.replace(path)


def run_one(job):
    run_id = job['run_id']
    folder = ROOT/'runs'/job['stage']/run_id
    status = folder/'attempt_status.json'
    if status.exists(): return json.loads(status.read_text())
    folder.mkdir(parents=True, exist_ok=True)
    if (ROOT/'registry'/f'{run_id}.json').exists():
        return dict(job, completed=False, scheduler_failure='incomplete prior attempt; create a new attempt ID')
    while True:
        mem = int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
        if mem >= 24*1024**3 and shutil.disk_usage(ROOT).free >= 30*1024**3 and not (ROOT/'STOP_NEW_RUNS').exists():
            break
        time.sleep(15)
    save(ROOT/'registry'/f'{run_id}.json', {'model':job['model'], 'max_requests':48, 'purpose':job['stage'], 'agent':job['agent']})
    save(folder/'job.json', job)
    command = ['docker','run','--name',run_id,'--label',LABEL,'--network',NETWORK,'--read-only',
        '--cap-drop','ALL','--security-opt','no-new-privileges','--memory','1536m','--memory-swap','1536m',
        '--cpus','1','--pids-limit','160','--user',f'{os.getuid()}:{os.getgid()}',
        '--tmpfs','/tmp:rw,nosuid,nodev,size=512m',
        '--tmpfs',f'/home/benchmark:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}',
        '--tmpfs',f'/home/node:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}',
        '--mount',f'type=bind,src={ROOT/"data/cases"/job["case_id"]},dst=/case,readonly',
        '--mount',f'type=bind,src={folder},dst=/run-output',
        '--mount',f'type=bind,src={job.get("runner_snapshot", str(ROOT/"scripts/api_experiment"))},dst=/opt/api-experiment,readonly',
        '--entrypoint','python',job.get('image_id', IMAGE),'/opt/api-experiment/run_case.py',
        '--agent',job['agent'],'--model',job['model'],'--condition',job['condition'],
        '--run-id',run_id,'--repeat',str(job['repeat']),'--timeout',str(job.get('timeout',600)),
        '--base-url',f'http://{GATEWAY}:8080/r/{run_id}/v1']
    result = dict(job, started_unix=time.time(), completed=False)
    try:
        p=subprocess.run(command, text=True, capture_output=True, timeout=job.get('timeout',600)+90)
        (folder/'container_stdout.log').write_text(p.stdout); (folder/'container_stderr.log').write_text(p.stderr)
        result['container_returncode']=p.returncode
        meta=folder/'run_metadata.json'
        if meta.exists():
            metadata=json.loads(meta.read_text()); result['completed']=metadata.get('scorable',False)
            result['event_count']=metadata.get('benchmark_event_count',0)
        state=subprocess.run(['docker','inspect',run_id,'--format','{{json .State}}'],capture_output=True,text=True,timeout=20)
        if state.returncode==0:
            result['docker_state']=json.loads(state.stdout)
            save(folder/'docker_state.json',result['docker_state'])
            if result['docker_state'].get('OOMKilled') or p.returncode != 0:
                result['completed']=False
    except Exception as e: result['scheduler_failure']=type(e).__name__
    finally:
        subprocess.run(['docker','rm','-f',run_id],capture_output=True,timeout=30)
    result['finished_unix']=time.time(); save(status,result)
    return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('plan',type=Path)
    parser.add_argument('--concurrency',type=int,default=2); args=parser.parse_args()
    if not 1<=args.concurrency<=8: raise ValueError('Concurrency must be 1..8')
    plan=json.loads(args.plan.read_text()); jobs=plan['jobs']
    lock=(ROOT/'reports'/f'{args.plan.stem}.scheduler.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
    if plan.get('source_sha256'):
        for relative,expected in plan['source_sha256'].items():
            if hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()!=expected:
                raise ValueError('Frozen source differs: '+relative)
        for case in plan['cases']:
            for relative,expected in case['files'].items():
                if hashlib.sha256((ROOT/'data/cases'/case['case_id']/relative).read_bytes()).hexdigest()!=expected:
                    raise ValueError('Frozen case differs: '+case['case_id'])
        digest=hashlib.sha256(args.plan.read_bytes()).hexdigest()
        snapshot=ROOT/'snapshots'/digest/'scripts'
        if not snapshot.exists(): shutil.copytree(ROOT/'scripts/api_experiment',snapshot,ignore=shutil.ignore_patterns('__pycache__'))
        image_id=subprocess.check_output(['docker','image','inspect',IMAGE,'--format','{{.Id}}'],text=True).strip()
        for job in jobs:
            job['runner_snapshot']=str(snapshot);job['image_id']=image_id
    if len({j['run_id'] for j in jobs})!=len(jobs): raise ValueError('Duplicate attempt IDs')
    report={'plan_sha256':hashlib.sha256(args.plan.read_bytes()).hexdigest(),'started_unix':time.time(),
            'concurrency':args.concurrency,'planned':len(jobs),'results':[]}
    dest=ROOT/'reports'/f'{args.plan.stem}_progress.json'; save(dest,report)
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures=[pool.submit(run_one,j) for j in jobs]
        for future in as_completed(futures):
            r=future.result(); report['results'].append(r); save(dest,report)
            print(json.dumps({k:v for k,v in r.items() if k!='docker_state'}),flush=True)
    report['finished_unix']=time.time(); save(dest,report)


if __name__=='__main__': main()
