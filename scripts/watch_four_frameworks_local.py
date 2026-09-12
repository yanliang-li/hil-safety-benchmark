"""Fetch both frozen cohorts, independently replay scores, and publish safe reports."""
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import time

import watch_api_experiment_local as common

ROOT, CONFIG, PUBLIC, PYTHON = common.ROOT, common.CONFIG, common.PUBLIC, common.PYTHON
STATE = ROOT / 'recovery/api-multimodel-20260912/four-framework-watch.json'
COHORTS = {'main': ('main-v1', 'main01_', 'main-plan-v1'),
           'hermes': ('hermes-main-v1', 'hermes01_', 'hermes-plan-v1')}


def extract_checked(archive, stage, ids):
    allowed = {f'runs/{stage}/{rid}' for rid in ids} | {f'gateway_evidence/{rid}' for rid in ids}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            if path.is_absolute() or '..' in path.parts or not (member.isfile() or member.isdir()):
                raise ValueError('Unsafe export member')
            if not any(member.name == prefix or member.name.startswith(prefix + '/') for prefix in allowed):
                raise ValueError('Unexpected export member')
        tar.extractall(ROOT, filter='data')


def fetch(cohort, ids):
    stage, stem, _ = COHORTS[cohort]
    if not all(re.fullmatch(re.escape(stem) + r'[a-f0-9]{20}', rid) for rid in ids):
        raise ValueError('Invalid closed attempt identifier')
    prefix = 'from pathlib import Path\nimport json,tarfile\nroot=Path(' + repr(CONFIG['remote_root']) + ')\n'
    # Bounded archives keep final reconciliation below SSH/transfer timeouts.
    for offset in range(0, len(ids), 80):
        batch = ids[offset:offset + 80]
        code = prefix + 'ids=' + repr(batch) + '\nstage=' + repr(stage) + "\narchive=root/'reports/four-framework-export.tar.gz'\nwith tarfile.open(archive,'w:gz') as tar:\n for rid in ids:\n  for rel in ['runs/'+stage+'/'+rid,'gateway_evidence/'+rid]:\n   path=root/rel\n   if path.exists():tar.add(path,arcname=rel)\nprint(json.dumps({'archive':str(archive)}))\n"
        archive = common.remote(code)['archive']
        local = ROOT / 'recovery/api-multimodel-20260912/four-framework-export.tar.gz'
        common.run(['scp', '-o', 'ControlPath=' + CONFIG['control_path'], '-o', 'BatchMode=yes',
                    CONFIG['ssh_target'] + ':' + archive, str(local)], timeout=240)
        extract_checked(local, stage, batch)
        if any(not (ROOT / 'runs' / stage / rid / 'attempt_status.json').exists() for rid in batch):
            raise ValueError('Export lacks closed attempt status')


def copy_public():
    for cohort in ['main', 'hermes', 'four-frameworks']:
        for path in (ROOT / 'reports/api-multimodel-20260912' / cohort).glob('*'):
            if path.is_file() and path.suffix in ('.json', '.csv', '.md'):
                dest = PUBLIC / path.relative_to(ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
    common.copy_public()


def publish(count, complete):
    env = dict(os.environ, GH_CONFIG_DIR=CONFIG['gh_config_dir'])
    env.pop('GH_TOKEN', None)
    env.pop('GITHUB_TOKEN', None)
    account = common.run([CONFIG['gh_executable'], 'api', 'user', '--jq', '.login'], env=env, timeout=30).stdout.strip()
    if account != CONFIG['github_owner']:
        raise ValueError('Unexpected GitHub account')
    spec = importlib.util.spec_from_file_location('public_audit', ROOT / 'scripts/prepare_public_release.py')
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    audit.audit(PUBLIC)
    common.run(['git', 'add', '--', *['reports/api-multimodel-20260912/' + c for c in ['main', 'hermes', 'four-frameworks']],
                'paper/iclr2027'], cwd=PUBLIC, timeout=30)
    common.run(['git', '-c', 'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol',
                'diff', '--cached', '--check'], cwd=PUBLIC, timeout=30)
    changed = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=PUBLIC).returncode
    if changed:
        common.run(['git', 'commit', '--quiet', '-m',
                    f'{"Complete" if complete else "Update provisional"} four-framework experiment: {count} closed attempts'],
                   cwd=PUBLIC, timeout=30)
    common.run(['git', 'push', 'origin', 'main'], cwd=PUBLIC, env=env, timeout=120)
    return common.run(['git', 'rev-parse', 'HEAD'], cwd=PUBLIC, timeout=10).stdout.strip()


def save(state):
    temporary = STATE.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2) + '\n')
    temporary.replace(STATE)


def main():
    lock = STATE.with_suffix('.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if STATE.exists():
        state = json.loads(STATE.read_text())
    else:
        previous = json.loads(common.STATE.read_text()) if common.STATE.exists() else {}
        state = {'fetched_ids': {'main': previous.get('fetched_ids', []), 'hermes': []},
                 'final_refetch_done': {}, 'last_published_count': -1}
    while True:
        try:
            prefix = 'from pathlib import Path\nimport json\nroot=Path(' + repr(CONFIG['remote_root']) + ')\n'
            paths = {name: 'reports/' + values[2] + '_progress.json' for name, values in COHORTS.items()}
            progress = common.remote(prefix + 'paths=' + repr(paths) + "\nprint(json.dumps({name:json.loads((root/path).read_text()) for name,path in paths.items()}))\n")
            for cohort, item in progress.items():
                finished = sorted(r['run_id'] for r in item['results'])
                complete = bool(item.get('finished_unix'))
                unseen = sorted(set(finished) - set(state['fetched_ids'][cohort]))
                if complete and not state['final_refetch_done'].get(cohort):
                    unseen = finished
                if unseen:
                    fetch(cohort, unseen)
                    state['fetched_ids'][cohort] = sorted(set(state['fetched_ids'][cohort]) | set(unseen))
                if complete:
                    state['final_refetch_done'][cohort] = True
                save(state)
            count = sum(len(p['results']) for p in progress.values())
            complete = all(p.get('finished_unix') for p in progress.values())
            if count > state.get('last_processed_count', -1) or (complete and not state.get('final_processed')):
                env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'))
                common.run([PYTHON, 'scripts/analyze_four_frameworks.py', '--bootstrap', '10000' if complete else '1000'],
                           cwd=ROOT, env=env, timeout=480)
                capacity = common.remote(prefix + "import subprocess\nsubprocess.run(['python3','scripts/report_api_capacity.py'],cwd=root,capture_output=True,check=True,timeout=180)\nprint((root/'reports/api-multimodel-20260912/main/capacity_report.json').read_text())\n")
                (ROOT / 'reports/api-multimodel-20260912/main/capacity_report.json').write_text(json.dumps(capacity, indent=2) + '\n')
                resources = common.remote(prefix + "import subprocess\np=subprocess.run(['python3','scripts/report_four_framework_capacity.py'],cwd=root,capture_output=True,text=True,check=True,timeout=180)\nprint(p.stdout)\n")
                (ROOT / 'reports/api-multimodel-20260912/four-frameworks/capacity_report.json').write_text(json.dumps(resources, indent=2) + '\n')
                common.build_paper()
                copy_public()
                if state['last_published_count'] < 0 or count - state['last_published_count'] >= 100 or complete:
                    state['published_commit'] = publish(count, complete)
                    state['last_published_count'] = count
                state['last_processed_count'] = count
                if complete:
                    state['final_processed'] = True
            state.update(checked_unix=time.time(), finished_attempts=count,
                         planned=sum(p['planned'] for p in progress.values()),
                         cohorts={name: {'finished': len(p['results']), 'planned': p['planned'],
                                         'active': p.get('active_attempts'), 'complete': bool(p.get('finished_unix'))}
                                  for name, p in progress.items()},
                         remote_complete=bool(complete), last_error=None)
            save(state)
            print(json.dumps({k: v for k, v in state.items() if k != 'fetched_ids'}), flush=True)
            if complete:
                break
        except Exception as error:
            state.update(checked_unix=time.time(), last_error=type(error).__name__ + ': ' + str(error)[:700])
            save(state)
            print(json.dumps({'error': state['last_error']}), flush=True)
        time.sleep(180)


if __name__ == '__main__':
    main()
