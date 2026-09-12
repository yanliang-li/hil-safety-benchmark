"""Apply the recorded 96/128 throughput checks and preserve their decisions."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports/api-multimodel-20260912/four-frameworks'
CONTROL = ROOT / 'reports/four-framework-capacity-control.json'
AMENDMENT = ROOT / 'experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json'


def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def assess(sample, reference, rule):
    failures = []
    if sample['window_seconds'] < rule['minimum_measurement_seconds'] or sample['recent_closed'] < rule['minimum_closed_attempts']:
        failures.append('insufficient_observation')
    if sample['valid_per_hour'] < rule['minimum_valid_throughput_ratio_to_previous'] * reference['valid_per_hour']:
        failures.append('insufficient_valid_throughput_gain')
    if sample['host_available_memory_gib'] < rule['minimum_available_host_memory_gib_for_promotion'] or sample['free_project_disk_gib'] < 30 or sample['host_load_1m'] >= .75 * sample['logical_cpus']:
        failures.append('host_resource_pressure')
    if sample['failure_categories'].get('out_of_memory', 0):
        failures.append('out_of_memory')
    for metric, threshold in [('transport_error_rate', 'maximum_transport_request_error_rate'), ('http_error_rate', 'maximum_http_request_error_rate')]:
        if sample[metric] is None or sample[metric] > rule[threshold]:
            failures.append(metric)
    if sample['failed_attempt_rate'] is None or sample['failed_attempt_rate'] > reference['failed_attempt_rate'] + rule['maximum_failed_attempt_rate_increase']:
        failures.append('increased_failed_attempt_rate')
    return failures


def change_target(expected, target, reason):
    current = json.loads(CONTROL.read_text())
    if current != expected:
        raise ValueError('Control changed externally; do not overwrite another operator')
    control = dict(current, aggregate_agent_target=target, main_workers=3 * target // 4,
                   hermes_workers=target // 4, gateway_max_inflight=target,
                   effective_unix=time.time(), epoch=f'four-frameworks-{target}', reason=reason)
    save(CONTROL, control)
    save(ROOT / 'reports/capacity-control.json', dict(control, agent_concurrency=control['main_workers']))
    return control


def observe(control, reference, rule, state):
    start = control['effective_unix'] + rule['warmup_seconds']
    for window_number in (1, 2):
        deadline = start + window_number * rule['minimum_measurement_seconds']
        while time.time() < deadline:
            if json.loads(CONTROL.read_text()) != control:
                raise ValueError('Control changed externally during observation')
            state.update(status='observing', target=control['aggregate_agent_target'],
                         measurement_start_unix=start, next_checkpoint_unix=deadline, checked_unix=time.time())
            save(ROOT / 'reports/capacity-ramp-observer.json', state)
            time.sleep(min(15, max(.1, deadline - time.time())))
        label = f"capacity-ramp-{control['aggregate_agent_target']}-window{window_number}"
        result = subprocess.run(['python3', 'scripts/sample_capacity_ramp.py', '--start', str(start),
                                 '--end', str(time.time()), '--label', label], cwd=ROOT,
                                text=True, capture_output=True, check=True, timeout=90)
        sample = json.loads(result.stdout)
        failures = assess(sample, reference, rule)
        decision = {'sample': label + '.json', 'target': control['aggregate_agent_target'],
                    'failures': failures, 'valid_throughput_ratio': sample['valid_per_hour'] / reference['valid_per_hour'],
                    'checked_unix': time.time()}
        state['checks'].append(decision)
        save(ROOT / 'reports/capacity-ramp-observer.json', state)
        save(REPORTS / 'capacity-ramp-decisions.json', state)
        print(json.dumps(decision), flush=True)
        if not failures:
            return sample, True
        if set(failures) - {'insufficient_observation', 'insufficient_valid_throughput_gain'}:
            return sample, False
        # A startup-affected or marginal first window gets one additional window.
    return sample, False


def main():
    amendment = json.loads(AMENDMENT.read_text())
    state = {'checks': [], 'amendment_sha256': hashlib.sha256(AMENDMENT.read_bytes()).hexdigest(),
             'observer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'status': 'waiting_for96'}
    save(ROOT / 'reports/capacity-ramp-observer.json', state)
    while True:
        control = json.loads(CONTROL.read_text())
        if control['aggregate_agent_target'] == 96 and control['gateway_name'] == amendment['gateway']['name']:
            break
        time.sleep(10)
    reference = json.loads((REPORTS / 'capacity-ramp-64-reference.json').read_text())
    rule = amendment['checkpoint_rule']
    try:
        sample96, passed = observe(control, reference, rule, state)
        if not passed:
            control = change_target(control, 64, '96-agent checkpoint did not meet the recorded throughput/resource/error conditions')
        else:
            control = change_target(control, 128, '96-agent checkpoint passed the recorded throughput/resource/error conditions')
            state.update(status='observing128', promoted_unix=control['effective_unix'])
            save(ROOT / 'reports/capacity-ramp-observer.json', state)
            sample128, passed = observe(control, sample96, rule, state)
            if not passed:
                control = change_target(control, 96, '128-agent checkpoint did not meet the recorded throughput/resource/error conditions')
        state.update(status='complete', retained_target=control['aggregate_agent_target'],
                     completed_unix=time.time(), control=control)
    except Exception as error:
        state.update(status='error', error=type(error).__name__, checked_unix=time.time())
        raise
    finally:
        save(ROOT / 'reports/capacity-ramp-observer.json', state)
        save(REPORTS / 'capacity-ramp-decisions.json', state)


if __name__ == '__main__':
    main()
