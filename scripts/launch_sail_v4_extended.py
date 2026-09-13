"""Apply the published capacity adapter to the unchanged frozen launch loop."""
import hashlib
import json
import sys
import time

import launch_sail_v4_sequential as entry
import sail_v4_capacity as frozen
from sail_v4_capacity_extended import AMENDMENT, ExtendedCapacityPolicy, outcome_window, set_extended_gateway


def verify_amendment():
    root = frozen.native.ROOT
    path = root / AMENDMENT
    value = json.loads(path.read_text())
    for rel, expected in value['source_sha256'].items():
        if hashlib.sha256((root / rel).read_bytes()).hexdigest() != expected:
            raise ValueError('Capacity amendment source changed: ' + rel)
    plan = root / 'experiments/sail-v4-20260913/sail4-matched-r2.json'
    if hashlib.sha256(plan.read_bytes()).hexdigest() != value['frozen_plan_sha256']:
        raise ValueError('Original formal plan changed')
    return value


def main():
    value = verify_amendment()
    frozen.native.save(frozen.native.ROOT / 'reports/sail4-capacity-extension-applied.json',
                       {'applied_unix': time.time(), 'amendment': AMENDMENT,
                        'source_sha256': value['source_sha256'],
                        'frozen_plan_sha256': value['frozen_plan_sha256'],
                        'initial_concurrency': 128, 'maximum_concurrency': 256,
                        'episode_runtime_changed': False})
    original_window = frozen.native.api_window
    frozen.native.api_window = lambda jobs, since: outcome_window(original_window, jobs, since)
    frozen.CapacityPolicy = ExtendedCapacityPolicy
    frozen.set_gateway = set_extended_gateway
    entry.main()


if __name__ == '__main__':
    main()
