"""Fetch only closed third-round attempts over the existing private SSH session."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
import time

import watch_api_experiment_local as connection

ROOT = Path(__file__).resolve().parents[1]


def collect(plan_path):
    plan = json.loads(plan_path.read_text())
    stage = plan['experiment']
    if not re.fullmatch(r'sail4-(preflight(?:-matched)?|matched|regression|heldout|clean)-r[123]', stage):
        raise ValueError('Unexpected third-round stage')
    state_path = ROOT / 'recovery/sail-v4-20260913' / (stage + '-collection.json')
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(state_path.read_text()) if state_path.exists() else {'fetched_ids': []}
    prefix = 'from pathlib import Path\nimport json,tarfile\nroot=Path(' + repr(connection.CONFIG['remote_root']) + ')\n'
    progress = connection.remote(prefix + 'print((root/' + repr('reports/' + plan_path.stem + '_progress.json') + ').read_text())')
    if progress['plan_sha256'] != hashlib.sha256(plan_path.read_bytes()).hexdigest():
        raise ValueError('Remote progress does not belong to the frozen local plan')
    closed = [row['run_id'] for row in progress['results']]
    expected = {j['run_id'] for j in plan['jobs']}
    assert set(closed) <= expected
    unseen = sorted(set(closed) - set(state['fetched_ids']))
    if progress.get('finished_unix') and not state.get('final_refetched'):
        unseen = sorted(closed)
    for offset in range(0, len(unseen), 80):
        batch = unseen[offset:offset + 80]
        assert all(re.fullmatch(r'sail4_[0-9a-f]{24}', rid) for rid in batch)
        code = prefix + 'ids=' + repr(batch) + '\nstage=' + repr(stage) + '\n'
        code += '''archive=root/'reports/sail4-closed-export.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
 for rid in ids:
  for rel in ['runs/'+stage+'/'+rid,'gateway_evidence/'+rid,'gateway_evidence/'+rid+'_guard']:
   p=root/rel
   if p.exists():tar.add(p,arcname=rel)
print(json.dumps({'archive':str(archive)}))
'''
        remote_archive = connection.remote(code)['archive']
        archive = state_path.parent / 'closed-export.tar.gz'
        connection.run(['scp', '-o', 'ControlPath=' + connection.CONFIG['control_path'], '-o', 'BatchMode=yes',
            connection.CONFIG['ssh_target'] + ':' + remote_archive, str(archive)], timeout=240)
        allowed = ['runs/' + stage + '/' + rid for rid in batch]
        allowed += ['gateway_evidence/' + rid + suffix for rid in batch for suffix in ('', '_guard')]
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                path = Path(member.name)
                if path.is_absolute() or '..' in path.parts or not (member.isfile() or member.isdir()):
                    raise ValueError('Unsafe archive entry')
                if not any(member.name == rel or member.name.startswith(rel + '/') for rel in allowed):
                    raise ValueError('Unexpected export prefix')
            tar.extractall(ROOT, filter='data')
        state['fetched_ids'] = sorted(set(state['fetched_ids']) | set(batch))
        state_path.write_text(json.dumps(state, indent=2) + '\n')
    if progress.get('finished_unix'):
        state['final_refetched'] = True
    state.update(checked_unix=time.time(), remote_complete=bool(progress.get('finished_unix')))
    state_path.write_text(json.dumps(state, indent=2) + '\n')
    local_progress = ROOT / 'reports/sail-v4-20260913' / stage / 'progress.json'
    local_progress.parent.mkdir(parents=True, exist_ok=True)
    local_progress.write_text(json.dumps({k: v for k, v in progress.items() if k != 'results'}, indent=2) + '\n')
    return {k: v for k, v in progress.items() if k != 'results'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    while True:
        value = collect(args.plan)
        print(json.dumps(value), flush=True)
        if not args.watch or value.get('finished_unix'):
            break
        time.sleep(45)


if __name__ == '__main__':
    main()
