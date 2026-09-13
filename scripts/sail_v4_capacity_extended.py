"""Explicit scheduling amendment; preserve the frozen launcher and episodes."""
import json
from pathlib import Path
import time

import sail_v4_capacity as frozen

AMENDMENT = 'experiments/sail-v4-20260913/capacity-amendment-v2.json'


class ExtendedCapacityPolicy:
    levels = (32, 64, 96, 128, 160, 192, 224, 256)

    def __init__(self, initial=128, maximum=256):
        if initial not in self.levels or maximum != 256:
            raise ValueError('Unsupported extended capacity')
        self.target, self.maximum = initial, maximum
        self.healthy = []
        self.trial = []
        self.reference = None
        self.cooldown = {}

    def backoff(self, now):
        self.cooldown[self.target] = now + 1800
        self.target = self.levels[max(0, self.levels.index(self.target) - 1)]
        self.healthy.clear()
        self.trial.clear()
        self.reference = None

    @staticmethod
    def summary(windows):
        seconds = sum(w['elapsed_s'] for w in windows)
        closed = sum(w.get('closed_attempts', 0) for w in windows)
        return {'request_rate': sum(w['requests'] - w['errors'] for w in windows) / max(seconds, 1),
                'valid_rate': sum(w.get('valid_attempts', 0) for w in windows) / max(seconds, 1),
                'closed': closed,
                'failure_rate': sum(w.get('failed_attempts', 0) for w in windows) / closed if closed else 0}

    def observe(self, window, resource_ready, memory_gib, active, now):
        if not resource_ready or window.get('oom_attempts', 0) or (
                window['requests'] and window['error_rate'] >= .05):
            self.backoff(now)
            return 'resource_or_api_backoff'
        # Draining a condition or phase is not evidence of capacity regression.
        if active < .8 * self.target or window['requests'] < 50:
            self.healthy.clear()
            self.trial.clear()
            return 'insufficient_sustained_load'
        if self.reference is not None:
            self.trial.append(dict(window))
            if len(self.trial) < 2:
                return 'measuring_extended_capacity'
            current, previous = self.summary(self.trial[-2:]), self.reference
            if (current['request_rate'] < 1.05 * previous['request_rate'] or
                    (current['closed'] >= 20 and previous['closed'] >= 20 and
                     (current['valid_rate'] < .95 * previous['valid_rate'] or
                      current['failure_rate'] > previous['failure_rate'] + .05))):
                self.backoff(now)
                return 'no_gain_or_more_failed_attempts_backoff'
            # Reuse the two successful measurement windows as the baseline
            # for the next step; no unmeasured jump over a level is allowed.
            self.healthy = self.trial[-2:]
            self.trial = []
            self.reference = None
        else:
            self.healthy.append(dict(window))
        if len(self.healthy) < 2 or self.target == self.maximum:
            return 'hold'
        candidate = self.levels[self.levels.index(self.target) + 1]
        if now < self.cooldown.get(candidate, 0):
            return 'capacity_trial_cooldown'
        if memory_gib < 64 + max(0, candidate - active) * 1.5:
            return 'insufficient_ramp_memory_headroom'
        if candidate > 128:
            self.reference = self.summary(self.healthy[-2:])
        self.target = candidate
        self.healthy.clear()
        return 'healthy_capacity_increase'


def set_extended_gateway(target, stage):
    path = frozen.native.ROOT / 'reports/four-framework-capacity-control.json'
    value = json.loads(path.read_text())
    if value.get('gateway_capacity_ceiling') != 256:
        raise ValueError('Extended gateway has not been installed')
    value.update(gateway_max_inflight=max(64, target), aggregate_agent_target=target,
                 active_experiment=stage, effective_unix=time.time(),
                 capacity_authorization=AMENDMENT)
    frozen.native.save(path, value)


def outcome_window(original, jobs, since):
    window = original(jobs, since)
    rows = []
    for job in jobs:
        path = frozen.native.ROOT / 'runs' / job['stage'] / job['run_id'] / 'attempt_status.json'
        if not path.exists() or path.stat().st_mtime < since:
            continue
        try:
            row = json.loads(path.read_text())
        except (ValueError, OSError):
            continue
        if row.get('finished_unix', 0) >= since:
            rows.append(row)
    valid = sum(bool(r.get('completed')) for r in rows)
    window.update(closed_attempts=len(rows), valid_attempts=valid,
                  failed_attempts=len(rows) - valid,
                  oom_attempts=sum(bool(r.get('oom_killed')) for r in rows))
    return window
