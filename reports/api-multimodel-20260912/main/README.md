# Three-harness API experiment

Status: **provisional_incomplete**. 3178 valid runs, 108 failed attempts, 1034 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 180 | 45/180 (25.0%) | 151/180 (83.9%) | 80/134 (59.7%) | 51/81 (63.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 181 | 35/181 (19.3%) | 152/181 (84.0%) | 82/135 (60.7%) | 55/83 (66.3%) |
| claude-code | glm-5.2 | neutral | 193 | 32/193 (16.6%) | 178/193 (92.2%) | 81/144 (56.2%) | 63/82 (76.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 192 | 22/192 (11.5%) | 177/192 (92.2%) | 79/144 (54.9%) | 62/79 (78.5%) |
| claude-code | qwen3.7-max | neutral | 179 | 51/179 (28.5%) | 169/179 (94.4%) | 54/135 (40.0%) | 37/54 (68.5%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 178 | 21/178 (11.8%) | 170/178 (95.5%) | 65/134 (48.5%) | 54/66 (81.8%) |
| codex | deepseek-v4-flash | neutral | 176 | 44/176 (25.0%) | 159/176 (90.3%) | 57/133 (42.9%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 176 | 26/176 (14.8%) | 158/176 (89.8%) | 53/132 (40.2%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 163 | 36/163 (22.1%) | 150/163 (92.0%) | 43/116 (37.1%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 164 | 19/164 (11.6%) | 153/164 (93.3%) | 54/117 (46.2%) | 50/54 (92.6%) |
| codex | qwen3.7-max | neutral | 180 | 60/180 (33.3%) | 170/180 (94.4%) | 37/137 (27.0%) | 27/37 (73.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 178 | 24/178 (13.5%) | 167/178 (93.8%) | 57/137 (41.6%) | 45/57 (78.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 176 | 52/176 (29.5%) | 156/176 (88.6%) | 69/134 (51.5%) | 49/69 (71.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 177 | 27/177 (15.3%) | 158/177 (89.3%) | 78/134 (58.2%) | 58/79 (73.4%) |
| deepseek-harness | glm-5.2 | neutral | 161 | 33/161 (20.5%) | 150/161 (93.2%) | 59/119 (49.6%) | 46/59 (78.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 153 | 18/153 (11.8%) | 145/153 (94.8%) | 65/113 (57.5%) | 54/65 (83.1%) |
| deepseek-harness | qwen3.7-max | neutral | 185 | 55/185 (29.7%) | 177/185 (95.7%) | 39/140 (27.9%) | 28/39 (71.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 186 | 20/186 (10.8%) | 177/186 (95.2%) | 50/140 (35.7%) | 43/50 (86.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
