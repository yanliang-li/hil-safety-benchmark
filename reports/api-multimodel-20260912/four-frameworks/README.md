# Four-framework API experiment

Status: **provisional_incomplete**. 4842/5760 attempts closed; 4673 valid, 169 failed, 918 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 53/213 (24.9%) | 181/213 (85.0%) | 97/159 (61.0%) | 63/98 (64.3%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 40/212 (18.9%) | 180/212 (84.9%) | 96/158 (60.8%) | 66/97 (68.0%) |
| claude-code | glm-5.2 | neutral | 38/217 (17.5%) | 199/217 (91.7%) | 92/159 (57.9%) | 70/93 (75.3%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 26/218 (11.9%) | 201/218 (92.2%) | 90/160 (56.2%) | 71/90 (78.9%) |
| claude-code | qwen3.7-max | neutral | 64/215 (29.8%) | 203/215 (94.4%) | 64/160 (40.0%) | 44/64 (68.8%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 27/216 (12.5%) | 205/216 (94.9%) | 77/161 (47.8%) | 64/78 (82.1%) |
| codex | deepseek-v4-flash | neutral | 50/205 (24.4%) | 184/205 (89.8%) | 62/152 (40.8%) | 43/62 (69.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 30/206 (14.6%) | 186/206 (90.3%) | 60/154 (39.0%) | 43/60 (71.7%) |
| codex | glm-5.2 | neutral | 41/193 (21.2%) | 177/193 (91.7%) | 52/140 (37.1%) | 43/52 (82.7%) |
| codex | glm-5.2 | prompt_guard_v1 | 22/191 (11.5%) | 177/191 (92.7%) | 64/138 (46.4%) | 59/64 (92.2%) |
| codex | qwen3.7-max | neutral | 68/211 (32.2%) | 200/211 (94.8%) | 41/156 (26.3%) | 29/41 (70.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 25/204 (12.3%) | 191/204 (93.6%) | 63/152 (41.4%) | 50/63 (79.4%) |
| deepseek-harness | deepseek-v4-flash | neutral | 61/210 (29.0%) | 185/210 (88.1%) | 87/160 (54.4%) | 61/88 (69.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 34/211 (16.1%) | 188/211 (89.1%) | 95/160 (59.4%) | 71/96 (74.0%) |
| deepseek-harness | glm-5.2 | neutral | 39/189 (20.6%) | 175/189 (92.6%) | 68/138 (49.3%) | 52/68 (76.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 21/177 (11.9%) | 168/177 (94.9%) | 74/130 (56.9%) | 62/74 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 69/219 (31.5%) | 209/219 (95.4%) | 47/164 (28.7%) | 33/47 (70.2%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/219 (11.9%) | 208/219 (95.0%) | 63/163 (38.7%) | 54/63 (85.7%) |
| hermes | deepseek-v4-flash | neutral | 49/160 (30.6%) | 138/160 (86.2%) | 61/119 (51.3%) | 40/61 (65.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 25/157 (15.9%) | 142/157 (90.4%) | 58/118 (49.2%) | 45/59 (76.3%) |
| hermes | glm-5.2 | neutral | 33/153 (21.6%) | 141/153 (92.2%) | 56/117 (47.9%) | 46/56 (82.1%) |
| hermes | glm-5.2 | prompt_guard_v1 | 19/160 (11.9%) | 152/160 (95.0%) | 69/120 (57.5%) | 57/69 (82.6%) |
| hermes | qwen3.7-max | neutral | 42/159 (26.4%) | 146/159 (91.8%) | 27/120 (22.5%) | 20/27 (74.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/158 (12.0%) | 149/158 (94.3%) | 45/119 (37.8%) | 36/45 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
