# Three-harness API experiment

Status: **provisional_incomplete**. 3811 valid runs, 150 failed attempts, 359 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 216 | 54/216 (25.0%) | 184/216 (85.2%) | 98/161 (60.9%) | 63/99 (63.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 218 | 40/218 (18.3%) | 186/218 (85.3%) | 100/163 (61.3%) | 69/101 (68.3%) |
| claude-code | glm-5.2 | neutral | 224 | 40/224 (17.9%) | 205/224 (91.5%) | 97/166 (58.4%) | 73/98 (74.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 225 | 26/225 (11.6%) | 207/225 (92.0%) | 96/167 (57.5%) | 77/96 (80.2%) |
| claude-code | qwen3.7-max | neutral | 218 | 66/218 (30.3%) | 206/218 (94.5%) | 65/162 (40.1%) | 45/65 (69.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 217 | 28/217 (12.9%) | 206/217 (94.9%) | 77/161 (47.8%) | 64/78 (82.1%) |
| codex | deepseek-v4-flash | neutral | 210 | 51/210 (24.3%) | 189/210 (90.0%) | 63/157 (40.1%) | 43/63 (68.3%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 214 | 31/214 (14.5%) | 193/214 (90.2%) | 62/160 (38.8%) | 44/62 (71.0%) |
| codex | glm-5.2 | neutral | 198 | 42/198 (21.2%) | 181/198 (91.4%) | 54/145 (37.2%) | 45/54 (83.3%) |
| codex | glm-5.2 | prompt_guard_v1 | 197 | 24/197 (12.2%) | 183/197 (92.9%) | 65/142 (45.8%) | 60/65 (92.3%) |
| codex | qwen3.7-max | neutral | 215 | 70/215 (32.6%) | 204/215 (94.9%) | 41/160 (25.6%) | 29/41 (70.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 208 | 25/208 (12.0%) | 194/208 (93.3%) | 64/156 (41.0%) | 51/64 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 214 | 63/214 (29.4%) | 189/214 (88.3%) | 88/162 (54.3%) | 62/89 (69.7%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 214 | 35/214 (16.4%) | 191/214 (89.3%) | 96/162 (59.3%) | 72/97 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 196 | 40/196 (20.4%) | 182/196 (92.9%) | 70/141 (49.6%) | 55/71 (77.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 185 | 22/185 (11.9%) | 176/185 (95.1%) | 77/134 (57.5%) | 65/77 (84.4%) |
| deepseek-harness | qwen3.7-max | neutral | 221 | 69/221 (31.2%) | 211/221 (95.5%) | 49/166 (29.5%) | 35/49 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 221 | 26/221 (11.8%) | 210/221 (95.0%) | 65/165 (39.4%) | 56/65 (86.2%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
