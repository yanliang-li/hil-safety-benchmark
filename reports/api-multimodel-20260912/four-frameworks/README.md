# Four-framework API experiment

Status: **provisional_incomplete**. 5290/5760 attempts closed; 5101 valid, 189 failed, 470 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 61/236 (25.8%) | 203/236 (86.0%) | 108/177 (61.0%) | 70/109 (64.2%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 44/235 (18.7%) | 201/235 (85.5%) | 105/177 (59.3%) | 73/106 (68.9%) |
| claude-code | glm-5.2 | neutral | 40/238 (16.8%) | 217/238 (91.2%) | 106/178 (59.6%) | 81/107 (75.7%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27/237 (11.4%) | 217/237 (91.6%) | 104/177 (58.8%) | 83/104 (79.8%) |
| claude-code | qwen3.7-max | neutral | 68/235 (28.9%) | 223/235 (94.9%) | 72/176 (40.9%) | 50/72 (69.4%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 29/237 (12.2%) | 226/237 (95.4%) | 84/177 (47.5%) | 70/85 (82.4%) |
| codex | deepseek-v4-flash | neutral | 53/220 (24.1%) | 199/220 (90.5%) | 65/164 (39.6%) | 45/65 (69.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 34/226 (15.0%) | 205/226 (90.7%) | 64/167 (38.3%) | 46/64 (71.9%) |
| codex | glm-5.2 | neutral | 45/206 (21.8%) | 189/206 (91.7%) | 56/150 (37.3%) | 46/56 (82.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 25/205 (12.2%) | 191/205 (93.2%) | 65/146 (44.5%) | 60/65 (92.3%) |
| codex | qwen3.7-max | neutral | 79/228 (34.6%) | 217/228 (95.2%) | 43/170 (25.3%) | 30/43 (69.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 28/221 (12.7%) | 207/221 (93.7%) | 68/166 (41.0%) | 55/68 (80.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 67/231 (29.0%) | 206/231 (89.2%) | 94/172 (54.7%) | 66/95 (69.5%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37/231 (16.0%) | 208/231 (90.0%) | 100/171 (58.5%) | 75/101 (74.3%) |
| deepseek-harness | glm-5.2 | neutral | 42/208 (20.2%) | 192/208 (92.3%) | 72/150 (48.0%) | 57/73 (78.1%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/194 (11.3%) | 184/194 (94.8%) | 80/140 (57.1%) | 67/80 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 71/234 (30.3%) | 223/234 (95.3%) | 51/175 (29.1%) | 37/51 (72.5%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/234 (11.1%) | 222/234 (94.9%) | 69/174 (39.7%) | 59/69 (85.5%) |
| hermes | deepseek-v4-flash | neutral | 55/177 (31.1%) | 154/177 (87.0%) | 68/133 (51.1%) | 45/68 (66.2%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 29/172 (16.9%) | 156/172 (90.7%) | 68/130 (52.3%) | 52/69 (75.4%) |
| hermes | glm-5.2 | neutral | 37/170 (21.8%) | 158/170 (92.9%) | 61/126 (48.4%) | 51/61 (83.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 20/172 (11.6%) | 164/172 (95.3%) | 73/126 (57.9%) | 61/73 (83.6%) |
| hermes | qwen3.7-max | neutral | 46/177 (26.0%) | 163/177 (92.1%) | 32/135 (23.7%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/177 (10.7%) | 167/177 (94.4%) | 51/134 (38.1%) | 42/51 (82.4%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
