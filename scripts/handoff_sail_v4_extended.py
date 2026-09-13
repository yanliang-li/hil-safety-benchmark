"""Drain-only transactional gateway/scheduler handoff; never retry episodes."""
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from launch_sail_v4_extended import verify_amendment
from hil_guard_v4.launch import ROOT, GATEWAY, NETWORK, save

CANDIDATE = 'hil-api-gateway-capacity256-20260913'
BACKUP = GATEWAY + '-before256'
STATE = ROOT / 'reports/sail4-capacity256-handoff.json'
PAUSE = ROOT / 'STOP_NEW_SAIL'
CONTROL = ROOT / 'reports/four-framework-capacity-control.json'


def run(command, timeout=45):
    return subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)


def inspect(name):
    return json.loads(run(['docker', 'inspect', name]).stdout)[0]


def owned_pause():
    return PAUSE.exists() and json.loads(PAUSE.read_text()).get('owner') == 'capacity256-handoff'


def remove_pause():
    if not owned_pause():
        raise ValueError('Pause ownership changed')
    PAUSE.unlink()


def stop_controller(pid, script):
    path = Path('/proc') / str(pid) / 'cmdline'
    if path.exists():
        if script.encode() not in path.read_bytes().split(bytes([0])):
            raise ValueError('Controller PID no longer belongs to this experiment')
        os.kill(pid, signal.SIGTERM)


def gateway_idle():
    pid = inspect(GATEWAY)['State']['Pid']
    if not pid:
        return False
    status = (Path('/proc') / str(pid) / 'status').read_text()
    return int(next(x.split()[1] for x in status.splitlines() if x.startswith('Threads:'))) == 1


def health(name, host='127.0.0.1'):
    code = ('import json,urllib.request; '
            f'assert json.load(urllib.request.urlopen("http://{host}:8080/health",timeout=5))["ok"]')
    run(['docker', 'exec', name, 'python', '-c', code], timeout=10)


def create_candidate(previous):
    config, host = previous['Config'], previous['HostConfig']
    if config['Entrypoint'] != ['python'] or host['PortBindings'] or host['NetworkMode'] != 'bridge':
        raise ValueError('Unexpected gateway configuration; do not approximate it')
    command = ['docker', 'create', '--name', CANDIDATE,
               '--label', 'org.hilbench.capacity=256-amendment', '--network', 'bridge',
               '--read-only', '--memory', str(6 * 1024**3), '--memory-swap', str(6 * 1024**3),
               '--cpus', str(host['NanoCpus'] / 1e9), '--pids-limit', str(host['PidsLimit']),
               '--user', config['User'], '--entrypoint', 'python']
    for value in host.get('CapDrop', []):
        command += ['--cap-drop', value]
    for value in host.get('SecurityOpt', []):
        command += ['--security-opt', value]
    for path, value in host.get('Tmpfs', {}).items():
        command += ['--tmpfs', path + ':' + value]
    for value in config['Env']:
        command += ['--env', value]
    for mount in previous['Mounts']:
        if mount['Type'] != 'bind':
            raise ValueError('Unexpected gateway mount type')
        value = f'type=bind,src={mount["Source"]},dst={mount["Destination"]}'
        if not mount['RW']:
            value += ',readonly'
        command += ['--mount', value]
    command += ['--mount', f'type=bind,src={ROOT}/scripts/gateway_capacity_extended.py,dst=/opt/gateway_capacity_extended.py,readonly']
    args = list(config['Cmd'])
    if args[0] != '/opt/gateway_capacity_ramp.py':
        raise ValueError('Unexpected gateway wrapper')
    args[0] = '/opt/gateway_capacity_extended.py'
    args[args.index('--max-inflight') + 1] = '256'
    command += [previous['Image'], *args]
    run(command)
    run(['docker', 'network', 'connect', NETWORK, CANDIDATE])
    run(['docker', 'start', CANDIDATE])
    for attempt in range(10):
        try:
            health(CANDIDATE)
            return
        except subprocess.CalledProcessError:
            if attempt == 9:
                raise
            time.sleep(1)


def start_supervisor(extended):
    script = 'scripts/supervise_sail_v4_extended.py' if extended else 'scripts/supervise_sail_v4.py'
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + ':' + str(ROOT / 'scripts'))
    with (ROOT / 'reports/sail4-capacity256-supervisor.log').open('ab') as log:
        process = subprocess.Popen(['python3', script], cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    return process.pid


def main():
    lock = (ROOT / 'reports/sail4-capacity256-handoff.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    verify_amendment()
    if not owned_pause():
        raise ValueError('Expected a pause owned by this handoff')
    request = json.loads((ROOT / 'reports/sail4-capacity256-handoff-request.json').read_text())
    old_control = json.loads(CONTROL.read_text())
    old_gateway = inspect(GATEWAY)
    state = {'state': 'draining', 'started_unix': time.time(), 'request': request}
    controllers_stopped = False
    old_renamed = False
    new_renamed = False
    resumed = False
    try:
        # Bound drain waiting; on failure release our pause to the old scheduler.
        deadline = time.time() + 1500
        while True:
            progress = json.loads((ROOT / 'reports/sail4-matched-r2_progress.json').read_text())
            state.update(checked_unix=time.time(), active=progress['active'],
                         finished_attempts=progress['finished_attempts'])
            save(STATE, state)
            if progress['active'] == 0 and gateway_idle():
                break
            if time.time() > deadline or not owned_pause():
                raise RuntimeError('Drain deadline or pause ownership changed')
            time.sleep(10)
        # Every registered episode must have a terminal status, including
        # failures. Never hide or replace an orphan registration on resume.
        plan = json.loads((ROOT / 'experiments/sail-v4-20260913/sail4-matched-r2.json').read_text())
        for job in plan['jobs']:
            registered = (ROOT / 'registry' / (job['run_id'] + '.json')).exists()
            closed = (ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json').exists()
            if registered and not closed:
                raise RuntimeError('Unfinished registration prevents handoff')
        state.update(state='preparing_gateway', drained_unix=time.time())
        save(STATE, state)
        create_candidate(old_gateway)
        for key, script in [('promotion_pid', 'scripts/promote_sail_v4.py'),
                            ('supervisor_pid', 'scripts/supervise_sail_v4.py'),
                            ('launcher_pid', 'scripts/launch_sail_v4_sequential.py')]:
            stop_controller(request[key], script)
        controllers_stopped = True
        with (ROOT / 'reports/sail4-matched-r2.lock').open('a') as handle:
            for attempt in range(30):
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if attempt == 29:
                        raise
                    time.sleep(.5)
        run(['docker', 'stop', GATEWAY])
        run(['docker', 'rename', GATEWAY, BACKUP])
        old_renamed = True
        # Remove the stopped endpoint before publishing the original DNS name.
        run(['docker', 'network', 'disconnect', NETWORK, BACKUP])
        run(['docker', 'rename', CANDIDATE, GATEWAY])
        new_renamed = True
        run(['docker', 'network', 'disconnect', NETWORK, GATEWAY])
        run(['docker', 'network', 'connect', '--alias', GATEWAY, NETWORK, GATEWAY])
        value = dict(old_control, gateway_capacity_ceiling=256, gateway_max_inflight=128,
                     aggregate_agent_target=128, effective_unix=time.time(),
                     capacity_authorization='experiments/sail-v4-20260913/capacity-amendment-v2.json')
        save(CONTROL, value)
        health(GATEWAY, GATEWAY)
        remove_pause()
        pid = start_supervisor(True)
        resumed = True
        state.update(state='resumed', resumed_unix=time.time(), supervisor_pid=pid,
                     gateway_backup=BACKUP, initial_concurrency=128, maximum_concurrency=256,
                     preserved_closed_attempts=progress['finished_attempts'])
        save(STATE, state)
        print(json.dumps(state), flush=True)
    except Exception as error:
        if resumed:
            # Once episodes can be active, a reporting error must never tear
            # down their gateway or replace their runs.
            state.update(state='resumed_reporting_error', error_type=type(error).__name__)
            save(STATE, state)
            raise
        state.update(state='rollback', error_type=type(error).__name__, checked_unix=time.time())
        save(STATE, state)
        if new_renamed:
            # No new episode has been started before the final resume step.
            run(['docker', 'rm', '-f', GATEWAY])
        else:
            subprocess.run(['docker', 'rm', '-f', CANDIDATE], capture_output=True, timeout=45)
        if old_renamed:
            run(['docker', 'rename', BACKUP, GATEWAY])
        if controllers_stopped:
            current = inspect(GATEWAY)
            if NETWORK not in current['NetworkSettings']['Networks']:
                run(['docker', 'network', 'connect', NETWORK, GATEWAY])
            save(CONTROL, old_control)
            run(['docker', 'start', GATEWAY])
        if owned_pause():
            remove_pause()
        if controllers_stopped:
            state['fallback_supervisor_pid'] = start_supervisor(False)
        state.update(state='rolled_back_to_original_scheduler', finished_unix=time.time())
        save(STATE, state)
        raise


if __name__ == '__main__':
    main()
