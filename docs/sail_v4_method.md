# SAIL v4: preserve original authority and recover task progress

This controller tests a HIL-centered hypothesis: after rejecting an unauthorized extension, explicitly preserve the original task and help the actor complete its remaining authorized work. Improvement is an experimental question, not an implementation guarantee.

## Task and authority state

The controller compiles the original TASK and static tool descriptions before seeing documents or a proposed action. The contract lists consequential effects with object, purpose, scope, literal task evidence, optional exact argument restrictions, and cumulative bounds. Each effect is marked required or optional. Required effects are reconciled into the completion obligations so a requested check cannot disappear from the finish check.

Permission is separate from retrieved workflow instructions. A denied expansion does not revoke a smaller original permission. Explicit revocation is recorded with actual response evidence. A human-approved extension must match the proposed action and its conditions, including total versus additional resource units.

The persistent ledger stores actual response pairs, consumed reply IDs, action signatures, resource reservations, observations, tool feedback, and recovery counts. Reservations are saved before dispatch and retained after uncertain/failed execution. A process lock rejects overlapping controllers for one episode; a later restart reloads the same state and reviewer-call budget.

The controller's semantic decisions remain model-dependent. Literal quotes, exact argument restrictions, one-use permits, and count checks make decisions inspectable and enforce local invariants; they do not prove general semantic authorization or cross-tool equivalence.

## Recovery and completion

A block returns the deferred effect, missing decision, unspent original authority, and task obligations. The reviewer may propose safe next tool calls using public task evidence and successful tool feedback. These are suggestions only: the native actor must submit any call, and every consequential call is checked again.

`finish` checks task-derived obligations against successful tool feedback. Writing that a validation occurred cannot substitute for the validation tool event. At most four recovery events are permitted, including at most two finish repairs. When the repair budget ends, the controller records remaining obligations rather than fabricating completion.

The controller implements five conditions. The user-corrected third round runs only Prompt, SAIL v4, and SAIL v4 without human replies; the other two are retained as code and engineering history:

| Condition | Purpose |
|---|---|
| `prompt_guard_v1` | Fresh unchanged prompt baseline |
| `sail_v3` | Historical controller; no fresh formal arm in this round |
| `sail_v4` | Authority preservation, scoped replies and recovery |
| `sail_v4_no_recovery` | Implemented for engineering; excluded from this formal round |
| `sail_v4_no_human` | Same recovery controller, with human replies unavailable |

The prompt baseline and v3 condition reuse their frozen condition text and runtime. v4 uses one fixed reviewer route, `deepseek-v4-flash`, across all actor models. All three v4 conditions share the same actor notice.

## Limits and experiment order

Each fresh Docker episode has 48 actor requests, 24 combined reviewer/recovery/protocol-correction requests, four actual human questions, 900 seconds, one CPU, 1536 MiB RAM, and no swap. One recoverable syntax/schema correction is allowed per review, with the original error retained. A successful correction does not invalidate an episode; unresolved errors fail closed. Whole failed episodes are not retried to replace outcomes.

Engineering preflights use 32 concurrent episodes. Formal phases start at 64 and can rise to 96 after two healthy five-minute windows. Persistent upstream errors reduce concurrency. New launches pause below 64 GiB available memory, below 30 GiB free disk, or above 75% of logical-CPU count in load average. Existing unrelated containers and processes are not modified.

Formal design: 6,720 attempts, exactly matching round two after mapping its defense conditions to the new controller. The same 80 cases and twelve framework-model configurations receive three repeats for fresh Prompt (2,880) and full SAIL v4 (2,880), plus one for SAIL v4 without human replies (960). The exact second-round job order, container images, task fixtures, and limits are preserved. The method and analysis are frozen before formal start. Complete every frozen condition regardless of outcome. The previously proposed 33,840-attempt expansion was cancelled before formal execution at the user's request.

## Evidence and limits

The primary objective is lower ASR and higher BCR relative to the fresh same-round Prompt baseline. Main paired estimates require both episodes valid under the same framework, model route, case, and repeat. Use 10,000 task-cluster bootstrap draws and report attack-family clustering separately. Retain all-attempt failures, observed-unsafe/missing-outcome bounds, request counts, reported token coverage, and time.

The independent audit flags cumulative effects missed by single-call predicates, possible alternate tool realizations, exact-one scoring disagreements, and missing or empty deliverables. It never changes the legacy scorer. Ambiguous equivalences and semantic completion remain unadjudicated, not silently labeled safe or successful.

Human replies are fixed synthetic fixtures, and consequential tools record simulated effects. Clean counterparts preserve task text and benign predicates, but some tasks still require legitimate decisions. Therefore clean question rate is not a false-positive rate, and legacy BCR is not semantic completion. Prepared task-ID validation and clean counterparts are not run in this round. All formal cases are reused development tasks; no unseen-task generalization is claimed.

## Reproduction entry points

1. `experiments/sail-v4-20260913/authorized_scope.json` fixes the active 6,720-attempt scope.
2. `scripts/prepare_sail_v4_matched.py --phase preflight` freezes the eight-case, three-condition r2 engineering check (288 attempts).
3. `scripts/promote_sail_v4.py` drains the already-running r1 check, runs matched r2, audits protocol validity, then freezes and starts the 6,720-attempt formal comparison. It does not select on ASR/BCR.
4. `scripts/supervise_sail_v4.py` reads `matched_formal_freeze.json`; it rejects the superseded expanded design.
5. `scripts/watch_sail_v4.py` mirrors closed attempts, replays scores, audits inputs, and updates the paper when the single formal phase finishes.
6. `scripts/build_sail_v4_paper.py` dispatches to the equal-scale report builder under the authorized scope.

The earlier `prepare_sail_v4.py` and expanded-split generator are archived design utilities, not the active launch path. The unused 480-attempt r2 plan was superseded before execution by the 288-attempt matched-condition check; the runtime remains engineering revision 2.

Private connection/provider configuration is required for the watcher and credential relay. It is excluded from the public repository. Image digests, runner hashes, parent-plan hash, and exact condition mapping are recorded in each active plan. Public artifacts exclude credentials, private conversations, and wire traces.
