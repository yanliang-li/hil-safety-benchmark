# Three-harness API experiment

Status: **provisional_incomplete**. 3337 valid runs, 117 failed attempts, 866 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 189 | 49/189 (25.9%) | 159/189 (84.1%) | 84/142 (59.2%) | 54/85 (63.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 189 | 37/189 (19.6%) | 160/189 (84.7%) | 85/142 (59.9%) | 58/86 (67.4%) |
| claude-code | glm-5.2 | neutral | 204 | 35/204 (17.2%) | 188/204 (92.2%) | 87/151 (57.6%) | 67/88 (76.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 205 | 24/205 (11.7%) | 189/205 (92.2%) | 86/152 (56.6%) | 68/86 (79.1%) |
| claude-code | qwen3.7-max | neutral | 189 | 55/189 (29.1%) | 178/189 (94.2%) | 58/144 (40.3%) | 39/58 (67.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 189 | 22/189 (11.6%) | 179/189 (94.7%) | 70/144 (48.6%) | 58/71 (81.7%) |
| codex | deepseek-v4-flash | neutral | 178 | 44/178 (24.7%) | 160/178 (89.9%) | 57/135 (42.2%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 177 | 27/177 (15.3%) | 159/177 (89.8%) | 53/133 (39.8%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 172 | 38/172 (22.1%) | 158/172 (91.9%) | 44/123 (35.8%) | 35/44 (79.5%) |
| codex | glm-5.2 | prompt_guard_v1 | 174 | 21/174 (12.1%) | 162/174 (93.1%) | 56/124 (45.2%) | 51/56 (91.1%) |
| codex | qwen3.7-max | neutral | 187 | 61/187 (32.6%) | 177/187 (94.7%) | 38/141 (27.0%) | 28/38 (73.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 186 | 24/186 (12.9%) | 175/186 (94.1%) | 58/142 (40.8%) | 46/58 (79.3%) |
| deepseek-harness | deepseek-v4-flash | neutral | 187 | 55/187 (29.4%) | 167/187 (89.3%) | 76/143 (53.1%) | 54/77 (70.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 187 | 29/187 (15.5%) | 168/187 (89.8%) | 85/142 (59.9%) | 64/86 (74.4%) |
| deepseek-harness | glm-5.2 | neutral | 169 | 34/169 (20.1%) | 158/169 (93.5%) | 61/123 (49.6%) | 48/61 (78.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 160 | 18/160 (11.2%) | 152/160 (95.0%) | 68/118 (57.6%) | 57/68 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 198 | 63/198 (31.8%) | 190/198 (96.0%) | 41/148 (27.7%) | 29/41 (70.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 197 | 23/197 (11.7%) | 188/197 (95.4%) | 55/147 (37.4%) | 48/55 (87.3%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
