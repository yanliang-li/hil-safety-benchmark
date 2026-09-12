# Four-framework API experiment

Status: **provisional_incomplete**. 4733/5760 attempts closed; 4567 valid, 166 failed, 1027 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 53/207 (25.6%) | 175/207 (84.5%) | 95/155 (61.3%) | 61/96 (63.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 40/207 (19.3%) | 175/207 (84.5%) | 94/155 (60.6%) | 64/95 (67.4%) |
| claude-code | glm-5.2 | neutral | 38/215 (17.7%) | 197/215 (91.6%) | 92/159 (57.9%) | 70/93 (75.3%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 26/215 (12.1%) | 198/215 (92.1%) | 89/159 (56.0%) | 70/89 (78.7%) |
| claude-code | qwen3.7-max | neutral | 61/205 (29.8%) | 194/205 (94.6%) | 61/153 (39.9%) | 42/61 (68.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 26/205 (12.7%) | 195/205 (95.1%) | 72/153 (47.1%) | 60/73 (82.2%) |
| codex | deepseek-v4-flash | neutral | 48/199 (24.1%) | 178/199 (89.4%) | 61/148 (41.2%) | 42/61 (68.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 29/201 (14.4%) | 182/201 (90.5%) | 58/149 (38.9%) | 41/58 (70.7%) |
| codex | glm-5.2 | neutral | 39/189 (20.6%) | 173/189 (91.5%) | 51/138 (37.0%) | 42/51 (82.4%) |
| codex | glm-5.2 | prompt_guard_v1 | 22/189 (11.6%) | 175/189 (92.6%) | 63/136 (46.3%) | 58/63 (92.1%) |
| codex | qwen3.7-max | neutral | 67/209 (32.1%) | 198/209 (94.7%) | 40/154 (26.0%) | 29/40 (72.5%) |
| codex | qwen3.7-max | prompt_guard_v1 | 25/203 (12.3%) | 191/203 (94.1%) | 62/151 (41.1%) | 50/62 (80.6%) |
| deepseek-harness | deepseek-v4-flash | neutral | 60/206 (29.1%) | 181/206 (87.9%) | 86/158 (54.4%) | 60/87 (69.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 34/208 (16.3%) | 185/208 (88.9%) | 94/159 (59.1%) | 70/95 (73.7%) |
| deepseek-harness | glm-5.2 | neutral | 38/183 (20.8%) | 170/183 (92.9%) | 65/132 (49.2%) | 51/65 (78.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 21/175 (12.0%) | 166/175 (94.9%) | 73/128 (57.0%) | 61/73 (83.6%) |
| deepseek-harness | qwen3.7-max | neutral | 69/215 (32.1%) | 206/215 (95.8%) | 46/161 (28.6%) | 32/46 (69.6%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/215 (12.1%) | 205/215 (95.3%) | 62/160 (38.8%) | 53/62 (85.5%) |
| hermes | deepseek-v4-flash | neutral | 49/155 (31.6%) | 135/155 (87.1%) | 59/115 (51.3%) | 39/59 (66.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 25/150 (16.7%) | 135/150 (90.0%) | 56/113 (49.6%) | 43/57 (75.4%) |
| hermes | glm-5.2 | neutral | 33/149 (22.1%) | 138/149 (92.6%) | 54/114 (47.4%) | 44/54 (81.5%) |
| hermes | glm-5.2 | prompt_guard_v1 | 18/154 (11.7%) | 147/154 (95.5%) | 67/117 (57.3%) | 56/67 (83.6%) |
| hermes | qwen3.7-max | neutral | 42/157 (26.8%) | 144/157 (91.7%) | 27/119 (22.7%) | 20/27 (74.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/156 (12.2%) | 147/156 (94.2%) | 45/117 (38.5%) | 36/45 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
