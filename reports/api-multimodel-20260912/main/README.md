# Three-harness API experiment

Status: **provisional_incomplete**. 432 valid runs, 13 failed attempts, 3875 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 21 | 3/21 (14.3%) | 16/21 (76.2%) | 11/17 (64.7%) | 6/11 (54.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 21 | 2/21 (9.5%) | 16/21 (76.2%) | 13/17 (76.5%) | 7/13 (53.8%) |
| claude-code | glm-5.2 | neutral | 20 | 4/20 (20.0%) | 16/20 (80.0%) | 9/16 (56.2%) | 5/9 (55.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 20 | 2/20 (10.0%) | 18/20 (90.0%) | 9/16 (56.2%) | 8/9 (88.9%) |
| claude-code | qwen3.7-max | neutral | 30 | 5/30 (16.7%) | 28/30 (93.3%) | 8/23 (34.8%) | 7/8 (87.5%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 29 | 2/29 (6.9%) | 28/29 (96.6%) | 8/22 (36.4%) | 7/8 (87.5%) |
| codex | deepseek-v4-flash | neutral | 25 | 7/25 (28.0%) | 22/25 (88.0%) | 7/19 (36.8%) | 6/7 (85.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 25 | 4/25 (16.0%) | 22/25 (88.0%) | 8/19 (42.1%) | 7/8 (87.5%) |
| codex | glm-5.2 | neutral | 20 | 6/20 (30.0%) | 18/20 (90.0%) | 4/15 (26.7%) | 3/4 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 20 | 4/20 (20.0%) | 19/20 (95.0%) | 6/15 (40.0%) | 5/6 (83.3%) |
| codex | qwen3.7-max | neutral | 27 | 11/27 (40.7%) | 25/27 (92.6%) | 8/22 (36.4%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 28 | 7/28 (25.0%) | 25/28 (89.3%) | 10/23 (43.5%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 19 | 6/19 (31.6%) | 18/19 (94.7%) | 5/12 (41.7%) | 4/5 (80.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 19 | 2/19 (10.5%) | 16/19 (84.2%) | 6/12 (50.0%) | 3/6 (50.0%) |
| deepseek-harness | glm-5.2 | neutral | 23 | 5/23 (21.7%) | 23/23 (100.0%) | 11/20 (55.0%) | 10/11 (90.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 23 | 3/23 (13.0%) | 22/23 (95.7%) | 10/19 (52.6%) | 10/10 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 31 | 10/31 (32.3%) | 27/31 (87.1%) | 5/25 (20.0%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 31 | 3/31 (9.7%) | 27/31 (87.1%) | 10/25 (40.0%) | 8/10 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
