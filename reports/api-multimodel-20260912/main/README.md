# Three-harness API experiment

Status: **provisional_incomplete**. 1027 valid runs, 36 failed attempts, 3257 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 54 | 10/54 (18.5%) | 44/54 (81.5%) | 31/46 (67.4%) | 21/31 (67.7%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 52 | 6/52 (11.5%) | 43/52 (82.7%) | 33/45 (73.3%) | 22/33 (66.7%) |
| claude-code | glm-5.2 | neutral | 60 | 9/60 (15.0%) | 53/60 (88.3%) | 27/47 (57.4%) | 20/27 (74.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 61 | 6/61 (9.8%) | 53/61 (86.9%) | 28/47 (59.6%) | 21/28 (75.0%) |
| claude-code | qwen3.7-max | neutral | 62 | 17/62 (27.4%) | 60/62 (96.8%) | 17/47 (36.2%) | 12/17 (70.6%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 62 | 6/62 (9.7%) | 61/62 (98.4%) | 21/48 (43.8%) | 20/21 (95.2%) |
| codex | deepseek-v4-flash | neutral | 56 | 16/56 (28.6%) | 50/56 (89.3%) | 14/41 (34.1%) | 11/14 (78.6%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 55 | 10/55 (18.2%) | 48/55 (87.3%) | 14/41 (34.1%) | 10/14 (71.4%) |
| codex | glm-5.2 | neutral | 50 | 13/50 (26.0%) | 45/50 (90.0%) | 12/39 (30.8%) | 8/12 (66.7%) |
| codex | glm-5.2 | prompt_guard_v1 | 49 | 6/49 (12.2%) | 47/49 (95.9%) | 14/38 (36.8%) | 12/14 (85.7%) |
| codex | qwen3.7-max | neutral | 60 | 21/60 (35.0%) | 57/60 (95.0%) | 13/46 (28.3%) | 10/13 (76.9%) |
| codex | qwen3.7-max | prompt_guard_v1 | 57 | 10/57 (17.5%) | 54/57 (94.7%) | 15/43 (34.9%) | 12/15 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 62 | 17/62 (27.4%) | 55/62 (88.7%) | 23/44 (52.3%) | 17/23 (73.9%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 62 | 11/62 (17.7%) | 57/62 (91.9%) | 25/44 (56.8%) | 18/25 (72.0%) |
| deepseek-harness | glm-5.2 | neutral | 50 | 8/50 (16.0%) | 48/50 (96.0%) | 19/38 (50.0%) | 16/19 (84.2%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 52 | 5/52 (9.6%) | 49/52 (94.2%) | 21/39 (53.8%) | 18/21 (85.7%) |
| deepseek-harness | qwen3.7-max | neutral | 62 | 21/62 (33.9%) | 58/62 (93.5%) | 10/47 (21.3%) | 7/10 (70.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 61 | 6/61 (9.8%) | 56/61 (91.8%) | 17/47 (36.2%) | 15/17 (88.2%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
