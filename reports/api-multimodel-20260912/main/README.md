# Three-harness API experiment

Status: **provisional_incomplete**. 1251 valid runs, 47 failed attempts, 3022 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 71 | 18/71 (25.4%) | 60/71 (84.5%) | 34/55 (61.8%) | 23/34 (67.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 70 | 14/70 (20.0%) | 58/70 (82.9%) | 37/55 (67.3%) | 23/37 (62.2%) |
| claude-code | glm-5.2 | neutral | 75 | 12/75 (16.0%) | 68/75 (90.7%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 75 | 7/75 (9.3%) | 67/75 (89.3%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | qwen3.7-max | neutral | 77 | 23/77 (29.9%) | 73/77 (94.8%) | 22/58 (37.9%) | 16/22 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 76 | 9/76 (11.8%) | 73/76 (96.1%) | 28/58 (48.3%) | 24/28 (85.7%) |
| codex | deepseek-v4-flash | neutral | 67 | 18/67 (26.9%) | 58/67 (86.6%) | 18/50 (36.0%) | 14/18 (77.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 70 | 11/70 (15.7%) | 61/70 (87.1%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | neutral | 59 | 15/59 (25.4%) | 54/59 (91.5%) | 16/44 (36.4%) | 12/16 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 60 | 8/60 (13.3%) | 58/60 (96.7%) | 20/44 (45.5%) | 18/20 (90.0%) |
| codex | qwen3.7-max | neutral | 71 | 24/71 (33.8%) | 67/71 (94.4%) | 14/53 (26.4%) | 10/14 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 72 | 11/72 (15.3%) | 67/72 (93.1%) | 20/54 (37.0%) | 16/20 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 73 | 20/73 (27.4%) | 64/73 (87.7%) | 29/53 (54.7%) | 20/29 (69.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 72 | 12/72 (16.7%) | 66/72 (91.7%) | 31/52 (59.6%) | 23/31 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 63 | 11/63 (17.5%) | 60/63 (95.2%) | 22/45 (48.9%) | 19/22 (86.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 58 | 7/58 (12.1%) | 55/58 (94.8%) | 22/41 (53.7%) | 19/22 (86.4%) |
| deepseek-harness | qwen3.7-max | neutral | 71 | 22/71 (31.0%) | 67/71 (94.4%) | 11/53 (20.8%) | 8/11 (72.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 71 | 8/71 (11.3%) | 66/71 (93.0%) | 20/53 (37.7%) | 18/20 (90.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
