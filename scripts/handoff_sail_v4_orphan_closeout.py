"""Close only recorded orphan requests of already terminal failed episodes."""
import hashlib
import json
from pathlib import Path
import time

import handoff_sail_v4_extended as handoff

AMENDMENT = 'experiments/sail-v4-20260913/capacity-v2-orphan-closeout.json'


def ready_with_closed_orphans():
    if is_really_idle():
        return True
    root = handoff.ROOT
    progress = json.loads((root/'reports/sail4-matched-r2_progress.json').read_text())
    if progress['active'] or not handoff.owned_pause():
        return False
    plan = json.loads((root/'experiments/sail-v4-20260913/sail4-matched-r2.json').read_text())
    records = []
    for job in plan['jobs']:
        for suffix in ('', '_guard'):
            for path in (root/'gateway_evidence'/(job['run_id']+suffix)).glob('request_*.json'):
                raw = path.read_bytes()
                row = json.loads(raw)
                if row.get('state') != 'pending':
                    continue
                status = root/'runs'/job['stage']/job['run_id']/'attempt_status.json'
                if not status.exists():
                    return False
                raw_status = status.read_bytes()
                attempt = json.loads(raw_status)
                if attempt.get('completed') is not False or time.time()-attempt.get('finished_unix',time.time()) < 60:
                    return False
                records.append({'request_path':str(path.relative_to(root)),
                    'request_sha256':hashlib.sha256(raw).hexdigest(),
                    'attempt_status_path':str(status.relative_to(root)),
                    'attempt_status_sha256':hashlib.sha256(raw_status).hexdigest(),
                    'attempt_finished_unix':attempt['finished_unix'], 'attempt_completed':False,
                    'request_started_unix':row['started_unix']})
    gateway = handoff.inspect(handoff.GATEWAY)
    status = Path('/proc',str(gateway['State']['Pid']),'status').read_text()
    threads = int(next(x.split()[1] for x in status.splitlines() if x.startswith('Threads:')))
    if not records or threads != len(records)+1:
        return False
    handoff.save(root/'reports/sail4-orphaned-gateway-closeout.json', {
        'recorded_unix':time.time(), 'amendment':AMENDMENT, 'gateway_threads':threads,
        'orphaned_requests':records, 'original_request_records_modified':False,
        'attempt_statuses_modified':False, 'requests_retried':False,
        'reason':'All associated episodes are already terminal failures with no live experiment containers. '
                 'Old gateway shutdown closes residual connections; pending evidence remains missing/partial, not successful.'})
    return True


def main():
    path = handoff.ROOT/AMENDMENT
    value = json.loads(path.read_text())
    if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != value['adapter_sha256']:
        raise ValueError('Closeout adapter source changed')
    original = handoff.gateway_idle
    # Retain the actual idle check without recursing through the adapter.
    globals()['is_really_idle'] = original
    handoff.gateway_idle = lambda: ready_with_closed_orphans()
    handoff.main()


# The readiness function uses this separate reference after installation.
is_really_idle = handoff.gateway_idle


if __name__ == '__main__':
    main()
