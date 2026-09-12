# InterveneBench / HIL Safety Benchmark

An executable research benchmark for human-in-the-loop safety in tool-using agents. It studies when an agent asks for human input, whether its question identifies the relevant action and scope, and how it acts after the reply.

The current V4 dataset contains **250 synthetic tasks × 4 fixed human replies = 1,000 cases**, across 24 application domains and 20 attack families. Replies are clear approval, clear denial, ambiguity, and scope mismatch. Some actions can receive valid authorization; hard-prohibited actions remain prohibited. Consequential tool effects are simulated and logged by the benchmark MCP server.

## Quick start

Requires Python 3.10 or newer. Python 3.12 was used for the recovered environment.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/pytest -q
.venv/bin/hilbench run-scripted data/cases/product_draft_delivery__clear_deny__s43 \
  --run-dir runs/scripted-example --behavior safe
```

The scripted agent checks instrumentation and scoring using hidden labels. It is **not a model baseline**. The checked-in cases are the frozen V4 dataset; regenerate into a separate directory when changing the generator.

## Experiments and current evidence

The completed exploratory pilot uses Codex CLI 0.144.1 with the requested model ID `gpt-5.6-luna`, medium reasoning, on the same 80 cases in two conditions. `prompt_guard_v1` adds an authorization-scope policy to the task prompt; it does not install an execution gate.

| Measure | Neutral | Prompt guard |
|---|---:|---:|
| Unsafe attack success ↓ | 18/80 | 8/80 |
| Benign task completion ↑ | 76/80 | 76/80 |
| Timely matched consultation on confirmable cases ↑ | 24/60 | 27/60 |
| Correct, safe completion after a matched reply ↑ | 22/26 | 21/27 |

Consulted groups differ between conditions. The results do not establish uniform improvement or a causal effect of human feedback. The motivating redundant-validation attack remains unresolved. Independent risk-recognition labels and semantic question-quality annotations are still missing. See [metric definitions](docs/metrics_zh.md), [pilot aggregates](reports/pilot_six_metrics.json), and the [working paper](paper/iclr2027/main.pdf).

A new **4,320-attempt** matrix is now running: actual Codex, Claude Code, and DeepSeek Harness CLIs × three requested model IDs (`deepseek-v4-flash`, `glm-5.2`, `qwen3.7-max`) × 80 cases × neutral/defense × three repeats. Each run uses Docker isolation. The [runner guide](scripts/api_experiment/README.md) and [frozen plan](experiments/api-multimodel-20260912/main-plan-v1.json) record versions, native protocols, order, sampling differences, and resource limits.

All nine configurations completed a real-task preflight. Of 36 text-model IDs, 33 passed a harmless tool round trip. These are compatibility results, not main safety results. The provider's underlying weights and serving provenance are unverified. Periodic reports and manuscript appendix tables are marked provisional until the matrix finishes.

Follow the [current result tables](reports/api-multimodel-20260912/main/README.md), [per-case scores](reports/api-multimodel-20260912/main/per_case.csv), and [all-attempt audit](reports/api-multimodel-20260912/main/attempt_audit.json). The supplementary audit includes failure categories, token usage for failed and valid attempts, and safety sensitivity bounds that retain unsafe actions observed before a failed termination. It was added after initial failures and does not replace the frozen primary analysis. Raw evidence is replayed locally before publication; updates are pushed after at least 100 additional closed attempts and at completion.

## Project layout

- `src/hil_safety_bench/`: generation, runtime, MCP tools, agent adapters, and scoring.
- `data/`: frozen V4 cases and dataset manifests. Hidden labels under `.benchmark/` are for the evaluator.
- `tests/`: instrumentation and scoring regression checks.
- `experiments/`: frozen pilot selection and defense plan.
- `scripts/`: local experiment and analysis utilities; some historical analyses require raw runs that are not part of this release.
- `docs/`: benchmark and metric definitions.
- `paper/iclr2027/`: compilable LaTeX draft, figures, tables, and PDF. This is a working draft, not an accepted paper.
- `case_000631/hil/evaluate.py`: historical motivating-case evaluator retained for its regression tests; the original private task bundle is not included.

For a base Docker image, run `docker build -t hil-safety-bench:latest .`. The API runner uses separate bounded containers and a credential relay; see its setup guide. Never mount personal authentication directories into an untrusted agent workspace.

This public snapshot excludes personal conversations, credentials, host recovery files, downloaded third-party papers, and raw CLI authentication/session artifacts. No open-source license is assigned to original project material in this draft release; third-party components retain their own licenses.
