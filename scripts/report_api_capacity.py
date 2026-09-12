"""Measure capacity stages from completed attempts and relay records, without prompts."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import statistics
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    now = time.time()
    progress = json.loads((ROOT / 'reports/main-plan-v1_progress.json').read_text())
    baseline = json.loads((ROOT / 'reports/capacity-8-baseline.json').read_text())
    history = json.loads((ROOT / 'reports/capacity-history.json').read_text())
    baseline_end = baseline['captured_unix']
    stages = [{'epoch': 'capacity-8-baseline', 'agent_concurrency': 8,
               'start': max(baseline['started_unix'], baseline_end - 600), 'end': baseline_end}]
    for i, entry in enumerate(history):
        stages.append({'epoch': entry['epoch'], 'agent_concurrency': entry['agent_concurrency'],
                       'start': entry['effective_unix'],
                       'end': history[i + 1]['effective_unix'] if i + 1 < len(history) else now})
    requests = []
    for p in (ROOT / 'gateway_evidence').glob('main01_*/request_*.json'):
        r = json.loads(p.read_text())
        if r.get('started_unix', 0) >= stages[0]['start']:
            requests.append({k: r.get(k) for k in ['run_id', 'started_unix', 'finished_unix',
                'state', 'http_status', 'error_type', 'endpoint']})
    results = progress['results']
    report = {'measured_unix': now, 'planned_attempts': progress['planned'],
              'finished_attempts': len(results), 'active_attempts': progress.get('active_attempts'),
              'caveat': 'Short operational windows with different case/model mixes and startup/drain effects. Observed throughput is not a controlled speed benchmark or a safety result.',
              'stages': []}
    for stage in stages:
        start, end = stage['start'], stage['end']
        closed = [r for r in results if start <= r['finished_unix'] < end]
        stage_closed = closed if stage['epoch'] == 'capacity-8-baseline' else [r for r in closed if r.get('capacity_epoch') == stage['epoch']]
        reqs = [r for r in requests if start <= r['started_unix'] < end]
        done = [r for r in reqs if r.get('finished_unix') and r['finished_unix'] <= end]
        latency = [r['finished_unix'] - r['started_unix'] for r in done if r['state'] == 'complete']
        by_agent = defaultdict(list)
        for r in stage_closed:
            by_agent[r['agent']].append(r['finished_unix'] - r['started_unix'])
        duration = max(end - start, .001)
        steady_start = max(start, end - 180)
        tail = [r for r in closed if r['finished_unix'] >= steady_start]
        report['stages'].append(dict(stage, elapsed_seconds=duration,
            closed_attempts=len(closed), valid_attempts=sum(bool(r['completed']) for r in closed),
            failed_attempts=sum(not r['completed'] for r in closed),
            closed_per_hour=len(closed) * 3600 / duration,
            valid_per_hour=sum(bool(r['completed']) for r in closed) * 3600 / duration,
            tail_180_seconds_closed_per_hour=len(tail) * 3600 / max(end - steady_start, .001),
            own_epoch_closed_attempts=len(stage_closed),
            mean_run_seconds_by_agent={k: statistics.mean(v) for k, v in by_agent.items()},
            closed_count_by_agent={k: len(v) for k, v in by_agent.items()},
            api_completed_requests=len(done), api_pending_requests=len(reqs) - len(done),
            api_states=dict(Counter(r['state'] for r in done)),
            api_http_statuses=dict(Counter(str(r['http_status']) for r in done)),
            api_success_latency_median_seconds=statistics.median(latency) if latency else None))
    output = ROOT / 'reports/api-multimodel-20260912/main/capacity_report.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
