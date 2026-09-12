# Model Experiment Protocol

## 1. Freeze the experimental configuration

Record the following before each experiment:

- benchmark source version and case-generation seed;
- exact Agent CLI version and exact model identifier;
- reasoning effort, temperature or other sampling controls when available;
- task prompt/policy condition;
- response-generation provider and model;
- repetition identifier (`r1`, `r2`, `r3`, ...).

Never mix different models or policy conditions in one run root.

## 2. Validate the harness without a paid model

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/pytest -q

.venv/bin/hilbench run-batch data/cases \
  --run-root runs/scripted-safe-check \
  --agent scripted-safe

.venv/bin/hilbench run-batch data/cases \
  --run-root runs/scripted-vulnerable-check \
  --agent scripted-vulnerable
```

The scripted agents only test instrumentation and scoring. They are not model
baselines and must not be included in the main model-comparison table.

## 3. Run a small pilot

Codex:

```bash
.venv/bin/hilbench run-batch data/cases \
  --run-root runs/codex-luna-pilot \
  --agent codex \
  --model gpt-5.6-luna \
  --reasoning-effort medium \
  --max-cases 2
```

Claude Code:

```bash
.venv/bin/hilbench run-batch data/cases \
  --run-root runs/claude-sonnet-pilot \
  --agent claude \
  --model sonnet \
  --max-budget-usd 0.5 \
  --max-cases 2
```

Inspect `events.jsonl`, the raw model stream, `result.json`, and
`run_metadata.json` for every pilot case. Check that:

1. the model read the intended attack-bearing artifact;
2. the risky action matcher corresponds to the intended attack;
3. the human reply was returned only after a matching `ask_human` call;
4. benign completion was detected correctly;
5. no API or tool failure was counted as a safe result.

## 4. Run the full matrix

Use a new run root for every model and repetition:

```bash
.venv/bin/hilbench run-batch data/cases \
  --run-root runs/codex-luna-r1 \
  --agent codex \
  --model gpt-5.6-luna \
  --reasoning-effort medium
```

Repeat with `r2` and `r3`. Use the same naming convention for every evaluated
model. A non-empty run directory is rejected to prevent accidental overwrite.

## 5. Aggregate and audit

```bash
.venv/bin/hilbench summarize runs/codex-luna-r1
```

This writes:

- `summary.json`: aggregate and per-response-category metrics;
- `cases.csv`: one row per case;
- per-case `events.jsonl`: normalized action/observation trajectory;
- per-case raw Agent stream and `run_metadata.json`.

The main metrics are:

- `unsafe_asr`;
- `any_human_question_rate`;
- `question_precision`;
- `ask_rate`;
- `safety_ask_f1`;
- `risk_disclosure_rate`;
- `timely_intervention_rate`;
- `evidence_grounded_intervention_rate`;
- `response_action_accuracy_on_asked`;
- `authorization_discrimination_gap_on_asked`;
- `clear_approve_execution_rate_on_asked`;
- `clear_deny_restraint_rate_on_asked`;
- `ambiguous_restraint_rate_on_asked`;
- `scope_mismatch_nontransfer_rate_on_asked`;
- `prohibited_restraint_rate_on_asked`;
- `post_hil_unsafe_rate`;
- `response_action_balanced_accuracy`;
- `paired_response_boundary_rate`;
- `paired_hil_success_rate`;
- `hil_effective_success_rate`;
- `safe_without_asking_rate`;
- `benign_completion_rate`;
- `joint_safe_utility_rate`.

Report HIL response-following accuracy only over cases where a valid matching
question was asked. If `response_scored_count` is zero, report the metric as
N/A rather than zero or one.

The main paper table should remain compact: Unsafe ASR, HIL Trigger Recall,
Response-Conditioned Action Accuracy, Paired Response-Boundary Rate, and Joint
Safe Utility. Treat the remaining values as diagnostic metrics. Because this
matrix contains only attacked cases, do not call HIL Trigger Recall “trigger
accuracy”; accuracy, specificity, or MCC requires matched clean controls.

## 6. Required human audit

Before using results in a paper, manually audit a stratified sample containing:

- every attack type;
- every response category;
- successes and failures for each model;
- safe cases with and without HIL;
- all unusual tool errors or incomplete trajectories.

Do not report the scripted smoke-test outputs as empirical model results.
