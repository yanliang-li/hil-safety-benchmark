# Three-harness API experiment

Status: **provisional_incomplete**. 3646 valid runs, 142 failed attempts, 532 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 207 | 53/207 (25.6%) | 175/207 (84.5%) | 95/155 (61.3%) | 61/96 (63.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 207 | 40/207 (19.3%) | 175/207 (84.5%) | 94/155 (60.6%) | 64/95 (67.4%) |
| claude-code | glm-5.2 | neutral | 215 | 38/215 (17.7%) | 197/215 (91.6%) | 92/159 (57.9%) | 70/93 (75.3%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 215 | 26/215 (12.1%) | 198/215 (92.1%) | 89/159 (56.0%) | 70/89 (78.7%) |
| claude-code | qwen3.7-max | neutral | 205 | 61/205 (29.8%) | 194/205 (94.6%) | 61/153 (39.9%) | 42/61 (68.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 205 | 26/205 (12.7%) | 195/205 (95.1%) | 72/153 (47.1%) | 60/73 (82.2%) |
| codex | deepseek-v4-flash | neutral | 199 | 48/199 (24.1%) | 178/199 (89.4%) | 61/148 (41.2%) | 42/61 (68.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 201 | 29/201 (14.4%) | 182/201 (90.5%) | 58/149 (38.9%) | 41/58 (70.7%) |
| codex | glm-5.2 | neutral | 189 | 39/189 (20.6%) | 173/189 (91.5%) | 51/138 (37.0%) | 42/51 (82.4%) |
| codex | glm-5.2 | prompt_guard_v1 | 189 | 22/189 (11.6%) | 175/189 (92.6%) | 63/136 (46.3%) | 58/63 (92.1%) |
| codex | qwen3.7-max | neutral | 209 | 67/209 (32.1%) | 198/209 (94.7%) | 40/154 (26.0%) | 29/40 (72.5%) |
| codex | qwen3.7-max | prompt_guard_v1 | 203 | 25/203 (12.3%) | 191/203 (94.1%) | 62/151 (41.1%) | 50/62 (80.6%) |
| deepseek-harness | deepseek-v4-flash | neutral | 206 | 60/206 (29.1%) | 181/206 (87.9%) | 86/158 (54.4%) | 60/87 (69.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 208 | 34/208 (16.3%) | 185/208 (88.9%) | 94/159 (59.1%) | 70/95 (73.7%) |
| deepseek-harness | glm-5.2 | neutral | 183 | 38/183 (20.8%) | 170/183 (92.9%) | 65/132 (49.2%) | 51/65 (78.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 175 | 21/175 (12.0%) | 166/175 (94.9%) | 73/128 (57.0%) | 61/73 (83.6%) |
| deepseek-harness | qwen3.7-max | neutral | 215 | 69/215 (32.1%) | 206/215 (95.8%) | 46/161 (28.6%) | 32/46 (69.6%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 215 | 26/215 (12.1%) | 205/215 (95.3%) | 62/160 (38.8%) | 53/62 (85.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
