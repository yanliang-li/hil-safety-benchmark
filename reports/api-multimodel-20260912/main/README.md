# Three-harness API experiment

Status: **provisional_incomplete**. 3102 valid runs, 106 failed attempts, 1112 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 175 | 43/175 (24.6%) | 147/175 (84.0%) | 79/131 (60.3%) | 51/80 (63.8%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 174 | 32/174 (18.4%) | 147/174 (84.5%) | 79/130 (60.8%) | 55/80 (68.8%) |
| claude-code | glm-5.2 | neutral | 186 | 31/186 (16.7%) | 171/186 (91.9%) | 79/140 (56.4%) | 62/80 (77.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 183 | 21/183 (11.5%) | 168/183 (91.8%) | 79/138 (57.2%) | 62/79 (78.5%) |
| claude-code | qwen3.7-max | neutral | 176 | 51/176 (29.0%) | 167/176 (94.9%) | 53/133 (39.8%) | 36/53 (67.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 176 | 21/176 (11.9%) | 168/176 (95.5%) | 64/133 (48.1%) | 53/65 (81.5%) |
| codex | deepseek-v4-flash | neutral | 173 | 43/173 (24.9%) | 156/173 (90.2%) | 55/130 (42.3%) | 38/55 (69.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 175 | 26/175 (14.9%) | 157/175 (89.7%) | 52/131 (39.7%) | 36/52 (69.2%) |
| codex | glm-5.2 | neutral | 160 | 36/160 (22.5%) | 148/160 (92.5%) | 43/113 (38.1%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 158 | 19/158 (12.0%) | 148/158 (93.7%) | 51/111 (45.9%) | 48/51 (94.1%) |
| codex | qwen3.7-max | neutral | 178 | 59/178 (33.1%) | 168/178 (94.4%) | 37/135 (27.4%) | 27/37 (73.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 177 | 24/177 (13.6%) | 166/177 (93.8%) | 57/136 (41.9%) | 45/57 (78.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 172 | 50/172 (29.1%) | 152/172 (88.4%) | 68/131 (51.9%) | 49/68 (72.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 172 | 27/172 (15.7%) | 153/172 (89.0%) | 76/130 (58.5%) | 56/77 (72.7%) |
| deepseek-harness | glm-5.2 | neutral | 160 | 32/160 (20.0%) | 149/160 (93.1%) | 59/118 (50.0%) | 46/59 (78.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 150 | 16/150 (10.7%) | 142/150 (94.7%) | 64/111 (57.7%) | 53/64 (82.8%) |
| deepseek-harness | qwen3.7-max | neutral | 179 | 53/179 (29.6%) | 171/179 (95.5%) | 36/134 (26.9%) | 26/36 (72.2%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 178 | 19/178 (10.7%) | 169/178 (94.9%) | 47/133 (35.3%) | 41/47 (87.2%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
