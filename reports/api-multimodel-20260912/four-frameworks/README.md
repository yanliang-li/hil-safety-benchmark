# Four-framework API experiment

Status: **provisional_incomplete**. 4196/5760 attempts closed; 4072 valid, 124 failed, 1564 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 47/184 (25.5%) | 154/184 (83.7%) | 82/138 (59.4%) | 52/83 (62.7%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 36/185 (19.5%) | 156/185 (84.3%) | 84/139 (60.4%) | 57/85 (67.1%) |
| claude-code | glm-5.2 | neutral | 33/198 (16.7%) | 183/198 (92.4%) | 84/147 (57.1%) | 65/85 (76.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 22/198 (11.1%) | 182/198 (91.9%) | 82/147 (55.8%) | 64/82 (78.0%) |
| claude-code | qwen3.7-max | neutral | 52/184 (28.3%) | 173/184 (94.0%) | 56/139 (40.3%) | 39/56 (69.6%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 21/183 (11.5%) | 174/183 (95.1%) | 68/138 (49.3%) | 56/69 (81.2%) |
| codex | deepseek-v4-flash | neutral | 44/176 (25.0%) | 159/176 (90.3%) | 57/133 (42.9%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 27/177 (15.3%) | 159/177 (89.8%) | 53/133 (39.8%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 37/168 (22.0%) | 154/168 (91.7%) | 43/120 (35.8%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 20/170 (11.8%) | 158/170 (92.9%) | 55/121 (45.5%) | 50/55 (90.9%) |
| codex | qwen3.7-max | neutral | 60/184 (32.6%) | 174/184 (94.6%) | 38/139 (27.3%) | 28/38 (73.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 24/183 (13.1%) | 172/183 (94.0%) | 58/139 (41.7%) | 46/58 (79.3%) |
| deepseek-harness | deepseek-v4-flash | neutral | 54/181 (29.8%) | 161/181 (89.0%) | 72/138 (52.2%) | 51/73 (69.9%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 28/183 (15.3%) | 164/183 (89.6%) | 82/139 (59.0%) | 62/83 (74.7%) |
| deepseek-harness | glm-5.2 | neutral | 34/166 (20.5%) | 155/166 (93.4%) | 60/120 (50.0%) | 47/60 (78.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 18/157 (11.5%) | 149/157 (94.9%) | 67/115 (58.3%) | 56/67 (83.6%) |
| deepseek-harness | qwen3.7-max | neutral | 60/193 (31.1%) | 185/193 (95.9%) | 39/145 (26.9%) | 28/39 (71.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 22/191 (11.5%) | 182/191 (95.3%) | 51/143 (35.7%) | 44/51 (86.3%) |
| hermes | deepseek-v4-flash | neutral | 43/136 (31.6%) | 118/136 (86.8%) | 53/104 (51.0%) | 36/53 (67.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 21/134 (15.7%) | 119/134 (88.8%) | 51/104 (49.0%) | 40/52 (76.9%) |
| hermes | glm-5.2 | neutral | 31/132 (23.5%) | 121/132 (91.7%) | 50/103 (48.5%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 15/132 (11.4%) | 125/132 (94.7%) | 59/102 (57.8%) | 50/59 (84.7%) |
| hermes | qwen3.7-max | neutral | 36/138 (26.1%) | 126/138 (91.3%) | 23/104 (22.1%) | 17/23 (73.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 18/139 (12.9%) | 131/139 (94.2%) | 39/104 (37.5%) | 31/39 (79.5%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
