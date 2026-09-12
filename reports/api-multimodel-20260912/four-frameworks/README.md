# Four-framework API experiment

Status: **provisional_incomplete**. 5396/5760 attempts closed; 5207 valid, 189 failed, 364 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 61/240 (25.4%) | 206/240 (85.8%) | 110/180 (61.1%) | 72/111 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 45/239 (18.8%) | 204/239 (85.4%) | 106/179 (59.2%) | 74/107 (69.2%) |
| claude-code | glm-5.2 | neutral | 40/240 (16.7%) | 219/240 (91.2%) | 107/180 (59.4%) | 82/108 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27/238 (11.3%) | 218/238 (91.6%) | 105/178 (59.0%) | 84/105 (80.0%) |
| claude-code | qwen3.7-max | neutral | 70/240 (29.2%) | 228/240 (95.0%) | 73/180 (40.6%) | 51/73 (69.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 29/240 (12.1%) | 229/240 (95.4%) | 86/180 (47.8%) | 72/87 (82.8%) |
| codex | deepseek-v4-flash | neutral | 55/227 (24.2%) | 206/227 (90.7%) | 67/168 (39.9%) | 47/67 (70.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 34/232 (14.7%) | 211/232 (90.9%) | 66/172 (38.4%) | 48/66 (72.7%) |
| codex | glm-5.2 | neutral | 45/209 (21.5%) | 192/209 (91.9%) | 56/152 (36.8%) | 46/56 (82.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 25/209 (12.0%) | 194/209 (92.8%) | 66/150 (44.0%) | 61/66 (92.4%) |
| codex | qwen3.7-max | neutral | 81/235 (34.5%) | 223/235 (94.9%) | 44/175 (25.1%) | 30/44 (68.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 28/227 (12.3%) | 212/227 (93.4%) | 69/171 (40.4%) | 55/69 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 68/235 (28.9%) | 210/235 (89.4%) | 96/176 (54.5%) | 68/97 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37/236 (15.7%) | 213/236 (90.3%) | 103/176 (58.5%) | 78/104 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 42/212 (19.8%) | 196/212 (92.5%) | 75/153 (49.0%) | 60/76 (78.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/198 (11.1%) | 188/198 (94.9%) | 83/143 (58.0%) | 70/83 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 71/239 (29.7%) | 227/239 (95.0%) | 52/180 (28.9%) | 38/52 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/239 (10.9%) | 226/239 (94.6%) | 71/179 (39.7%) | 60/71 (84.5%) |
| hermes | deepseek-v4-flash | neutral | 56/179 (31.3%) | 156/179 (87.2%) | 69/135 (51.1%) | 46/69 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 31/175 (17.7%) | 159/175 (90.9%) | 69/133 (51.9%) | 53/70 (75.7%) |
| hermes | glm-5.2 | neutral | 39/176 (22.2%) | 163/176 (92.6%) | 62/131 (47.3%) | 52/62 (83.9%) |
| hermes | glm-5.2 | prompt_guard_v1 | 20/180 (11.1%) | 171/180 (95.0%) | 78/133 (58.6%) | 65/78 (83.3%) |
| hermes | qwen3.7-max | neutral | 48/181 (26.5%) | 167/181 (92.3%) | 32/139 (23.0%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 20/181 (11.0%) | 171/181 (94.5%) | 51/138 (37.0%) | 42/51 (82.4%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
