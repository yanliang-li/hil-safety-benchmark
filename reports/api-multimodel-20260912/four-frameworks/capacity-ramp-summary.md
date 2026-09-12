# Completed 64/96/128 capacity comparison

The staged check retained **96 concurrent agents**. The 96-agent observation produced about 19% more valid completions per hour than the 64-agent reference. The extended 128-agent observation produced about 12% fewer than 96, so the controller returned to 96 without cancelling active work.

| Target | Measured window | Closed attempts | Valid | Failed | Valid attempts/hour |
|---|---:|---:|---:|---:|---:|
| 64 | 10 min | 220 | 212 | 8 | 1272 |
| 96 | 5 min | 128 | 126 | 2 | 1512 |
| 128 | 10 min | 230 | 222 | 8 | 1332 |

The 128-agent ten-minute window includes its first five-minute window; those counts must not be added together. The first five minutes yielded 1,176 valid completions/hour. Request transport-error rates were about 0.21%, 0.33%, and 0.47% in the 64, 96, and extended 128 windows. No HTTP errors or out-of-memory failures were observed in the covered window records. The 128 window retained eight failed attempts: five upstream transport errors, two output-limit terminations, and one other incomplete run.

At the extended 128 checkpoint, the host still had 146.1 GiB available memory and a load of 13.45 across 152 logical CPUs. Many submitted attempts were waiting for Docker startup: 67 containers were still in the created state in the checkpoint listing. A nearby diagnostic found a median created-container age of 95.5 seconds and a 95th percentile of 197.5 seconds. These observations make memory exhaustion an unsupported explanation for the slowdown. They do not isolate the causal contribution of Docker contention, changing case mix, or external serving load.

Container memory and CPU samples were partial because containers started and exited during sampling. Their sums are not full-pool peak measurements. The concurrency limit counts submitted unfinished attempts, including startup and cleanup. After reducing 128 to 96, the old attempts finish naturally before the controller replenishes at the lower limit.

The original case manifests, images, per-attempt adapters, model IDs, conditions, repeats, quotas and primary scoring remain unchanged. All attempts and their gateway evidence are retained. These operational comparisons are not randomized concurrency experiments or evidence of a safety improvement. The earlier 128-agent time estimate was a projection; measured throughput did not support keeping that target on this host during these windows.

Evidence: `capacity-ramp-64-reference.json`, `capacity-ramp-96-window1.json`, `capacity-ramp-128-window1.json`, `capacity-ramp-128-window2.json`, `capacity-ramp-decisions.json`, and `capacity-ramp-startup-diagnostic.json`.
