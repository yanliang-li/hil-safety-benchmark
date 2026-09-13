"""Keep third-round evidence locally mirrored and finish the paper after all phases.

Private SSH/publication configuration stays in recovery; no credentials or raw
trajectories are copied into the public checkout. Every checkpoint is resumable.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import watch_api_experiment_local as connection
from collect_sail_v4 import collect

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'recovery/sail-v4-20260913/local-watch.json'


def save(value):
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(STATE)


def ensure_connection():
    check = subprocess.run(['ssh', '-S', connection.CONFIG['control_path'], '-O', 'check',
        connection.CONFIG['ssh_target']], capture_output=True, timeout=15)
    if check.returncode == 0:
        return
    helper = ROOT / '.secrets/ssh_askpass.py'
    if not helper.exists():
        raise RuntimeError('SSH session unavailable; private reconnect helper is absent')
    Path(connection.CONFIG['control_path']).unlink(missing_ok=True)
    env = dict(os.environ, DISPLAY=':0', SSH_ASKPASS=str(helper), SSH_ASKPASS_REQUIRE='force')
    result = subprocess.run(['ssh', '-M', '-S', connection.CONFIG['control_path'], '-o', 'ControlPersist=12h',
        '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=15', '-fnN', connection.CONFIG['ssh_target']],
        stdin=subprocess.DEVNULL, capture_output=True, env=env, timeout=45, start_new_session=True)
    if result.returncode:
        raise RuntimeError('SSH reconnect failed; details suppressed to protect connection metadata')


def sync_control():
    prefix = 'from pathlib import Path\nimport json\nr=Path(' + repr(connection.CONFIG['remote_root']) + ')\n'
    code = prefix + '''files={}
for name in ('authorized_scope.json','matched_formal_freeze.json','matched_engineering_gate.json','sail4-matched-r2.json'):
 p=r/'experiments/sail-v4-20260913'/name
 if p.exists():files[name]=p.read_text()
control={}
for name in ('sail4-promotion.json','sail4-formal-supervisor.json'):
 p=r/'reports'/name
 if p.exists():control[name]=json.loads(p.read_text())
print(json.dumps({'files':files,'control':control}))
'''
    value = connection.remote(code)
    for name, content in value['files'].items():
        path = ROOT / 'experiments/sail-v4-20260913' / name
        if path.exists() and path.read_text() != content:
            raise ValueError('Remote frozen artifact differs from local copy: ' + name)
        if not path.exists():
            path.write_text(content)
    return value['control']


def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    lock = STATE.with_suffix('.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state = json.loads(STATE.read_text()) if STATE.exists() else {'phases': {}, 'started_unix': time.time()}
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + ':' + str(ROOT / 'scripts'))
    while not state.get('final_processed'):
        try:
            ensure_connection()
            control = sync_control()
            state['remote_control'] = control
            names = ['sail4-preflight-r1', 'sail4-preflight-matched-r2', 'sail4-matched-r2']
            for name in names:
                path = ROOT / 'experiments/sail-v4-20260913' / (name + '.json')
                if not path.exists() or state['phases'].get(name, {}).get('final_processed'):
                    continue
                # A plan can exist before its phase starts. Avoid treating a
                # missing progress file as a failed experiment.
                prefix = 'from pathlib import Path\nimport json\nr=Path(' + repr(connection.CONFIG['remote_root']) + ')\n'
                exists = connection.remote(prefix + 'print(json.dumps((r/' + repr('reports/' + name + '_progress.json') + ').exists()))')
                if not exists:
                    continue
                progress = collect(path)
                count = progress.get('finished_attempts', 0)
                old = state['phases'].get(name, {})
                final = bool(progress.get('finished_unix'))
                step = 32 if 'preflight' in name else 250
                if count - old.get('analyzed_attempts', -step) >= step or final:
                    output = 'reports/sail-v4-20260913/' + name
                    subprocess.run([sys.executable, 'scripts/analyze_sail_v4.py', '--plan', str(path), '--output', output,
                        '--bootstrap', '10000' if final else '1000'], cwd=ROOT, env=env, check=True)
                    subprocess.run([sys.executable, 'scripts/audit_sail_v4.py', '--plan', str(path),
                        '--output', output + '/input_audit.json'], cwd=ROOT, env=env, check=True)
                    old.update(analyzed_attempts=count, final_processed=final)
                old.update(progress=progress)
                state['phases'][name] = old
                save(state)
            formal = ('sail4-matched-r2',)
            if all(state['phases'].get(name, {}).get('final_processed') for name in formal):
                subprocess.run([sys.executable, 'scripts/build_sail_v4_paper.py', '--require-complete'], cwd=ROOT, env=env, check=True)
                subprocess.run([sys.executable, 'scripts/package_iclr_v4_draft.py'], cwd=ROOT, env=env, check=True)
                subprocess.run([sys.executable, 'scripts/publish_sail_v4.py', '--complete'], cwd=ROOT, env=env, check=True)
                state.update(final_processed=True, finished_unix=time.time())
            state.update(last_error=None, checked_unix=time.time())
            save(state)
        except Exception as error:
            # Keep a useful error without echoing command arguments or secrets.
            state.update(last_error=type(error).__name__, checked_unix=time.time())
            save(state)
            print(json.dumps({'watch_error': type(error).__name__, 'time_unix': time.time()}), flush=True)
        if not state.get('final_processed'):
            time.sleep(45)


if __name__ == '__main__':
    main()
