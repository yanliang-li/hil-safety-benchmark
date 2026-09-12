# Resource assessment before considering 128 agents

The running experiment remains at **64 submitted, unfinished attempts**. No 96- or 128-agent safety run or load test has been performed. These observations do not authorize or record a new capacity phase.

At the throughput snapshot, 1,366 of 5,760 attempts had closed, leaving 4,394. The trailing 600 seconds contained 222 closed attempts: 209 valid and 13 failed. The independent failure audit classified 11 as output-limit terminations and two as other incomplete framework runs. None was an out-of-memory failure. Five transport-error request records were observed, including errors within attempts that could later finish; request errors and failed attempts have different denominators.

The resource snapshot covered 59 agent cgroups and the relay as containers started and exited. Their combined current memory was 8.97 GiB, including file cache; working-set memory was 8.55 GiB. Over the two-second sample, these cgroups used 2.51 CPU cores. The whole host used about 9.18 of 152 logical cores and had 152.49 GiB available memory. No swap-in or swap-out pages were recorded during the sample. This is a short observation, not a guaranteed peak bound, and host Docker/controller overhead is outside the agent cgroup sum.

Mean current memory per sampled agent was approximately 77 MiB for Codex, 160 MiB for Claude Code, 136 MiB for DeepSeek Harness, and 222 MiB for Hermes. The relay used 686 MiB including file cache (262 MiB working set). Each agent still has a 1,536 MiB limit. At the observed task mix, 128 agents would plausibly use about 18–22 GiB including the relay; that is an extrapolation, not a measured reservation or upper bound. All 128 agent memory limits plus the relay would instead total 194 GiB, so simultaneous maximum allocations must not be assumed available on this shared host.

Model inference runs at the supplied API endpoint, without local GPU inference. CPU, memory, container lifecycle work, filesystem I/O, network connections, and remote API capacity all matter. Successful request median durations were about 4.8–6.7 seconds, with 95th percentiles of 49–84 seconds by model. These durations include relay waiting and response streaming. There were 51 pending request records at the snapshot. No HTTP 429 was observed in the covered request records; this does not establish capacity at 128 agents.

## Conditional time estimates

| Aggregate target | Measurement status | Remaining time estimate |
|---|---|---|
| 64 | Measured: 1,332 closed / 1,254 valid attempts per hour in this window | About 3.5–5 hours, allowing for task mix and tail effects |
| 96 | Not measured | About 2.5–4 hours if higher concurrency increases useful throughput |
| 128 | Not measured | About 2–3.5 hours if the provider sustains roughly 1.5–2 times current throughput; ideal linear closure alone is 1.65 hours |

The 96/128 estimates are scenarios, not confidence intervals. Provider overload can erase the expected gain or make completion slower. The current controller and relay are both capped at 64. An actual increase requires a new recorded amendment and coordinated scheduling and relay changes, while retaining original cases, images, per-attempt limits, scoring, and prior failures. A short 96-agent window followed by 128, evaluated using valid completions per hour and failure causes, would provide stronger operational evidence than assuming linear scaling.

The resource monitor now filters experiment container names before querying Docker, to avoid scanning unrelated containers on the shared host. Missing resource observations remain explicitly unavailable; they do not stop outcome analysis or publication.

Evidence: `capacity128-assessment-resources.json`, `capacity128-assessment-throughput.json`, and `capacity128-assessment-failures.json`. All were collected at a 64-agent target.
