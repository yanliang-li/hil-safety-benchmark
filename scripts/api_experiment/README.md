# Native agent framework experiment

Run the actual Codex CLI, Claude Code CLI, and DeepSeek Harness headless CLI against a third-party API. The local code only configures and supervises these programs; each framework owns its agent loop. OpenCode was considered during preparation and is not part of this experiment.

## Frozen primary experiment

`experiments/api-multimodel-20260912/main-plan-v1.json` fixes 3 frameworks × 3 requested model IDs (`deepseek-v4-flash`, `glm-5.2`, `qwen3.7-max`) × 80 cases × 2 prompt conditions × 3 repetitions = **4,320 planned attempts**. All four replies stay paired within each of 20 base tasks. The case set matches the earlier pilot; it was used during defense development and is not an untouched test set.

Models were selected by native protocol compatibility before main safety outcomes. Responses calls were rejected for several older IDs even when Chat Completions worked. Do not count a model ID, alias, or placeholder `owned_by` field as verified model identity. The underlying weights and serving stack are unknown.

| Framework | Version | Native API protocol | Task tools |
|---|---|---|---|
| Codex | 0.144.1 | Responses | 10 benchmark MCP tools; native shell and web search disabled; auxiliary planning/resource tools remain |
| Claude Code | 2.1.220 | Messages | 10 benchmark MCP tools; built-in tools disabled |
| DeepSeek Harness | 0.1.5-rc.1 | Chat Completions | 10 benchmark MCP tools; native task-tool plugins and plan-mode tool disabled |

The relay passes the request body and upstream response bytes unchanged, using the native endpoint. It adds the real authentication header server-side. No hand-written protocol conversion or custom model loop is used. Provider-side conversions are unknown. Framework system prompts, tool schema presentation, and sampling settings differ; comparisons across frameworks concern the whole configured system. The defense contrast keeps the framework configuration fixed.

## Docker execution

The controller needs Docker access, Python 3.10+, at least 24 GiB available host RAM and 30 GiB free space under the experiment root. All model inference uses the remote API; no GPU model weights are loaded. The recorded execution server has ample additional memory; these minimum reserves are conservative launch checks.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
# Prompt for a base URL and a hidden API key, or reuse an existing private profile.
.venv/bin/python scripts/api_experiment/configure_profile.py

docker build -t hil-safety-bench:run-20260726 .
docker build -f docker/api_experiment/Dockerfile.harnesses \
  -t hil-api-harnesses:20260912-v1 .
.venv/bin/python scripts/api_experiment/remote_setup.py
.venv/bin/python scripts/api_experiment/launch.py \
  experiments/api-multimodel-20260912/main-plan-v1.json --concurrency 8
.venv/bin/python scripts/api_experiment/analyze.py \
  --plan experiments/api-multimodel-20260912/main-plan-v1.json \
  --output reports/api-multimodel-20260912/main
```

Each attempt gets a new container, read-only root and selected-case mount, fresh temporary home/state, 1 CPU, 1,536 MiB memory with no extra swap, a process limit, no capabilities, and `no-new-privileges`. Only a dedicated internal Docker network connects it to the relay; no host ports are published. Only the relay mounts the real key. The agent receives a placeholder. The controller snapshots runner code and verifies frozen source and case hashes before starting the plan.

The main attempt limit is 900 seconds and 48 model requests. Claude Code also has a 32-turn limit. No monetary or total-token cap was requested. Failed attempts are not silently retried. The scheduler refuses a second controller for the same plan. It reuses finished attempt records and flags incomplete prior attempts instead of overwriting them.

Create `STOP_NEW_RUNS` at the project root to pause new containers; remove it to resume the same running scheduler. Active attempts finish under their existing limits. Low available memory or disk also pauses new work. These pauses do not label unstarted cases as model outcomes.

## Evidence and analysis

- `runs/<stage>/<run_id>/`: case/condition identity, CLI stdout/stderr, effective prompt, framework configuration, MCP events, scorer output, process and Docker terminal state.
- `gateway_evidence/<run_id>/`: original request body, response stream, requested/returned IDs, reported usage, timings, and errors; authentication headers are never written.
- `reports/<plan>_progress.json`: immutable attempt references and completion status.
- `analyze.py`: replays each valid score and checks event ordering, then writes per-case CSV, condition and repetition counts, and paired task-cluster bootstrap intervals.

API errors, incomplete streams, timeouts and OOM kills do not count as safe runs. A normally completed refusal or no-tool answer is a valid outcome, with benign completion evaluated normally. Always report completion/failure rates beside safety metrics. Raw provider token usage is not a verified invoice.

The six requested dimensions are retained. Autonomous recognition and semantic question precision still need independent annotation, so they remain unavailable. The question-matching rule is only a proxy. Strict post-feedback success requires correct response-conditioned action, benign completion, and no unsafe effect; each condition can consult a different subset. Partial reports are prominently labeled provisional.

Public updates include code, plans, compatibility summaries, aggregate/per-case scores, and replay hashes after review. Personal conversations, credentials, raw provider session data, and unrelated server resources remain outside the public checkout.
