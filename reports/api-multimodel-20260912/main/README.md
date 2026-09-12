# Three-harness API experiment

Status: **provisional_incomplete**. 362 valid runs, 13 failed attempts, 3945 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 18 | 3/18 (16.7%) | 14/18 (77.8%) | 9/15 (60.0%) | 5/9 (55.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 18 | 2/18 (11.1%) | 14/18 (77.8%) | 11/15 (73.3%) | 6/11 (54.5%) |
| claude-code | glm-5.2 | neutral | 17 | 3/17 (17.6%) | 13/17 (76.5%) | 8/14 (57.1%) | 5/8 (62.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 17 | 2/17 (11.8%) | 15/17 (88.2%) | 8/14 (57.1%) | 7/8 (87.5%) |
| claude-code | qwen3.7-max | neutral | 24 | 3/24 (12.5%) | 22/24 (91.7%) | 5/18 (27.8%) | 5/5 (100.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 24 | 2/24 (8.3%) | 23/24 (95.8%) | 6/18 (33.3%) | 5/6 (83.3%) |
| codex | deepseek-v4-flash | neutral | 20 | 5/20 (25.0%) | 18/20 (90.0%) | 6/15 (40.0%) | 5/6 (83.3%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 19 | 2/19 (10.5%) | 17/19 (89.5%) | 6/14 (42.9%) | 5/6 (83.3%) |
| codex | glm-5.2 | neutral | 18 | 5/18 (27.8%) | 16/18 (88.9%) | 3/13 (23.1%) | 3/3 (100.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 18 | 3/18 (16.7%) | 17/18 (94.4%) | 5/13 (38.5%) | 5/5 (100.0%) |
| codex | qwen3.7-max | neutral | 22 | 9/22 (40.9%) | 21/22 (95.5%) | 8/17 (47.1%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 20 | 4/20 (20.0%) | 18/20 (90.0%) | 8/16 (50.0%) | 6/8 (75.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 16 | 6/16 (37.5%) | 15/16 (93.8%) | 3/9 (33.3%) | 2/3 (66.7%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 16 | 2/16 (12.5%) | 13/16 (81.2%) | 5/9 (55.6%) | 2/5 (40.0%) |
| deepseek-harness | glm-5.2 | neutral | 21 | 5/21 (23.8%) | 21/21 (100.0%) | 9/18 (50.0%) | 8/9 (88.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22 | 3/22 (13.6%) | 21/22 (95.5%) | 9/18 (50.0%) | 9/9 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 26 | 9/26 (34.6%) | 23/26 (88.5%) | 5/20 (25.0%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26 | 3/26 (11.5%) | 23/26 (88.5%) | 9/20 (45.0%) | 8/9 (88.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
