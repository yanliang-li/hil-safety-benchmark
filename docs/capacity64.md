# Owner-requested 64-agent execution

The owner explicitly requested 64 concurrent agents after reviewing the earlier 40-agent connection failures. The [64-agent amendment](../experiments/api-multimodel-20260912/capacity-64-amendment-v1.json) records that instruction and the new scheduling and relay limits. The 4,320-attempt original plan and the 1,440-attempt Hermes extension remain unchanged.

## Scheduling and handoff

`scripts/schedule_four_frameworks.py` owns both original scheduler locks and uses one 64-worker pool. Its initial shares are 48 workers for Codex, Claude Code, and DeepSeek Harness together, and 16 for Hermes. It preserves the FIFO order of never-started jobs within each frozen plan. When a queue runs out of new work, spare slots serve the remaining queue. There are never more than 64 submitted, unfinished attempts in this controller.

The previous controllers first stopped launching new tasks and let their running tasks finish. At handoff, all **912 closed attempts** were retained: 816 in the original plan and 96 in the Hermes plan. No agent container or old in-flight relay request remained. The [handoff record](../reports/api-multimodel-20260912/four-frameworks/capacity64-handoff.json) records these checks. The old relay was removed only after it had no remaining requests. No failed attempt is silently retried, overwritten, or reclassified as safe.

The controller verifies both plan hashes, benchmark and adapter source hashes, execution snapshots, and agent image IDs. It resumes only never-started IDs. The case contents, three requested models, neutral and prompt-guard conditions, repeats, per-attempt resource limits, and scoring are unchanged. New attempts record the `four-frameworks-64` epoch and the amendment hash.

## Relay and resources

| Setting | Value |
|---|---|
| Total active agent limit | 64 |
| Relay name | `hil-api-gateway-capacity64-20260912` |
| Relay simultaneous upstream requests | 64 |
| Relay limits | 2 GiB memory, no extra swap, 4 CPUs, 512 processes |
| Each agent | 1,536 MiB memory, no extra swap, 1 CPU, 160 processes |
| Attempt limits | 900 seconds, 48 API requests |
| Launch reserves | At least 64 GiB available host memory and 30 GiB free storage |

The relay uses the same hash-verified byte-passthrough handler and capacity wrapper. Agent containers remain on the dedicated internal network, with read-only root and case mounts and fresh temporary state. Only the relay holds the actual API key. No host port is published. No local model weights or GPU inference are used.

Available-memory, storage, and host-load checks still pause new launches when necessary. Creating the project-root `STOP_NEW_RUNS` file also pauses new launches; active attempts continue under their existing limits. The requested target stays at 64; this controller does not automatically downgrade to the previous 32/40-agent plan based on an early error window.

## Operation and reporting

Once the recorded relay, frozen images, snapshots, and private connection profile are in place, the controller command is:

```bash
python3 scripts/schedule_four_frameworks.py
```

It requires exclusive ownership of both scheduler locks. Do not also run the earlier separate controllers. Control settings live in `reports/four-framework-capacity-control.json`; their aggregate target must match the recorded amendment.

The unified progress file is `reports/unified-plan-v1_progress.json`. It includes aggregate and per-cohort active counts and queue lengths. The original per-cohort progress files remain compatible with the existing independent replay, report, manuscript, and publication watchers. On the execution server, the controller log is `reports/four-frameworks64-controller.log`.

The [capacity report](../reports/api-multimodel-20260912/four-frameworks/capacity_report.json) records observed containers, combined agent/relay memory, host memory, throughput, failures, and API transport errors. Primary outcome tables still exclude failed attempts; the all-attempt audit retains failures and any unsafe actions observed before them.

64 agents do not establish a twofold speedup over 32. API load, network behavior, task mix, startup and drain periods, and the changed relay limits can affect throughput. Calendar windows are operational observations, not a controlled concurrency experiment. The earlier [40-agent failure follow-up](../reports/api-multimodel-20260912/four-frameworks/capacity40-followup.json) remains part of the record.
