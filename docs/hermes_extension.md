# Fourth framework: Hermes Agent

The owner requested the actual Claude Code, Codex, Hermes, and DeepSeek Harness frameworks. Hermes is the official [NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent), version **0.21.2**, commit `b7b35a84b7fbe1aa2e223a6ce726a2471300d0a4`. Its native `hermes --oneshot` command runs the agent loop. The adapter does not implement a replacement model loop.

## Matched extension

The original [4,320-attempt plan](../experiments/api-multimodel-20260912/main-plan-v1.json) is unchanged. The [Hermes plan](../experiments/api-multimodel-20260912/hermes-plan-v1.json) adds 1,440 attempts:

| Factor | Values |
|---|---|
| Requested model routes | `deepseek-v4-flash`, `glm-5.2`, `qwen3.7-max` |
| Cases | Same 80 cases from 20 base tasks |
| Conditions | `neutral`, `prompt_guard_v1` |
| Repeats | Three per case and condition |
| Combined matrix | Four frameworks, 12 framework–model configurations, 5,760 attempts |

The cases were used in earlier pilot and defense development. This is an exploratory repeated evaluation, not a held-out or full-dataset estimate. Hermes starts later than the original frameworks. Calendar time, gateway load, native framework prompts, and serving drift can affect comparisons. Requested API IDs do not establish the identity of the underlying model weights.

## Native behavior and preflights

Hermes uses the provider's Chat Completions route through the same credential relay. It receives a placeholder credential; the real key stays in the relay. Its `hil_bench` MCP server exposes the same ten benchmark tools. Native terminal, browser, memory, and other task toolsets are disabled. Hermes presents its native `tool_search`, `tool_describe`, and `tool_call` bridge to discover and invoke these ten tools. This interface is retained as part of the framework being evaluated.

The first Hermes attempt failed during initialization: its 32,768-token configuration was below the framework's 64,000-token minimum. No model request occurred. The six subsequent model–condition preflights used a 65,536-token context setting; all completed, and independent local event replay reproduced all six scores. Their largest reported prompt was 8,267 tokens. Codex and DeepSeek Harness use 32,768; Claude Code retains its native context handling. Configuration values do not verify endpoint context limits.

Hermes also makes a native session-title request. The six successful preflights each contained one such request. These calls use the requested model and count toward the relay's 48-request allowance and all-attempt usage totals. Agent-loop requests specify `max_tokens=4096`; the observed title requests do not specify an output-token cap. No prompt rewriting or protocol translation is performed by the relay.

The [preflight ledger](../reports/hermes-framework-preflight.json) retains all seven attempts, including the initialization failure. The [independent replay audit](../reports/hermes-preflight-replay.json) records event hashes, requested tool names, usage checks, and successful replay. Preflights are excluded from the main matrix.

## Build and run

Build the original harness image following its [guide](../scripts/api_experiment/README.md). Make a separate Hermes build context containing `Dockerfile.hermes` renamed to `Dockerfile`, and the pinned upstream checkout in `hermes-source/`. Build it as `hil-api-hermes:20260912-v1`. Do not include personal files or authentication directories in the context.

The Dockerfile installs the upstream checkout in a separate virtual environment. The pinned release requires an editable source installation; a standard wheel installation is rejected by upstream. The benchmark MCP process still uses the original image's Python environment and frozen benchmark source. The resolved [Hermes dependency list](../experiments/api-multimodel-20260912/hermes-dependencies.txt), upstream commit, image ID, runner hashes, and case hashes are retained. A rebuild may resolve different transitive packages; use the recorded image ID when reproducing this execution.

`scripts/hermes_experiment/freeze.py` creates a new immutable manifest only after successful model–condition preflights and independent replay. `scripts/hermes_experiment/launch.py` checks its source, case, and image hashes, then runs the frozen adapter from an isolated snapshot.

Keep the original scheduler target at **24** while Hermes has **8** workers. Wait for the original active count to fall to 24 before starting Hermes. The total agent limit is **32**, not 32 per framework. The relay's 40-request capacity is a separate limit. Each agent keeps a 1 CPU and 1,536 MiB limit, no extra swap, a read-only root and case mount, fresh temporary state, and a 900-second timeout. New launches require at least 64 GiB available host memory and 30 GiB free storage. The shared `STOP_NEW_RUNS` flag pauses new launches without terminating active attempts. When one cohort finishes, the remaining cohort may use all 32 slots.

## Results and publication

`scripts/analyze_four_frameworks.py` calls the original frozen scorer for each manifest, verifies stored scores against ordered events, and combines reports without pooling framework–model configurations. Failed attempts remain in a separate all-attempt audit, including any unsafe actions observed before failure.

The [combined report](../reports/api-multimodel-20260912/four-frameworks/README.md) links the 5,760-attempt matrix to provisional observed counts. Original and Hermes reports remain separate under `reports/api-multimodel-20260912/main/` and `hermes/`. Reported defense differences stay provisional until all attempts close. Recognition labels and semantic question precision remain unavailable; the existing question score is a rule proxy.

`scripts/watch_four_frameworks_remote.py` refreshes server reports every three minutes. `scripts/watch_four_frameworks_local.py` replaces the old local watcher: it downloads only closed attempts, independently replays both cohorts, updates the manuscript, audits the public checkout, and publishes roughly every 100 additional closed attempts and at completion. Private connection settings, raw sessions, conversations, and credentials are not published. Do not run both old and new report watchers simultaneously.
