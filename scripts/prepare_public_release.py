#!/usr/bin/env python3
"""Export an explicit allowlist into a separate Git checkout; never export secrets."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def export(dest):
    dest.mkdir(parents=True, exist_ok=True)
    selected = set()
    for folder, pattern in [('src/hil_safety_bench', '*.py'), ('tests', '*.py'), ('data', '*')]:
        selected.update(p for p in (ROOT / folder).rglob(pattern) if p.is_file())
    selected.update(ROOT / p for p in ['pyproject.toml', 'Dockerfile', 'compose.yaml', 'Makefile',
        'case_000631/hil/evaluate.py', 'requirements-recovery-20260912.txt',
        'experiments/gpt-luna-pilot-80-v1.json', 'experiments/gpt-luna-smoke-4-v1.json',
        'experiments/prompt-guard-80-v1-plan.json'])
    selected.update(p for p in (ROOT / 'scripts').glob('*.py'))
    selected.update(p for p in (ROOT / 'docker/pilot').rglob('*') if p.is_file())
    for name in ['metrics_zh.md', 'prompt_guard_v1_design.md', 'experiment_protocol.md',
                 'hil_safety_1000_v4_design.md', 'specs.md', 'workflow_native_v2_design.md']:
        selected.add(ROOT / 'docs' / name)
    for p in sorted(selected):
        if '__pycache__' in p.parts or not p.is_file():
            continue
        if p.is_symlink():
            raise ValueError('Do not export symlinks: ' + str(p))
        q = dest / p.relative_to(ROOT)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
    paper = dest / 'paper/iclr2027'
    paper.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ROOT / 'paper/iclr2027/iclr2027-draft-source.zip') as archive:
        for info in archive.infolist():
            path = Path(info.filename)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Unsafe source archive path')
            if not info.is_dir():
                q = paper / path
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_bytes(archive.read(info))
    shutil.copy2(ROOT / 'paper/iclr2027/main.pdf', paper / 'main.pdf')
    (paper / 'README.md').write_text('# ICLR 2027 working draft\n\nCompile `main.tex` using `latexmk -pdf main.tex`, or upload this directory to Overleaf. Figures and tables are included. This is an internal working draft, not an accepted paper.\n')
    metrics = json.loads((ROOT / 'reports/six-metrics-20260912/metrics.json').read_text())
    summary = {k: v for k, v in metrics.items() if k not in ['evidence']}
    reports = dest / 'reports'; reports.mkdir(exist_ok=True)
    (reports / 'pilot_six_metrics.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (dest / '.gitignore').write_text('.venv/\n__pycache__/\n.pytest_cache/\n*.py[cod]\n*.egg-info/\n.secrets/\n.env\n.env.*\nhistory/\nrecovery/\nruns/\nregistry/\ngateway_evidence/\n*.log\n*.aux\n*.blg\n')
    (dest / '.dockerignore').write_text('.git\n.venv\n__pycache__\n.pytest_cache\n.secrets\n.env\nruns\nregistry\ngateway_evidence\nhistory\nrecovery\n')
    return audit(dest)


def audit(dest):
    patterns = [rb'github_pat_[A-Za-z0-9_]{20,}', rb'gh[pousr]_[A-Za-z0-9]{20,}',
                rb'sk-[A-Za-z0-9_-]{24,}', rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',
                rb'chatgpt\.com/share/']
    # Compare the real local key in memory without printing it or storing its hash.
    profile = ROOT / '.secrets/boyu-20260912.json'
    exact = [json.loads(profile.read_text())['api_key'].encode()] if profile.exists() else []
    connection = ROOT / 'recovery/api_experiment_connection.json'
    if connection.exists():
        target = json.loads(connection.read_text()).get('ssh_target', '')
        if target: exact.append(target.rsplit('@', 1)[-1].encode())
    failures, files = [], {}
    for p in sorted(dest.rglob('*')):
        if not p.is_file() or '.git' in p.relative_to(dest).parts:
            continue
        content = p.read_bytes()
        if any(re.search(pattern, content) for pattern in patterns) or any(key in content for key in exact):
            failures.append(str(p.relative_to(dest)))
        files[str(p.relative_to(dest))] = hashlib.sha256(content).hexdigest()
    if failures:
        raise ValueError('Publication scan requires review (values suppressed): ' + ', '.join(failures))
    return {'file_count': len(files), 'files': files, 'credential_pattern_matches': 0,
            'private_conversations_exported': False, 'real_credentials_exported': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    report = export(args.destination)
    (ROOT / 'recovery/publication_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}))
