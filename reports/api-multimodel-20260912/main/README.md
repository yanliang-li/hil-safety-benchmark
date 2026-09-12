# Three-harness API experiment

Status: **provisional_incomplete**. 3028 valid runs, 101 failed attempts, 1191 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 172 | 43/172 (25.0%) | 146/172 (84.9%) | 77/129 (59.7%) | 51/78 (65.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 172 | 32/172 (18.6%) | 146/172 (84.9%) | 78/129 (60.5%) | 55/79 (69.6%) |
| claude-code | glm-5.2 | neutral | 177 | 30/177 (16.9%) | 162/177 (91.5%) | 76/134 (56.7%) | 60/77 (77.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 177 | 20/177 (11.3%) | 162/177 (91.5%) | 77/134 (57.5%) | 61/77 (79.2%) |
| claude-code | qwen3.7-max | neutral | 174 | 51/174 (29.3%) | 165/174 (94.8%) | 53/132 (40.2%) | 36/53 (67.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 174 | 21/174 (12.1%) | 166/174 (95.4%) | 64/132 (48.5%) | 53/65 (81.5%) |
| codex | deepseek-v4-flash | neutral | 167 | 41/167 (24.6%) | 150/167 (89.8%) | 53/124 (42.7%) | 36/53 (67.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 170 | 26/170 (15.3%) | 152/170 (89.4%) | 50/126 (39.7%) | 34/50 (68.0%) |
| codex | glm-5.2 | neutral | 157 | 36/157 (22.9%) | 145/157 (92.4%) | 43/112 (38.4%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 154 | 19/154 (12.3%) | 144/154 (93.5%) | 49/109 (45.0%) | 46/49 (93.9%) |
| codex | qwen3.7-max | neutral | 174 | 56/174 (32.2%) | 164/174 (94.3%) | 37/131 (28.2%) | 27/37 (73.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 172 | 23/172 (13.4%) | 161/172 (93.6%) | 55/131 (42.0%) | 43/55 (78.2%) |
| deepseek-harness | deepseek-v4-flash | neutral | 168 | 49/168 (29.2%) | 149/168 (88.7%) | 68/128 (53.1%) | 49/68 (72.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 169 | 27/169 (16.0%) | 151/169 (89.3%) | 74/128 (57.8%) | 55/75 (73.3%) |
| deepseek-harness | glm-5.2 | neutral | 154 | 29/154 (18.8%) | 143/154 (92.9%) | 56/112 (50.0%) | 44/56 (78.6%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 147 | 15/147 (10.2%) | 139/147 (94.6%) | 61/108 (56.5%) | 51/61 (83.6%) |
| deepseek-harness | qwen3.7-max | neutral | 174 | 53/174 (30.5%) | 166/174 (95.4%) | 35/131 (26.7%) | 25/35 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 176 | 19/176 (10.8%) | 167/176 (94.9%) | 46/132 (34.8%) | 40/46 (87.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
