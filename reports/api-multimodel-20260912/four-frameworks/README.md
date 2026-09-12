# Four-framework API experiment

Status: **provisional_incomplete**. 5506/5760 attempts closed; 5315 valid, 191 failed, 254 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 61/240 (25.4%) | 206/240 (85.8%) | 110/180 (61.1%) | 72/111 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 45/240 (18.8%) | 205/240 (85.4%) | 107/180 (59.4%) | 75/108 (69.4%) |
| claude-code | glm-5.2 | neutral | 40/240 (16.7%) | 219/240 (91.2%) | 107/180 (59.4%) | 82/108 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27/240 (11.2%) | 220/240 (91.7%) | 106/180 (58.9%) | 85/106 (80.2%) |
| claude-code | qwen3.7-max | neutral | 70/240 (29.2%) | 228/240 (95.0%) | 73/180 (40.6%) | 51/73 (69.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 29/240 (12.1%) | 229/240 (95.4%) | 86/180 (47.8%) | 72/87 (82.8%) |
| codex | deepseek-v4-flash | neutral | 55/229 (24.0%) | 206/229 (90.0%) | 68/170 (40.0%) | 47/68 (69.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 34/232 (14.7%) | 211/232 (90.9%) | 66/172 (38.4%) | 48/66 (72.7%) |
| codex | glm-5.2 | neutral | 45/209 (21.5%) | 192/209 (91.9%) | 56/152 (36.8%) | 46/56 (82.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 25/210 (11.9%) | 195/210 (92.9%) | 67/151 (44.4%) | 62/67 (92.5%) |
| codex | qwen3.7-max | neutral | 82/237 (34.6%) | 224/237 (94.5%) | 44/177 (24.9%) | 30/44 (68.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 29/229 (12.7%) | 214/229 (93.4%) | 69/172 (40.1%) | 55/69 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 68/236 (28.8%) | 210/236 (89.0%) | 96/177 (54.2%) | 68/97 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37/237 (15.6%) | 213/237 (89.9%) | 103/177 (58.2%) | 78/104 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 42/212 (19.8%) | 196/212 (92.5%) | 75/153 (49.0%) | 60/76 (78.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/198 (11.1%) | 188/198 (94.9%) | 83/143 (58.0%) | 70/83 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 71/239 (29.7%) | 227/239 (95.0%) | 52/180 (28.9%) | 38/52 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/239 (10.9%) | 226/239 (94.6%) | 71/179 (39.7%) | 60/71 (84.5%) |
| hermes | deepseek-v4-flash | neutral | 61/191 (31.9%) | 167/191 (87.4%) | 70/143 (49.0%) | 46/70 (65.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 31/189 (16.4%) | 171/189 (90.5%) | 74/142 (52.1%) | 56/75 (74.7%) |
| hermes | glm-5.2 | neutral | 45/194 (23.2%) | 178/194 (91.8%) | 65/146 (44.5%) | 53/65 (81.5%) |
| hermes | glm-5.2 | prompt_guard_v1 | 23/197 (11.7%) | 186/197 (94.4%) | 88/148 (59.5%) | 73/88 (83.0%) |
| hermes | qwen3.7-max | neutral | 49/198 (24.7%) | 183/198 (92.4%) | 34/150 (22.7%) | 27/34 (79.4%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 21/199 (10.6%) | 189/199 (95.0%) | 52/148 (35.1%) | 43/52 (82.7%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
