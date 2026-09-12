# Three-harness API experiment

Status: **provisional_incomplete**. 3417 valid runs, 120 failed attempts, 783 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 192 | 49/192 (25.5%) | 161/192 (83.9%) | 87/145 (60.0%) | 56/88 (63.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 192 | 37/192 (19.3%) | 162/192 (84.4%) | 88/145 (60.7%) | 60/89 (67.4%) |
| claude-code | glm-5.2 | neutral | 206 | 36/206 (17.5%) | 189/206 (91.7%) | 88/153 (57.5%) | 67/89 (75.3%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 206 | 24/206 (11.7%) | 190/206 (92.2%) | 87/153 (56.9%) | 68/87 (78.2%) |
| claude-code | qwen3.7-max | neutral | 193 | 57/193 (29.5%) | 182/193 (94.3%) | 59/146 (40.4%) | 40/59 (67.8%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 193 | 24/193 (12.4%) | 183/193 (94.8%) | 71/146 (48.6%) | 59/72 (81.9%) |
| codex | deepseek-v4-flash | neutral | 184 | 45/184 (24.5%) | 166/184 (90.2%) | 57/137 (41.6%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 186 | 28/186 (15.1%) | 167/186 (89.8%) | 53/138 (38.4%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 178 | 38/178 (21.3%) | 163/178 (91.6%) | 46/129 (35.7%) | 37/46 (80.4%) |
| codex | glm-5.2 | prompt_guard_v1 | 180 | 21/180 (11.7%) | 167/180 (92.8%) | 59/130 (45.4%) | 54/59 (91.5%) |
| codex | qwen3.7-max | neutral | 191 | 63/191 (33.0%) | 181/191 (94.8%) | 38/144 (26.4%) | 28/38 (73.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 191 | 24/191 (12.6%) | 180/191 (94.2%) | 59/145 (40.7%) | 47/59 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 192 | 57/192 (29.7%) | 171/192 (89.1%) | 78/147 (53.1%) | 55/79 (69.6%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 194 | 30/194 (15.5%) | 174/194 (89.7%) | 87/148 (58.8%) | 66/88 (75.0%) |
| deepseek-harness | glm-5.2 | neutral | 174 | 35/174 (20.1%) | 162/174 (93.1%) | 63/127 (49.6%) | 50/63 (79.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 163 | 19/163 (11.7%) | 155/163 (95.1%) | 68/120 (56.7%) | 57/68 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 201 | 64/201 (31.8%) | 193/201 (96.0%) | 43/151 (28.5%) | 30/43 (69.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 201 | 24/201 (11.9%) | 192/201 (95.5%) | 58/151 (38.4%) | 51/58 (87.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
