# InterveneBench v2.2 formal launch record

Launch date: 2026-09-14 (Asia/Shanghai)

Status in this file is a launch-time record, not a live dashboard. The live
machine-readable status is
`/home/root123/intervene-v1-20260914/reports/formal_plan.v22_progress.json` on
the experiment server.

## Frozen inputs

- Plan: `formal_plan.v22.json`
- Plan SHA-256:
  `fafb96011e68af924f425c774709e20b6673702e09b8aa1b15f7427046649480`
- Case-bank JSONL SHA-256:
  `1c77bed9dc899683841dd4d37a58a581fd3a951afd73eac52d7848172e2a3a6e`
- Suite-manifest SHA-256:
  `2604894b76a34e944ff959176d1b9fd1f75d09824c7578483f7fdb0f680c566b`
- Container image ID:
  `sha256:cef9c75343a0fd7f84e735ae4002a69b8d812d9becf3175bf029504852030c46`
- Source inventory: 42 hashed files; zero local/server mismatches before
  launch.
- Accepted preflight: `preflight_acceptance.v22.json`, status `pass`.

## Allocation

| Arm | Attempts |
|---|---:|
| Neutral | 360 |
| Prompt-only guard | 360 |
| Full SAIL-HIL | 360 |
| SAIL-HIL without controller clarification | 360 |
| SAIL-HIL without safe recovery | 360 |
| Risk oracle | 120 |
| SAIL-HIL without human feedback | 60 |
| **Total** | **1,980** |

The five main arms cross 120 cases and three repeats. The risk oracle uses one
attempt per case. The no-human arm uses the observationally sufficient
direct-denial case for each task and three repeats.

## Runtime policy

- Native actor: Codex CLI with requested route `glm-5.2`.
- SAIL reviewer: requested route `deepseek-v4-flash`.
- Total launcher concurrency: 4.
- Per-attempt timeout: 900 seconds.
- No automatic retry after a run ID has been registered.
- Failed attempts stay in the planned denominator and receive an explicit
  failure category plus missing-outcome bounds.
- No runtime, scorer, task, response-bank, or analysis-source change is allowed
  after this launch.

## Analysis contract

Only successful, replayable attempts enter valid-run point estimates. Primary
comparisons pair case and repeat, average policy/repeat differences within each
`task_id`, and bootstrap equal-weight task means. The final report must include
all planned, valid, failed, and pending counts; failure categories; task-cluster
intervals; and best/worst missing-outcome bounds. Preflight trajectories are
excluded.

## Scheduler continuity incident

The initial launcher was attached to a foreground SSH/Codex execution session.
That client-side session later disappeared, leaving a stale progress snapshot
at 28 recorded results and no live launcher or containers. All 31 attempts that
had actually been registered already possessed terminal `attempt_status.json`
files: 28 were valid and three were agent timeouts. There were zero registered
formal run IDs without a terminal status.

Before resuming, the stale report was preserved as
`formal_plan.v22_progress.before-detached-resume.json`. The same frozen plan was
then restarted under a server-side detached session. The launcher loaded all 31
existing terminal statuses and began with the next unregistered run ID; no
attempt was retried or replaced. The detached launcher PID at verification was
2016915 (parent PID 1, session ID 2016915), with four experiment containers and
a refreshing progress file. This is a scheduler-continuity incident, not an
agent outcome, and must be reported separately from the three registered agent
timeouts.

## User-authorized concurrency ramp

The user subsequently requested a staged concurrency increase using the same
multi-model API. A `STOP_INTERVENE` gate first prevented new dispatches while
the four active attempts were allowed to terminate under their original
900-second limit. At the switch boundary there were 37 terminal attempts (32
valid and five failed) and zero registered run IDs without terminal status.
The progress report was preserved as
`formal_plan.v22_progress.before-concurrency8.json`.

The concurrency-4 launcher was then terminated while idle and the same frozen
plan was resumed in a detached server session with concurrency 8. It loaded all
37 terminal attempts and launched only previously unregistered run IDs. The
verified launcher PID was 2172500 (parent PID 1, session ID 2172500), with eight
experiment containers and a continuously refreshed progress report. Actor and
reviewer routes, cases, prompts, timeouts, scorers, source hashes, and the
no-retry policy did not change. Because API load changed during the experiment,
the final limitations must report this operational phase boundary and audit
failure rates before and after the ramp.

After 82 concurrency-8 terminal attempts had accumulated, 70 were valid and
12 failed. Five failed trajectories contained reviewer-side rate-limit text;
all five belonged to SAIL conditions and appeared only in `guard_events.jsonl`.
To increase total throughput without doubling pressure on that bottleneck, the
user authorized a further route-aware ramp. The concurrency-8 queue was paused
and all eight active attempts again terminated naturally. At this second switch
boundary there were 128 terminal attempts (108 valid and 20 failed) and zero
registered run IDs without terminal status. The snapshot is
`formal_plan.v22_progress.before-route-shards.json`.

Two mutually exclusive scheduler manifests were derived from the unchanged
parent allocation. `formal_plan.v22-direct-shard.json` contains the 840
neutral, prompt-only, and risk-oracle run IDs (SHA-256
`54354bbb98eab857f1341392f881a7ab5ca6416dd7c44ca275c3d2f893940b0f`)
and runs at concurrency 8. `formal_plan.v22-reviewer-shard.json` contains the
1,140 SAIL-family run IDs (SHA-256
`d1bea11b9fa12b8794a9d0b830c58b802fe9154daa0b20c8577f67a8225ade4a`)
and runs at concurrency 4. Their job sets are disjoint and their union equals
all 1,980 parent-plan run IDs. Total container concurrency is therefore 12,
while reviewer concurrency remains four. Final analysis still uses the parent
plan; the shard manifests only control scheduling. This phase boundary and
route-specific failure rates must remain explicit in the final report.

## User-requested termination

On 2026-09-16, the user requested termination and export to GitHub. A global
stop gate first prevented any new dispatch. The remaining three active reviewer
runs were allowed to reach their existing terminal outcomes, after which the
reviewer launcher was stopped. The direct shard had already completed and its
launcher had exited. Verification found zero live experiment containers and
zero registered run IDs without a stage-resolved terminal status.

The terminal progress contains 1,190/1,980 finished attempts: 859 valid, 331
failed, and 790 never started. The direct shard finished 840/840 (656 valid,
184 failed); the reviewer shard finished 350/1,140 (203 valid, 147 failed).
`reports/intervene-v22-terminated/summary.json` intentionally reports status
`incomplete`. These partial outcomes do not constitute the planned balanced
formal matrix and must not replace the pending stateful results in the paper.
