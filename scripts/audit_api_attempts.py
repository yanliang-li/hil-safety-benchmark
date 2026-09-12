"""Supplementary failure and resource audit; does not change frozen primary scoring."""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import time

from hil_safety_bench.evaluate import evaluate_run

ROOT = Path(__file__).resolve().parents[1]


def safety_bounds(valid_unsafe, valid_count, failed_unsafe, failed_count):
    """Bounds among closed attempts; an observed unsafe action remains evidence."""
    assert 0 <= valid_unsafe <= valid_count
    assert 0 <= failed_unsafe <= failed_count
    denominator = valid_count + failed_count
    return {
        "denominator_closed_attempts": denominator,
        "lower_numerator": valid_unsafe + failed_unsafe,
        "upper_numerator": valid_unsafe + failed_count,
        "lower": (valid_unsafe + failed_unsafe) / denominator if denominator else None,
        "upper": (valid_unsafe + failed_count) / denominator if denominator else None,
    }


def records_for(run_id):
    return [json.loads(p.read_text()) for p in sorted(
        (ROOT / 'gateway_evidence' / run_id).glob('request_*.json'))]


def last_finish_reasons(record):
    raw = record.get('raw_response', '')
    objects = []
    try:
        objects.append(json.loads(raw))
    except ValueError:
        for line in raw.splitlines():
            if line.startswith('data:'):
                try:
                    objects.append(json.loads(line[5:]))
                except ValueError:
                    pass
    reasons = set()
    for obj in objects:
        if not isinstance(obj, dict):
            continue
        for choice in obj.get('choices', []):
            if choice.get('finish_reason'):
                reasons.add(choice['finish_reason'])
        for child in [obj, obj.get('delta', {}), obj.get('message', {})]:
            if isinstance(child, dict) and child.get('stop_reason'):
                reasons.add(child['stop_reason'])
    return sorted(reasons)


def main():
    plan_path = ROOT / 'experiments/api-multimodel-20260912/main-plan-v1.json'
    plan = json.loads(plan_path.read_text())
    rows, groups = [], defaultdict(Counter)
    for job in plan['jobs']:
        group = groups[(job['agent'], job['model'], job['condition'])]
        group['planned'] += 1
        folder = ROOT / 'runs' / job['stage'] / job['run_id']
        status_path = folder / 'attempt_status.json'
        if not status_path.exists():
            group['pending'] += 1
            continue
        state = json.loads(status_path.read_text())
        meta_path = folder / 'run_metadata.json'
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        valid = bool(state.get('completed'))
        group['valid' if valid else 'failed'] += 1
        records = records_for(job['run_id'])
        final = records[-1] if records else {}
        reasons = last_finish_reasons(final)
        observed = None
        events_path = folder / 'events.jsonl'
        if events_path.exists():
            # An incomplete trace can establish an executed unsafe action, but
            # its absence cannot establish a successfully safe completion.
            observed = evaluate_run(ROOT / 'data/cases' / job['case_id'], folder).unsafe_attack_success
        elif valid:
            raise ValueError('Valid attempt lacks events: ' + job['run_id'])
        group['valid_unsafe' if valid else 'failed_observed_unsafe'] += int(observed is True)
        if valid:
            cause = 'valid'
        elif state.get('docker_state', {}).get('OOMKilled'):
            cause = 'out_of_memory'
        elif meta.get('timed_out'):
            cause = 'attempt_timeout'
        elif final.get('state') == 'transport_error':
            cause = 'upstream_transport_error'
        elif final.get('http_status', 200) >= 400:
            cause = 'upstream_http_error'
        elif set(reasons) & {'length', 'max_tokens'}:
            cause = 'output_limit_termination'
        else:
            cause = 'other_incomplete_framework_run'
        group['cause_' + cause] += 1
        input_tokens = output_tokens = usage_records = 0
        for record in records:
            usage = record.get('usage')
            if usage:
                usage_records += 1
                input_tokens += usage.get('input_tokens', usage.get('prompt_tokens', 0)) or 0
                output_tokens += usage.get('output_tokens', usage.get('completion_tokens', 0)) or 0
        group['requests_all_closed_attempts'] += len(records)
        group['requests_with_usage'] += usage_records
        group['reported_input_tokens'] += input_tokens
        group['reported_output_tokens'] += output_tokens
        rows.append({k: job[k] for k in ['run_id', 'agent', 'model', 'condition', 'case_id', 'repeat']} | {
            'completed_valid': valid, 'failure_category': cause,
            'observed_unsafe_in_available_trace': observed,
            'events_sha256': hashlib.sha256(events_path.read_bytes()).hexdigest() if events_path.exists() else '',
            'wall_seconds': state['finished_unix'] - state['started_unix'],
            'memory_peak_bytes': meta.get('cgroup_memory_peak'),
            'api_requests': len(records), 'requests_with_usage': usage_records,
            'reported_input_tokens': input_tokens, 'reported_output_tokens': output_tokens,
            'last_http_status': final.get('http_status'),
            'last_gateway_state': final.get('state'),
            'last_finish_reasons': ','.join(reasons),
        })
    report = {
        'created_unix': time.time(), 'plan_sha256': hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        'analysis_status': 'Supplementary analysis added after initial failures; frozen primary analysis unchanged.',
        'bounds_interpretation': 'Among closed attempts only. Lower bound includes unsafe actions observed before failed termination. Upper bound treats every remaining failed attempt as unsafe. Pending attempts are excluded. These are sensitivity bounds, not confidence intervals or imputed outcomes.',
        'usage_interpretation': 'Reported usage across all closed attempts, including failed attempts and CLI retries. Missing usage is not estimated. Not a monetary cost estimate.',
        'groups': [],
    }
    for (agent, model, condition), group in sorted(groups.items()):
        report['groups'].append(dict(agent=agent, model=model, condition=condition, **group,
            unsafe_sensitivity=safety_bounds(group['valid_unsafe'], group['valid'],
                                             group['failed_observed_unsafe'], group['failed'])))
    output = ROOT / 'reports/api-multimodel-20260912/main'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'attempt_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    if rows:
        with (output / 'all_attempts.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps({'audited_closed_attempts': len(rows), 'failure_categories': dict(Counter(
        r['failure_category'] for r in rows if not r['completed_valid']))}))


if __name__ == '__main__':
    main()
