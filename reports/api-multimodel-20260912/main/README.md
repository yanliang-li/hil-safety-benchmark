# Three-harness API experiment

Status: **provisional_incomplete**. 4150 valid runs, 167 failed attempts, 3 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 240 | 61/240 (25.4%) | 206/240 (85.8%) | 110/180 (61.1%) | 72/111 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 240 | 45/240 (18.8%) | 205/240 (85.4%) | 107/180 (59.4%) | 75/108 (69.4%) |
| claude-code | glm-5.2 | neutral | 240 | 40/240 (16.7%) | 219/240 (91.2%) | 107/180 (59.4%) | 82/108 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 240 | 27/240 (11.2%) | 220/240 (91.7%) | 106/180 (58.9%) | 85/106 (80.2%) |
| claude-code | qwen3.7-max | neutral | 240 | 70/240 (29.2%) | 228/240 (95.0%) | 73/180 (40.6%) | 51/73 (69.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 240 | 29/240 (12.1%) | 229/240 (95.4%) | 86/180 (47.8%) | 72/87 (82.8%) |
| codex | deepseek-v4-flash | neutral | 229 | 55/229 (24.0%) | 206/229 (90.0%) | 68/170 (40.0%) | 47/68 (69.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 233 | 34/233 (14.6%) | 211/233 (90.6%) | 67/173 (38.7%) | 48/67 (71.6%) |
| codex | glm-5.2 | neutral | 209 | 45/209 (21.5%) | 192/209 (91.9%) | 56/152 (36.8%) | 46/56 (82.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 211 | 25/211 (11.8%) | 196/211 (92.9%) | 68/152 (44.7%) | 63/68 (92.6%) |
| codex | qwen3.7-max | neutral | 237 | 82/237 (34.6%) | 224/237 (94.5%) | 44/177 (24.9%) | 30/44 (68.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 230 | 29/230 (12.6%) | 214/230 (93.0%) | 69/173 (39.9%) | 55/69 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 236 | 68/236 (28.8%) | 210/236 (89.0%) | 96/177 (54.2%) | 68/97 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 237 | 37/237 (15.6%) | 213/237 (89.9%) | 103/177 (58.2%) | 78/104 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 212 | 42/212 (19.8%) | 196/212 (92.5%) | 75/153 (49.0%) | 60/76 (78.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 198 | 22/198 (11.1%) | 188/198 (94.9%) | 83/143 (58.0%) | 70/83 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 239 | 71/239 (29.7%) | 227/239 (95.0%) | 52/180 (28.9%) | 38/52 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 239 | 26/239 (10.9%) | 226/239 (94.6%) | 71/179 (39.7%) | 60/71 (84.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
