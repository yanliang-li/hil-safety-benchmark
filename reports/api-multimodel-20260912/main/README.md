# Three-harness API experiment

Status: **provisional_incomplete**. 3726 valid runs, 144 failed attempts, 450 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 213 | 53/213 (24.9%) | 181/213 (85.0%) | 97/159 (61.0%) | 63/98 (64.3%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 212 | 40/212 (18.9%) | 180/212 (84.9%) | 96/158 (60.8%) | 66/97 (68.0%) |
| claude-code | glm-5.2 | neutral | 217 | 38/217 (17.5%) | 199/217 (91.7%) | 92/159 (57.9%) | 70/93 (75.3%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 218 | 26/218 (11.9%) | 201/218 (92.2%) | 90/160 (56.2%) | 71/90 (78.9%) |
| claude-code | qwen3.7-max | neutral | 215 | 64/215 (29.8%) | 203/215 (94.4%) | 64/160 (40.0%) | 44/64 (68.8%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 216 | 27/216 (12.5%) | 205/216 (94.9%) | 77/161 (47.8%) | 64/78 (82.1%) |
| codex | deepseek-v4-flash | neutral | 205 | 50/205 (24.4%) | 184/205 (89.8%) | 62/152 (40.8%) | 43/62 (69.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 206 | 30/206 (14.6%) | 186/206 (90.3%) | 60/154 (39.0%) | 43/60 (71.7%) |
| codex | glm-5.2 | neutral | 193 | 41/193 (21.2%) | 177/193 (91.7%) | 52/140 (37.1%) | 43/52 (82.7%) |
| codex | glm-5.2 | prompt_guard_v1 | 191 | 22/191 (11.5%) | 177/191 (92.7%) | 64/138 (46.4%) | 59/64 (92.2%) |
| codex | qwen3.7-max | neutral | 211 | 68/211 (32.2%) | 200/211 (94.8%) | 41/156 (26.3%) | 29/41 (70.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 204 | 25/204 (12.3%) | 191/204 (93.6%) | 63/152 (41.4%) | 50/63 (79.4%) |
| deepseek-harness | deepseek-v4-flash | neutral | 210 | 61/210 (29.0%) | 185/210 (88.1%) | 87/160 (54.4%) | 61/88 (69.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 211 | 34/211 (16.1%) | 188/211 (89.1%) | 95/160 (59.4%) | 71/96 (74.0%) |
| deepseek-harness | glm-5.2 | neutral | 189 | 39/189 (20.6%) | 175/189 (92.6%) | 68/138 (49.3%) | 52/68 (76.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 177 | 21/177 (11.9%) | 168/177 (94.9%) | 74/130 (56.9%) | 62/74 (83.8%) |
| deepseek-harness | qwen3.7-max | neutral | 219 | 69/219 (31.5%) | 209/219 (95.4%) | 47/164 (28.7%) | 33/47 (70.2%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 219 | 26/219 (11.9%) | 208/219 (95.0%) | 63/163 (38.7%) | 54/63 (85.7%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
