# InterveneBench v2.2 preflight development ledger

Date: 2026-09-14 (Asia/Shanghai)

This ledger separates development evidence from the frozen formal experiment.
No run listed here enters a formal effect estimate. Failed and superseded
attempts are retained rather than selectively removed.

## What the preflight was allowed to establish

The preflight tested container integration, model routing, hidden-label
isolation, reviewer protocol validity, state advancement after matched
questions, one-use reply handling, and coverage of every formal condition. It
was not sized or sampled to compare conditions. Safety or completion outcomes
from these runs must not be reported as formal benchmark results.

## Development sequence

1. The first container pass exposed a missing writable `/home/node` and was
   stopped before completion. The launcher now supplies an isolated tmpfs for
   that path.
2. A standard pass reached 17/18 valid runs; one risk-oracle run timed out. Its
   valid cases did not exercise a second native-agent turn, so this pass was not
   accepted as the integration gate.
3. Targeted multi-turn passes exposed four protocol problems: reviewer output
   truncated at the earlier token limit, occasional named-stage wrappers,
   malformed completion payloads, and reuse of a stale earlier reply after the
   latest reply had already been consumed. The isolated SAIL-HIL implementation
   was corrected and covered by unit tests. No old SAIL-v4 source was changed.
4. A higher-total-concurrency gate exposed provider-side 429 responses and
   timeouts. These attempts remain in the archived progress reports. The final
   gate therefore used at most four concurrent API-consuming jobs.
5. After the last source change, fresh standard and targeted plans were created
   with new run IDs. The standard plan completed 18/18 valid runs at launcher
   concurrency 3. The targeted plan completed 7/7 valid runs at concurrency 3;
   four runs advanced to a later native-agent turn.

The intermediate reports record additional fully valid development batches.
They are still superseded because their source hashes precede the last protocol
change or because they do not jointly satisfy the final gate definition.

## Accepted integration gate

| Component | Plan SHA-256 | Runs | Audit |
|---|---|---:|---|
| Standard | `2185c8ab6ebe0a64b2730715e4e9a85a79a290f529397b461af9fdd1c28581da` | 18/18 valid | pass; 0 violations; 0 warnings |
| Targeted | `7e239a377b452964daf66792ca08d1a419e611cf162d255d13a07d4dec9bd6f6` | 7/7 valid | pass; 0 violations; 0 warnings |

The joint acceptance record is
`preflight_acceptance.v22.json`. It covers all seven formal conditions and
records the four advanced-turn run IDs. The accepted source, bank manifest, and
case-bank hashes agree across both plans. No timeout replacement was admitted.

## Frozen formal launch

The accepted gate authorized generation of `formal_plan.v22.json` only. That
plan contains 1,980 unique run IDs: 1,800 main-condition attempts, 120
risk-oracle attempts, and 60 no-human attempts. It uses 900-second per-run
timeouts, task-level clustering, and a total launcher concurrency of four. The
plan SHA-256 is
`fafb96011e68af924f425c774709e20b6673702e09b8aa1b15f7427046649480`.
The launcher does not automatically retry a registered formal attempt.

## Evidence map

- Final plans, audits, and acceptance record are in this directory.
- Every archived terminal progress report is under
  `preflight_development_reports/`.
- Frozen bank construction and model-audit evidence are under
  `contextual_v22/` and `simulator_v22_judge_rubric3/`.
- Formal results, when complete, must be analyzed from the formal plan and its
  first-attempt run directories, never from any preflight trajectory.
