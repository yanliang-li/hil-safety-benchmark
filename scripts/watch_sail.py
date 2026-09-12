"""Fetch closed SAIL attempts, replay locally, and publish audited reports.

Private connection settings are read by the existing connection helper. Neither
raw trajectories nor gateway evidence are copied to the public repository.
"""
import argparse
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
PLAN = 'experiments/sail-20260913/sail-main-v3.json'
REPORT = 'reports/sail-20260913/main-v3'
STATE = ROOT / 'recovery/sail-20260913/local-watch.json'


def save(value):
    temp = STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(STATE)


def fetch(stage, ids):
    if stage not in ('sail-preflight-v1', 'sail-preflight-v2', 'sail-preflight-v3', 'sail-main-v3'):
        raise ValueError('Invalid stage')
    if not all(re.fullmatch(r'sail(?:pre0[123]|main03)_[a-f0-9]{20}', rid) for rid in ids):
        raise ValueError('Invalid run identifier')
    prefix = 'from pathlib import Path\nimport json,tarfile\nroot=Path(' + repr(CONFIG['remote_root']) + ')\n'
    for offset in range(0, len(ids), 80):
        batch = ids[offset:offset+80]
        code = prefix + 'ids=' + repr(batch) + '\nstage=' + repr(stage) + "\narchive=root/'reports/sail-export.tar.gz'\nwith tarfile.open(archive,'w:gz') as tar:\n for rid in ids:\n  for rel in ['runs/'+stage+'/'+rid,'gateway_evidence/'+rid,'gateway_evidence/'+rid+'_guard']:\n   p=root/rel\n   if p.exists():tar.add(p,arcname=rel)\nprint(json.dumps({'archive':str(archive)}))\n"
        archive = common.remote(code)['archive']
        local = ROOT / 'recovery/sail-20260913/sail-export.tar.gz'
        common.run(['scp', '-o', 'ControlPath='+CONFIG['control_path'], '-o', 'BatchMode=yes',
                    CONFIG['ssh_target']+':'+archive, str(local)], timeout=240)
        allowed = {f'runs/{stage}/{rid}' for rid in batch}
        allowed |= {f'gateway_evidence/{rid}{suffix}' for rid in batch for suffix in ('', '_guard')}
        with tarfile.open(local) as tar:
            for member in tar.getmembers():
                p = Path(member.name)
                if p.is_absolute() or '..' in p.parts or not (member.isfile() or member.isdir()):
                    raise ValueError('Unsafe export member')
                if not any(member.name == prefix or member.name.startswith(prefix+'/') for prefix in allowed):
                    raise ValueError('Unexpected export member')
            tar.extractall(ROOT, filter='data')
        if any(not (ROOT/'runs'/stage/rid/'attempt_status.json').exists() for rid in batch):
            raise ValueError('Missing closed attempt status')


def publish(count, complete):
    # Copy only derived reports and manuscript artifacts, never raw evidence.
    for folder in ('reports/sail-20260913', 'paper/iclr2027'):
        for path in (ROOT/folder).rglob('*'):
            if not path.is_file() or 'build' in path.relative_to(ROOT/folder).parts:
                continue
            if path.suffix not in ('.json','.csv','.md','.tex','.bib','.sty','.bst','.pdf','.svg','.zip','.py'):
                continue
            dest = PUBLIC/path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    env = dict(os.environ, GH_CONFIG_DIR=CONFIG['gh_config_dir'])
    env.pop('GH_TOKEN', None); env.pop('GITHUB_TOKEN', None)
    account = common.run([CONFIG['gh_executable'],'api','user','--jq','.login'], env=env,timeout=30).stdout.strip()
    if account != CONFIG['github_owner']:
        raise ValueError('Unexpected GitHub account')
    spec = importlib.util.spec_from_file_location('release_audit', ROOT/'scripts/prepare_public_release.py')
    audit = importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    audit.audit(PUBLIC)
    common.run(['git','add','--','reports/sail-20260913','paper/iclr2027'],cwd=PUBLIC,timeout=30)
    common.run(['git','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol',
                'diff','--cached','--check'],cwd=PUBLIC,timeout=30)
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=PUBLIC).returncode:
        common.run(['git','commit','--quiet','-m',f'{"Complete" if complete else "Update provisional"} SAIL comparison: {count} closed attempts'],cwd=PUBLIC,timeout=30)
    common.run(['git','push','origin','main'],cwd=PUBLIC,env=env,timeout=120)
    return common.run(['git','rev-parse','HEAD'],cwd=PUBLIC,timeout=10).stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--no-publish', action='store_true')
    args = parser.parse_args()
    lock = STATE.with_suffix('.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    state = json.loads(STATE.read_text()) if STATE.exists() else {'fetched_ids':[], 'last_published_count':-1}
    while True:
        try:
            prefix = 'from pathlib import Path\nimport json\nroot=Path(' + repr(CONFIG['remote_root']) + ')\n'
            progress = common.remote(prefix + "print((root/'reports/sail-main-v3_progress.json').read_text())\n")
            complete = bool(progress.get('finished_unix'))
            finished = sorted(r['run_id'] for r in progress['results'])
            unseen = sorted(set(finished)-set(state['fetched_ids']))
            if complete and not state.get('final_refetch_done'):
                unseen = finished
            if unseen:
                fetch('sail-main-v3', unseen)
                state['fetched_ids'] = sorted(set(state['fetched_ids'])|set(unseen))
            if complete:
                state['final_refetch_done'] = True
            save(state)
            count = len(finished)
            if count != state.get('last_processed_count') or (complete and not state.get('final_processed')):
                common.run([PYTHON,'scripts/analyze_sail_v3.py','--plan',PLAN,'--output',REPORT,
                            '--bootstrap','10000' if complete else '1000'],cwd=ROOT,timeout=480)
                if complete:
                    common.run([PYTHON,'scripts/audit_sail_inputs.py','--plan',PLAN,
                                '--output',REPORT+'/input_audit.json'],cwd=ROOT,timeout=240)
                common.run([PYTHON,'scripts/build_sail_results.py'],cwd=ROOT,timeout=60)
                if complete:
                    common.run([PYTHON,'scripts/package_iclr_draft.py'],cwd=ROOT,timeout=240)
                if not args.no_publish and (count-state['last_published_count']>=240 or complete):
                    state['published_commit'] = publish(count, complete)
                    state['last_published_count'] = count
                state['last_processed_count'] = count
                state['final_processed'] = complete
            state.update(checked_unix=time.time(),finished_attempts=count,planned=progress['planned'],
                         valid_runs=progress['valid_runs'],active=progress['active'],queued=progress['queued'],
                         remote_complete=complete,last_error=None)
            save(state)
            print(json.dumps({k:v for k,v in state.items() if k!='fetched_ids'}),flush=True)
            if complete or args.once:
                break
        except Exception as error:
            state.update(checked_unix=time.time(),last_error=type(error).__name__+': '+str(error)[:600])
            save(state)
            print(json.dumps({'error':state['last_error']}),flush=True)
            if args.once:
                raise
        time.sleep(60)


if __name__ == '__main__':
    main()
