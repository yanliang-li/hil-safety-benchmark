# Staged 96- and 128-agent execution

The owner accepted a staged increase from 64 to 96 agents, followed by 128 if measured useful throughput improves without excessive errors or resource pressure. The [amendment](../experiments/api-multimodel-20260912/capacity-ramp-amendment-v1.json) preserves both experiment plans, their cases, native framework images, per-attempt limits, and primary scoring. No new attempts or retries are added.

The [64-agent reference](../reports/api-multimodel-20260912/four-frameworks/capacity-ramp-64-reference.json) contains 220 closed attempts over 600 seconds, with 212 valid and eight failed attempts: 1,272 valid attempts per hour. Seven failures were output-limit terminations and one was an upstream transport error. Four transport-error requests occurred among 1,868 covered requests. This operational window is a reference for throughput, not a controlled safety comparison.

## Handoff and live limits

The old controller first stops new launches and lets registered attempts and their relay requests finish. Its scheduler locks are then released. The new `scripts/schedule_four_frameworks_ramp.py` verifies frozen source and case hashes, image IDs, runner snapshots, the amendment, and existing attempt identities before resuming only never-started IDs.

One thread pool has a maximum of 128 unfinished attempts. The initial 96-agent allocation gives 72 slots to the original Codex/Claude Code/DeepSeek Harness plan and 24 to Hermes. At 128, the shares become 96 and 32. FIFO order remains unchanged within each plan. Spare slots serve the other plan when one queue is exhausted.

The controller and relay read the same atomically replaced `reports/four-framework-capacity-control.json`. A shared admission semaphore accepts only the recorded 64, 96, or 128 limits. Increasing the target does not restart active agents or requests. Decreasing it waits for existing work to finish before filling fewer slots; it does not cancel admitted work.

The relay uses the hash-verified original byte-passthrough protocol handler, with a 128-request ceiling, four CPUs, a 4 GiB memory limit without extra swap, and a 1,024-process limit. It alone holds the real API credential. Agent containers retain one CPU, 1,536 MiB memory without extra swap, 160 processes, a 900-second limit, and the 48-request quota.

New launches still require 64 GiB available host memory, 30 GiB free project storage, and a host load below 75% of the logical CPU count. Per-attempt capacity fields describe launch settings. A request from an existing attempt can encounter a new admission limit after a live change. Capacity history and checkpoint timestamps preserve this operational confound.

## Checkpoint rules

`scripts/observe_capacity_ramp.py` follows the recorded rules:

1. Allow 120 seconds for startup, then observe at least 300 seconds and 80 closed attempts.
2. Require at least 10% more valid completions per hour than the preceding reference.
3. Require transport and HTTP error rates of at most 1% each among the covered requests. Failed-attempt rate may increase by at most five percentage points. No out-of-memory failure is accepted.
4. Require at least 96 GiB available host memory for promotion, adequate disk space, and acceptable host load.
5. If only the observation length or throughput gain is marginal, collect one additional 300-second window. If the requirements still fail, return to the preceding target.
6. After promotion to 128, apply the same checks against the successful 96-agent window before retaining 128. Otherwise return to 96.

Thus the first decision occurs about seven minutes after a target change, plus measurement overhead. The observer checks for external control changes and stops rather than overwriting them. The experiment controller continues to enforce resource guards independently of the observer.

The live observer state is `reports/capacity-ramp-observer.json`; its log is `reports/capacity-ramp-observer.log`. The experiment controller log is `reports/four-frameworks-ramp-controller.log`. Public checkpoint files and `capacity-ramp-decisions.json` are in the [four-framework report directory](../reports/api-multimodel-20260912/four-frameworks/).

Throughput and error checks are operational safeguards. They are not statistical confidence tests, proof of provider capacity, or evidence that concurrency caused a safety difference. Task mix, incomplete long attempts, calendar time, and serving load can affect comparisons. All failed attempts remain in the full audit; incomplete traces are not counted as valid safe outcomes.
