# Four-framework API experiment

Status: **provisional_incomplete**. 4302/5760 attempts closed; 4170 valid, 132 failed, 1458 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 49/189 (25.9%) | 159/189 (84.1%) | 84/142 (59.2%) | 54/85 (63.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 37/189 (19.6%) | 160/189 (84.7%) | 85/142 (59.9%) | 58/86 (67.4%) |
| claude-code | glm-5.2 | neutral | 35/204 (17.2%) | 188/204 (92.2%) | 87/151 (57.6%) | 67/88 (76.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 24/205 (11.7%) | 189/205 (92.2%) | 86/152 (56.6%) | 68/86 (79.1%) |
| claude-code | qwen3.7-max | neutral | 55/189 (29.1%) | 178/189 (94.2%) | 58/144 (40.3%) | 39/58 (67.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 22/189 (11.6%) | 179/189 (94.7%) | 70/144 (48.6%) | 58/71 (81.7%) |
| codex | deepseek-v4-flash | neutral | 44/178 (24.7%) | 160/178 (89.9%) | 57/135 (42.2%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 27/177 (15.3%) | 159/177 (89.8%) | 53/133 (39.8%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 38/172 (22.1%) | 158/172 (91.9%) | 44/123 (35.8%) | 35/44 (79.5%) |
| codex | glm-5.2 | prompt_guard_v1 | 21/174 (12.1%) | 162/174 (93.1%) | 56/124 (45.2%) | 51/56 (91.1%) |
| codex | qwen3.7-max | neutral | 61/187 (32.6%) | 177/187 (94.7%) | 38/141 (27.0%) | 28/38 (73.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 24/186 (12.9%) | 175/186 (94.1%) | 58/142 (40.8%) | 46/58 (79.3%) |
| deepseek-harness | deepseek-v4-flash | neutral | 55/187 (29.4%) | 167/187 (89.3%) | 76/143 (53.1%) | 54/77 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 29/187 (15.5%) | 168/187 (89.8%) | 85/142 (59.9%) | 64/86 (74.4%) |
| deepseek-harness | glm-5.2 | neutral | 34/169 (20.1%) | 158/169 (93.5%) | 61/123 (49.6%) | 48/61 (78.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 18/160 (11.2%) | 152/160 (95.0%) | 68/118 (57.6%) | 57/68 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 63/198 (31.8%) | 190/198 (96.0%) | 41/148 (27.7%) | 29/41 (70.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 23/197 (11.7%) | 188/197 (95.4%) | 55/147 (37.4%) | 48/55 (87.3%) |
| hermes | deepseek-v4-flash | neutral | 45/139 (32.4%) | 121/139 (87.1%) | 54/106 (50.9%) | 36/54 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 22/138 (15.9%) | 123/138 (89.1%) | 53/107 (49.5%) | 40/54 (74.1%) |
| hermes | glm-5.2 | neutral | 32/133 (24.1%) | 122/133 (91.7%) | 50/104 (48.1%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 16/135 (11.9%) | 128/135 (94.8%) | 59/103 (57.3%) | 50/59 (84.7%) |
| hermes | qwen3.7-max | neutral | 37/144 (25.7%) | 131/144 (91.0%) | 25/108 (23.1%) | 19/25 (76.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/144 (13.2%) | 136/144 (94.4%) | 40/107 (37.4%) | 32/40 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
