"""Measure aggregate Docker resources and recent throughput for both cohorts."""
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def is_experiment_container(name):
    return bool(re.fullmatch(r'(?:main01_|hermes01_)[a-f0-9]{20}', name)) or name in {
        'hil-api-gateway-capacity-20260912', 'hil-api-gateway-capacity64-20260912',
        'hil-api-gateway-capacity-ramp-20260912'}


def cgroup_resources(owned):
    def read(item):
        folder = Path('/sys/fs/cgroup/system.slice') / ('docker-' + item['ID'] + '.scope')
        try:
            stat = dict(line.split() for line in (folder / 'memory.stat').read_text().splitlines())
            cpu = dict(line.split() for line in (folder / 'cpu.stat').read_text().splitlines())
            return max(0, int((folder / 'memory.current').read_text()) - int(stat.get('inactive_file', 0))), int(cpu['usage_usec'])
        except (OSError, KeyError, ValueError):
            return None
    started = time.monotonic()
    before = {item['ID']: read(item) for item in owned if item['State'] == 'running' and 'ID' in item}
    if not any(before.values()):
        return []
    time.sleep(1)
    output = []
    for item in owned:
        first = before.get(item.get('ID'))
        if first is None:
            continue
        last = read(item)
        if last is not None:
            output.append({'name': item['Names'], 'memory_bytes': last[0],
                           'cpu_cores': max(0, last[1] - first[1]) / 1e6 / (time.monotonic() - started)})
    return output


def resource_sample():
    owned, containers, errors = [], [], []
    try:
        listing = subprocess.check_output(['docker', 'ps', '-a', '--no-trunc', '--filter', 'name=main01_',
                                           '--filter', 'name=hermes01_', '--filter', 'name=hil-api-gateway-capacity',
                                           '--format', '{{json .}}'], text=True, timeout=20)
        owned = [item for line in listing.splitlines() if is_experiment_container((item := json.loads(line))['Names'])]
    except (subprocess.SubprocessError, OSError, ValueError) as error:
        return [], None, ['container_listing:' + type(error).__name__]
    names = [item['Names'] for item in owned if item['State'] == 'running']
    if not names:
        return [], owned, []
    direct = cgroup_resources(owned)
    if direct:
        return direct, owned, ['cgroup_sample:container_churn'] if len(direct) != len(names) else []
    try:
        # Never query unrelated, possibly paused containers on the shared host.
        sample = subprocess.run(['docker', 'stats', '--no-stream', '--format', '{{json .}}', *names],
                                capture_output=True, text=True, timeout=30)
        stats = sample.stdout
        if sample.returncode:
            errors.append('container_stats:nonzero_exit')
    except (subprocess.SubprocessError, OSError) as error:
        return [], owned, ['container_stats:' + type(error).__name__]
    factors = {'B': 1, 'KiB': 1024, 'MiB': 1024**2, 'GiB': 1024**3}
    for line in stats.splitlines():
        try:
            item = json.loads(line)
            if not is_experiment_container(item['Name']):
                continue
            match = re.fullmatch(r'([0-9.]+)(B|KiB|MiB|GiB)', item['MemUsage'].split(' / ')[0])
            if match is None:
                raise ValueError('Unrecognized Docker memory unit')
            value, unit = match.groups()
            containers.append({'name': item['Name'], 'memory_bytes': float(value) * factors[unit],
                               'cpu_cores': float(item['CPUPerc'].rstrip('%')) / 100})
        except (ValueError, KeyError):
            errors.append('container_stats:invalid_record')
    if len(containers) != len(names):
        errors.append('container_stats:incomplete_sample')
    return containers, owned, errors


def main():
    now = time.time()
    progress = {name: json.loads((ROOT / f'reports/{name}-plan-v1_progress.json').read_text()) for name in ['main', 'hermes']}
    capacity_path = ROOT / 'reports/four-framework-capacity-control.json'
    capacity = json.loads(capacity_path.read_text()) if capacity_path.exists() else {'aggregate_agent_target': 32, 'epoch': 'four-frameworks-32', 'effective_unix': progress['hermes']['started_unix']}
    start = max(now - 600, capacity['effective_unix'])
    seconds = now - start
    rows = [r for p in progress.values() for r in p['results']]
    recent = [r for r in rows if r['finished_unix'] >= start]
    containers, owned, resource_errors = resource_sample()
    resources_available = bool(containers) or not resource_errors
    memory = {line.split(':')[0]: int(line.split()[1]) * 1024 for line in Path('/proc/meminfo').read_text().splitlines()}
    requests = []
    for r in rows:
        if r['finished_unix'] < start:
            continue
        for path in (ROOT / 'gateway_evidence' / r['run_id']).glob('request_*.json'):
            request = json.loads(path.read_text())
            if request.get('finished_unix', 0) >= start:
                requests.append(request)
    report = {'sampled_unix': now, 'aggregate_agent_limit': capacity['aggregate_agent_target'],
              'capacity_epoch': capacity['epoch'],
              'gateway_max_inflight': capacity.get('gateway_max_inflight', 40),
              'new_launches_paused': (ROOT / 'STOP_NEW_RUNS').exists(),
              'scheduled_active_attempts': sum(p.get('active_attempts', 0) for p in progress.values()),
              'agent_states_at_listing': dict(Counter(item['State'] for item in owned if item['Names'].startswith(('main01_', 'hermes01_')))) if owned is not None else None,
              'resource_sample_finished_unix': time.time(),
              'resource_sample_partial': bool(resource_errors),
              'resource_sample_errors': resource_errors,
              'active_agent_containers': sum(c['name'].startswith(('main01_', 'hermes01_')) for c in containers) if resources_available else None,
              'memory_bytes_including_relay': sum(c['memory_bytes'] for c in containers) if resources_available else None,
              'cpu_cores_including_relay': sum(c['cpu_cores'] for c in containers) if resources_available else None,
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
              'caveat': 'Single resource sample; missing Docker samples are null, and partial resource sums cover observed containers only. Scheduled active attempts include startup and cleanup. The trailing window includes carryover attempts and changing case/model mix. Request metrics cover closed attempts only, not active requests. This is not a controlled concurrency comparison.',
              'scaling_status': 'The aggregate target and its effective time are recorded separately from the frozen case and scoring manifests. Larger targets require coordinated pool changes.'}
    output = ROOT / 'reports/api-multimodel-20260912/four-frameworks/capacity_report.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
