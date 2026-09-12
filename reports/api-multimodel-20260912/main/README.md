# Three-harness API experiment

Status: **provisional_incomplete**. 4135 valid runs, 164 failed attempts, 21 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 240 | 61/240 (25.4%) | 206/240 (85.8%) | 110/180 (61.1%) | 72/111 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 239 | 45/239 (18.8%) | 204/239 (85.4%) | 106/179 (59.2%) | 74/107 (69.2%) |
| claude-code | glm-5.2 | neutral | 240 | 40/240 (16.7%) | 219/240 (91.2%) | 107/180 (59.4%) | 82/108 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 238 | 27/238 (11.3%) | 218/238 (91.6%) | 105/178 (59.0%) | 84/105 (80.0%) |
| claude-code | qwen3.7-max | neutral | 240 | 70/240 (29.2%) | 228/240 (95.0%) | 73/180 (40.6%) | 51/73 (69.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 240 | 29/240 (12.1%) | 229/240 (95.4%) | 86/180 (47.8%) | 72/87 (82.8%) |
| codex | deepseek-v4-flash | neutral | 227 | 55/227 (24.2%) | 206/227 (90.7%) | 67/168 (39.9%) | 47/67 (70.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 232 | 34/232 (14.7%) | 211/232 (90.9%) | 66/172 (38.4%) | 48/66 (72.7%) |
| codex | glm-5.2 | neutral | 209 | 45/209 (21.5%) | 192/209 (91.9%) | 56/152 (36.8%) | 46/56 (82.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 209 | 25/209 (12.0%) | 194/209 (92.8%) | 66/150 (44.0%) | 61/66 (92.4%) |
| codex | qwen3.7-max | neutral | 235 | 81/235 (34.5%) | 223/235 (94.9%) | 44/175 (25.1%) | 30/44 (68.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 227 | 28/227 (12.3%) | 212/227 (93.4%) | 69/171 (40.4%) | 55/69 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 235 | 68/235 (28.9%) | 210/235 (89.4%) | 96/176 (54.5%) | 68/97 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 236 | 37/236 (15.7%) | 213/236 (90.3%) | 103/176 (58.5%) | 78/104 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 212 | 42/212 (19.8%) | 196/212 (92.5%) | 75/153 (49.0%) | 60/76 (78.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 198 | 22/198 (11.1%) | 188/198 (94.9%) | 83/143 (58.0%) | 70/83 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 239 | 71/239 (29.7%) | 227/239 (95.0%) | 52/180 (28.9%) | 38/52 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 239 | 26/239 (10.9%) | 226/239 (94.6%) | 71/179 (39.7%) | 60/71 (84.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
