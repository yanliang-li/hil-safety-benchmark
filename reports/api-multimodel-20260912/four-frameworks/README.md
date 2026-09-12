# Four-framework API experiment

Status: **complete**. 5760/5760 attempts closed; 5551 valid, 209 failed, 0 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 61/240 (25.4%) | 206/240 (85.8%) | 110/180 (61.1%) | 72/111 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 45/240 (18.8%) | 205/240 (85.4%) | 107/180 (59.4%) | 75/108 (69.4%) |
| claude-code | glm-5.2 | neutral | 40/240 (16.7%) | 219/240 (91.2%) | 107/180 (59.4%) | 82/108 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27/240 (11.2%) | 220/240 (91.7%) | 106/180 (58.9%) | 85/106 (80.2%) |
| claude-code | qwen3.7-max | neutral | 70/240 (29.2%) | 228/240 (95.0%) | 73/180 (40.6%) | 51/73 (69.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 29/240 (12.1%) | 229/240 (95.4%) | 86/180 (47.8%) | 72/87 (82.8%) |
| codex | deepseek-v4-flash | neutral | 55/229 (24.0%) | 206/229 (90.0%) | 68/170 (40.0%) | 47/68 (69.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 34/233 (14.6%) | 211/233 (90.6%) | 67/173 (38.7%) | 48/67 (71.6%) |
| codex | glm-5.2 | neutral | 45/210 (21.4%) | 193/210 (91.9%) | 57/153 (37.3%) | 47/57 (82.5%) |
| codex | glm-5.2 | prompt_guard_v1 | 25/211 (11.8%) | 196/211 (92.9%) | 68/152 (44.7%) | 63/68 (92.6%) |
| codex | qwen3.7-max | neutral | 82/237 (34.6%) | 224/237 (94.5%) | 44/177 (24.9%) | 30/44 (68.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 29/230 (12.6%) | 214/230 (93.0%) | 69/173 (39.9%) | 55/69 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 68/236 (28.8%) | 210/236 (89.0%) | 96/177 (54.2%) | 68/97 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37/237 (15.6%) | 213/237 (89.9%) | 103/177 (58.2%) | 78/104 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 42/212 (19.8%) | 196/212 (92.5%) | 75/153 (49.0%) | 60/76 (78.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/198 (11.1%) | 188/198 (94.9%) | 83/143 (58.0%) | 70/83 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 71/239 (29.7%) | 227/239 (95.0%) | 52/180 (28.9%) | 38/52 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/239 (10.9%) | 226/239 (94.6%) | 71/179 (39.7%) | 60/71 (84.5%) |
| hermes | deepseek-v4-flash | neutral | 73/233 (31.3%) | 203/233 (87.1%) | 83/175 (47.4%) | 54/83 (65.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 40/230 (17.4%) | 211/230 (91.7%) | 88/172 (51.2%) | 65/89 (73.0%) |
| hermes | glm-5.2 | neutral | 54/232 (23.3%) | 215/232 (92.7%) | 80/176 (45.5%) | 65/80 (81.2%) |
| hermes | glm-5.2 | prompt_guard_v1 | 28/234 (12.0%) | 223/234 (95.3%) | 105/176 (59.7%) | 88/105 (83.8%) |
| hermes | qwen3.7-max | neutral | 61/234 (26.1%) | 217/234 (92.7%) | 41/175 (23.4%) | 32/41 (78.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 29/237 (12.2%) | 224/237 (94.5%) | 65/178 (36.5%) | 52/65 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
