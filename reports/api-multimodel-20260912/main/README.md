# Three-harness API experiment

Status: **provisional_incomplete**. 1310 valid runs, 53 failed attempts, 2957 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 75 | 18/75 (24.0%) | 64/75 (85.3%) | 35/56 (62.5%) | 24/35 (68.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 76 | 14/76 (18.4%) | 64/76 (84.2%) | 38/56 (67.9%) | 24/38 (63.2%) |
| claude-code | glm-5.2 | neutral | 78 | 13/78 (16.7%) | 71/78 (91.0%) | 34/59 (57.6%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 79 | 8/79 (10.1%) | 71/79 (89.9%) | 35/59 (59.3%) | 28/35 (80.0%) |
| claude-code | qwen3.7-max | neutral | 78 | 23/78 (29.5%) | 74/78 (94.9%) | 22/59 (37.3%) | 16/22 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 79 | 9/79 (11.4%) | 76/79 (96.2%) | 28/60 (46.7%) | 24/28 (85.7%) |
| codex | deepseek-v4-flash | neutral | 71 | 19/71 (26.8%) | 62/71 (87.3%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 71 | 11/71 (15.5%) | 62/71 (87.3%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | neutral | 65 | 17/65 (26.2%) | 58/65 (89.2%) | 18/48 (37.5%) | 13/18 (72.2%) |
| codex | glm-5.2 | prompt_guard_v1 | 67 | 9/67 (13.4%) | 63/67 (94.0%) | 22/49 (44.9%) | 20/22 (90.9%) |
| codex | qwen3.7-max | neutral | 75 | 25/75 (33.3%) | 71/75 (94.7%) | 15/56 (26.8%) | 11/15 (73.3%) |
| codex | qwen3.7-max | prompt_guard_v1 | 74 | 12/74 (16.2%) | 69/74 (93.2%) | 20/56 (35.7%) | 16/20 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 74 | 20/74 (27.0%) | 65/74 (87.8%) | 30/54 (55.6%) | 21/30 (70.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 72 | 12/72 (16.7%) | 66/72 (91.7%) | 31/52 (59.6%) | 23/31 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 63 | 11/63 (17.5%) | 60/63 (95.2%) | 22/45 (48.9%) | 19/22 (86.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 63 | 7/63 (11.1%) | 59/63 (93.7%) | 23/43 (53.5%) | 20/23 (87.0%) |
| deepseek-harness | qwen3.7-max | neutral | 74 | 23/74 (31.1%) | 70/74 (94.6%) | 14/56 (25.0%) | 10/14 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 76 | 8/76 (10.5%) | 71/76 (93.4%) | 23/58 (39.7%) | 21/23 (91.3%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
