"""Measure aggregate Docker resources and recent throughput for both cohorts."""
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    now = time.time()
    progress = {name: json.loads((ROOT / f'reports/{name}-plan-v1_progress.json').read_text()) for name in ['main', 'hermes']}
    start = max(now - 600, progress['hermes']['started_unix'])
    seconds = now - start
    rows = [r for p in progress.values() for r in p['results']]
    recent = [r for r in rows if r['finished_unix'] >= start]
    stats = subprocess.check_output(['docker', 'stats', '--no-stream', '--format', '{{json .}}'], text=True)
    containers = []
    factors = {'B': 1, 'KiB': 1024, 'MiB': 1024**2, 'GiB': 1024**3}
    for line in stats.splitlines():
        item = json.loads(line)
        name = item['Name']
        if not (re.fullmatch(r'(?:main01_|hermes01_)[a-f0-9]{20}', name) or name == 'hil-api-gateway-capacity-20260912'):
            continue
        match = re.fullmatch(r'([0-9.]+)(B|KiB|MiB|GiB)', item['MemUsage'].split(' / ')[0])
        if match is None:
            raise ValueError('Unrecognized Docker memory unit')
        value, unit = match.groups()
        containers.append({'name': name, 'memory_bytes': float(value) * factors[unit],
                           'cpu_cores': float(item['CPUPerc'].rstrip('%')) / 100})
    memory = {line.split(':')[0]: int(line.split()[1]) * 1024 for line in Path('/proc/meminfo').read_text().splitlines()}
    requests = []
    for r in rows:
        if r['finished_unix'] < start:
            continue
        for path in (ROOT / 'gateway_evidence' / r['run_id']).glob('request_*.json'):
            request = json.loads(path.read_text())
            if request.get('finished_unix', 0) >= start:
                requests.append(request)
    report = {'sampled_unix': now, 'aggregate_agent_limit': 32,
              'active_agent_containers': sum(c['name'].startswith(('main01_', 'hermes01_')) for c in containers),
              'memory_bytes_including_relay': sum(c['memory_bytes'] for c in containers),
              'cpu_cores_including_relay': sum(c['cpu_cores'] for c in containers),
              'host_available_memory_bytes': memory['MemAvailable'], 'host_total_memory_bytes': memory['MemTotal'],
              'host_load_1m': os.getloadavg()[0], 'logical_cpus': os.cpu_count(),
              'window_seconds': seconds, 'recent_closed_attempts': len(recent),
              'recent_valid_attempts': sum(bool(r['completed']) for r in recent),
              'recent_failed_attempts': sum(not r['completed'] for r in recent),
              'closed_attempts_per_hour': len(recent) * 3600 / seconds if seconds else None,
              'valid_attempts_per_hour': sum(bool(r['completed']) for r in recent) * 3600 / seconds if seconds else None,
              'recent_oom_kills': sum(bool(r.get('docker_state', {}).get('OOMKilled')) for r in recent),
              'http_status_counts_closed_attempt_requests': dict(Counter(str(r.get('http_status')) for r in requests)),
              'transport_errors_closed_attempt_requests': sum(r.get('state') == 'transport_error' for r in requests),
              'cohorts': {name: {'planned': p['planned'], 'closed': len(p['results']),
                                'valid': sum(bool(r['completed']) for r in p['results']),
                                'active': p.get('active_attempts')} for name, p in progress.items()},
              'caveat': 'Single resource sample; trailing window includes carryover attempts and changing case/model mix. Request metrics cover closed attempts only, not active requests. This is not a controlled concurrency comparison.',
              'scaling_status': 'Aggregate target remains 32. A larger target requires coordinated changes to both pools and a separately recorded capacity amendment.'}
    output = ROOT / 'reports/api-multimodel-20260912/four-frameworks/capacity_report.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
