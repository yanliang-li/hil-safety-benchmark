"""Publish an explicit v4 allowlist to the previously authorized GitHub owner."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

import watch_api_experiment_local as connection

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--complete', action='store_true')
    args = parser.parse_args()
    public = connection.PUBLIC
    env = dict(os.environ, GH_CONFIG_DIR=connection.CONFIG['gh_config_dir'])
    env.pop('GH_TOKEN', None)
    env.pop('GITHUB_TOKEN', None)
    account = connection.run([connection.CONFIG['gh_executable'], 'api', 'user', '--jq', '.login'], env=env, timeout=30).stdout.strip()
    if account != 'yanliang-li' or account != connection.CONFIG['github_owner']:
        raise ValueError('GitHub account does not match the authorized owner')
    selected = set()
    for folder in ('scripts/hil_guard_v4', 'experiments/sail-v4-20260913'):
        selected.update(p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    names = ['.gitattributes', 'docs/sail_v4_method.md', 'tests/test_hil_guard_v4.py', 'tests/test_sail_v4_analysis.py',
        'scripts/prepare_sail_v4.py', 'scripts/build_sail_v4_data.py', 'scripts/analyze_sail_v4.py',
        'scripts/audit_sail_v4.py', 'scripts/collect_sail_v4.py', 'scripts/supervise_sail_v4.py',
        'scripts/promote_sail_v4.py', 'scripts/watch_sail_v4.py', 'scripts/publish_sail_v4.py',
        'scripts/diagnose_sail_v3_utility.py', 'scripts/plot_sail_v4_method.py',
        'scripts/build_sail_v4_paper.py', 'scripts/package_iclr_v4_draft.py',
        'scripts/plot_sail_v4_results.py', 'scripts/prepare_sail_v4_matched.py',
        'scripts/build_sail_v4_matched_paper.py', 'tests/test_sail_v4_matched_plan.py',
        'scripts/prepare_sail_v4_sequential.py', 'scripts/launch_sail_v4_sequential.py',
        'tests/test_sail_v4_sequential.py','scripts/sail_v4_capacity.py','tests/test_sail_v4_capacity.py',
        'scripts/prepare_sail_v4_engineering_r3.py','tests/test_sail_v4_engineering_r3.py',
        'scripts/sail_v4_capacity_extended.py','scripts/launch_sail_v4_extended.py',
        'scripts/gateway_capacity_extended.py','scripts/supervise_sail_v4_extended.py',
        'scripts/handoff_sail_v4_extended.py','tests/test_sail_v4_capacity_extended.py']
    selected.update(ROOT / n for n in names if (ROOT / n).exists())
    for path in (ROOT / 'reports/sail-v4-20260913').rglob('*'):
        if path.is_file() and path.suffix in ('.json', '.csv', '.md'):
            relative = path.relative_to(ROOT / 'reports/sail-v4-20260913')
            if len(relative.parts) > 1:
                summary = ROOT / 'reports/sail-v4-20260913' / relative.parts[0] / 'summary.json'
                if not summary.exists() or json.loads(summary.read_text()).get('status') != 'complete':
                    continue
            selected.add(path)
    # Share the built, coherent manuscript, not private working archives.
    for path in (ROOT / 'paper/iclr2027').rglob('*'):
        if path.is_file() and 'build' not in path.relative_to(ROOT / 'paper/iclr2027').parts and path.suffix in ('.tex', '.bib', '.sty', '.bst', '.md', '.json', '.csv', '.pdf', '.svg', '.zip'):
            selected.add(path)
    if args.complete:
        for phase in ('matched',):
            path = ROOT / 'reports/sail-v4-20260913' / f'sail4-{phase}-r2/summary.json'
            if not path.exists() or json.loads(path.read_text())['status'] != 'complete':
                raise ValueError('Formal results are not complete')
        validation = json.loads((ROOT / 'paper/iclr2027/build_validation.json').read_text())
        if not validation.get('standalone_source_bundle_compiles') or not validation.get('main_text_within_official_nine_page_limit'):
            raise ValueError('Paper build has not passed validation')
    relatives = []
    for path in sorted(selected):
        if path.is_symlink():
            raise ValueError('Refusing symlink in public export')
        rel = path.relative_to(ROOT)
        dest = public / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        relatives.append(str(rel))
    spec = importlib.util.spec_from_file_location('release_audit', ROOT / 'scripts/prepare_public_release.py')
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    report = audit.audit(public)
    ssh_profile = ROOT / '.secrets/fdusmilab-ssh.json'
    if ssh_profile.exists():
        secret = json.loads(ssh_profile.read_text())['password'].encode()
        for rel in relatives:
            if secret in (public / rel).read_bytes():
                raise ValueError('Credential match in public export; value suppressed')
    # This audited explicit list includes a synthetic case fixture named
    # audit.log, which the repository's generic log exclusion would omit.
    connection.run(['git', 'add', '--force', '--', *relatives], cwd=public, timeout=60)
    connection.run(['git', 'diff', '--cached', '--check'], cwd=public, timeout=30)
    changed = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=public).returncode
    if changed:
        connection.run(['git', 'commit', '--quiet', '-m',
            'Complete frozen SAIL v4 evaluation and revise ICLR draft' if args.complete else
            'Match third-round evaluation to the second-round experimental design'], cwd=public, timeout=60)
    connection.run(['git', 'push', 'origin', 'main'], cwd=public, env=env, timeout=120)
    commit = connection.run(['git', 'rev-parse', 'HEAD'], cwd=public, timeout=10).stdout.strip()
    output = {'github_owner': account, 'commit': commit, 'complete_formal_results': args.complete,
        'exported_files': len(relatives), 'credential_pattern_matches': report['credential_pattern_matches']}
    dest = ROOT / 'recovery/sail-v4-20260913/publication.json'
    dest.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
