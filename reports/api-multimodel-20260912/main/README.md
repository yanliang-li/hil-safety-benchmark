# Three-harness API experiment

Status: **provisional_incomplete**. 3499 valid runs, 125 failed attempts, 696 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 196 | 50/196 (25.5%) | 165/196 (84.2%) | 89/149 (59.7%) | 58/90 (64.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 197 | 38/197 (19.3%) | 166/197 (84.3%) | 90/150 (60.0%) | 62/91 (68.1%) |
| claude-code | glm-5.2 | neutral | 212 | 37/212 (17.5%) | 194/212 (91.5%) | 91/158 (57.6%) | 69/92 (75.0%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 212 | 25/212 (11.8%) | 195/212 (92.0%) | 88/158 (55.7%) | 69/88 (78.4%) |
| claude-code | qwen3.7-max | neutral | 195 | 57/195 (29.2%) | 184/195 (94.4%) | 59/147 (40.1%) | 40/59 (67.8%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 195 | 24/195 (12.3%) | 185/195 (94.9%) | 71/147 (48.3%) | 59/72 (81.9%) |
| codex | deepseek-v4-flash | neutral | 193 | 46/193 (23.8%) | 172/193 (89.1%) | 59/144 (41.0%) | 42/59 (71.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 193 | 28/193 (14.5%) | 174/193 (90.2%) | 54/143 (37.8%) | 38/54 (70.4%) |
| codex | glm-5.2 | neutral | 183 | 39/183 (21.3%) | 168/183 (91.8%) | 49/133 (36.8%) | 40/49 (81.6%) |
| codex | glm-5.2 | prompt_guard_v1 | 183 | 22/183 (12.0%) | 169/183 (92.3%) | 60/132 (45.5%) | 55/60 (91.7%) |
| codex | qwen3.7-max | neutral | 199 | 64/199 (32.2%) | 189/199 (95.0%) | 39/149 (26.2%) | 29/39 (74.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 194 | 25/194 (12.9%) | 183/194 (94.3%) | 60/146 (41.1%) | 48/60 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 198 | 58/198 (29.3%) | 175/198 (88.4%) | 81/151 (53.6%) | 56/82 (68.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 198 | 31/198 (15.7%) | 177/198 (89.4%) | 88/150 (58.7%) | 66/89 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 177 | 36/177 (20.3%) | 164/177 (92.7%) | 63/128 (49.2%) | 50/63 (79.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 166 | 20/166 (12.0%) | 158/166 (95.2%) | 69/121 (57.0%) | 58/69 (84.1%) |
| deepseek-harness | qwen3.7-max | neutral | 205 | 66/205 (32.2%) | 196/205 (95.6%) | 43/153 (28.1%) | 30/43 (69.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 203 | 25/203 (12.3%) | 194/203 (95.6%) | 58/151 (38.4%) | 51/58 (87.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
