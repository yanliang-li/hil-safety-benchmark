"""Record throughput, operational failures and resources without raw model content."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from audit_api_attempts import last_finish_reasons
from report_four_framework_capacity import resource_sample


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=float, required=True)
    parser.add_argument('--end', type=float)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', args.label):
        raise ValueError('Invalid checkpoint label')
    end = args.end or time.time()
    duration = end - args.start
    if duration <= 0:
        raise ValueError('Nonpositive observation window')
    progress = [json.loads((ROOT / f'reports/{name}-plan-v1_progress.json').read_text()) for name in ['main', 'hermes']]
    rows = [row for item in progress for row in item['results']]
    recent = [row for row in rows if args.start <= row['finished_unix'] <= end]
    causes, request_states, statuses = Counter(), Counter(), Counter()
    for row in recent:
        folder = ROOT / 'runs' / row['stage'] / row['run_id']
        meta_path = folder / 'run_metadata.json'
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        records = [json.loads(p.read_text()) for p in sorted((ROOT / 'gateway_evidence' / row['run_id']).glob('request_*.json'))]
        final = records[-1] if records else {}
        if row['completed']:
            cause = 'valid'
        elif row.get('docker_state', {}).get('OOMKilled'):
            cause = 'out_of_memory'
        elif meta.get('timed_out'):
            cause = 'attempt_timeout'
        elif final.get('state') == 'transport_error':
            cause = 'upstream_transport_error'
        elif (final.get('http_status') or 200) >= 400:
            cause = 'upstream_http_error'
        elif set(last_finish_reasons(final)) & {'length', 'max_tokens'}:
            cause = 'output_limit_termination'
        else:
            cause = 'other_incomplete_framework_run'
        causes[cause] += 1
        for record in records:
            if args.start <= record.get('finished_unix', 0) <= end:
                request_states[record['state']] += 1
                statuses[str(record.get('http_status'))] += 1
    closed_ids = {row['run_id'] for row in rows}
    pending_ages = []
    for path in (ROOT / 'registry').glob('*.json'):
        if path.stem in closed_ids or not path.stem.startswith(('main01_', 'hermes01_')):
            continue
        for request in (ROOT / 'gateway_evidence' / path.stem).glob('request_*.json'):
            record = json.loads(request.read_text())
            if record['state'] == 'pending':
                pending_ages.append(time.time() - record['started_unix'])
    containers, owned, errors = resource_sample()
    mem = int(next(line.split()[1] for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith('MemAvailable:'))) * 1024
    requests = sum(request_states.values())
    transport = request_states['transport_error']
    http_errors = sum(count for status, count in statuses.items() if status.isdigit() and int(status) >= 400)
    valid = causes['valid']
    report = {
        'label': args.label, 'sampled_unix': time.time(), 'window_start_unix': args.start,
        'window_end_unix': end, 'window_seconds': duration,
        'control_at_sampling': json.loads((ROOT / 'reports/four-framework-capacity-control.json').read_text()),
        'closed_total': len(rows), 'planned': sum(item['planned'] for item in progress),
        'recent_closed': len(recent), 'recent_valid': valid, 'recent_failed': len(recent) - valid,
        'valid_per_hour': valid * 3600 / duration,
        'closed_per_hour': len(recent) * 3600 / duration,
        'failed_attempt_rate': (len(recent) - valid) / len(recent) if recent else None,
        'failure_categories': dict(causes), 'closed_attempt_request_states': dict(request_states),
        'closed_attempt_http_statuses': dict(statuses),
        'transport_error_rate': transport / requests if requests else None,
        'http_error_rate': http_errors / requests if requests else None,
        'pending_requests_at_sampling': len(pending_ages),
        'oldest_pending_request_seconds': max(pending_ages, default=0),
        'host_available_memory_gib': mem / 1024**3,
        'free_project_disk_gib': shutil.disk_usage(ROOT).free / 1024**3,
        'host_load_1m': os.getloadavg()[0], 'logical_cpus': os.cpu_count(),
        'sampled_containers': len(containers),
        'sampled_memory_gib': sum(c['memory_bytes'] for c in containers) / 1024**3 if containers else None,
        'sampled_cpu_cores': sum(c['cpu_cores'] for c in containers) if containers else None,
        'resource_sample_errors': errors,
        'agent_states_at_listing': dict(Counter(item['State'] for item in owned if item['Names'].startswith(('main01_', 'hermes01_')))) if owned is not None else None,
        'caveat': 'Operational observation, not a controlled concurrency experiment. Case mix and calendar serving load vary. Request error rates cover requests from attempts closed in the window; pending ages are sampled separately. Cgroup resources exclude host daemon/controller overhead and may miss container churn.'}
    dest = ROOT / 'reports/api-multimodel-20260912/four-frameworks' / (args.label + '.json')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
