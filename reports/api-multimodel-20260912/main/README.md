# Three-harness API experiment

Status: **provisional_incomplete**. 577 valid runs, 14 failed attempts, 3729 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 36 | 6/36 (16.7%) | 29/36 (80.6%) | 20/32 (62.5%) | 14/20 (70.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 36 | 4/36 (11.1%) | 29/36 (80.6%) | 24/32 (75.0%) | 16/24 (66.7%) |
| claude-code | glm-5.2 | neutral | 27 | 6/27 (22.2%) | 21/27 (77.8%) | 11/22 (50.0%) | 6/11 (54.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27 | 3/27 (11.1%) | 23/27 (85.2%) | 12/22 (54.5%) | 9/12 (75.0%) |
| claude-code | qwen3.7-max | neutral | 36 | 9/36 (25.0%) | 34/36 (94.4%) | 11/28 (39.3%) | 8/11 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 35 | 3/35 (8.6%) | 34/35 (97.1%) | 11/27 (40.7%) | 10/11 (90.9%) |
| codex | deepseek-v4-flash | neutral | 34 | 10/34 (29.4%) | 30/34 (88.2%) | 9/24 (37.5%) | 8/9 (88.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 34 | 7/34 (20.6%) | 30/34 (88.2%) | 9/24 (37.5%) | 8/9 (88.9%) |
| codex | glm-5.2 | neutral | 27 | 6/27 (22.2%) | 24/27 (88.9%) | 7/20 (35.0%) | 4/7 (57.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 25 | 4/25 (16.0%) | 24/25 (96.0%) | 7/19 (36.8%) | 5/7 (71.4%) |
| codex | qwen3.7-max | neutral | 33 | 13/33 (39.4%) | 31/33 (93.9%) | 8/27 (29.6%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 33 | 8/33 (24.2%) | 30/33 (90.9%) | 10/27 (37.0%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 32 | 7/32 (21.9%) | 29/32 (90.6%) | 12/22 (54.5%) | 10/12 (83.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 31 | 5/31 (16.1%) | 27/31 (87.1%) | 12/21 (57.1%) | 7/12 (58.3%) |
| deepseek-harness | glm-5.2 | neutral | 28 | 6/28 (21.4%) | 28/28 (100.0%) | 13/23 (56.5%) | 12/13 (92.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 29 | 4/29 (13.8%) | 28/29 (96.6%) | 13/23 (56.5%) | 13/13 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 37 | 11/37 (29.7%) | 33/37 (89.2%) | 5/29 (17.2%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 37 | 3/37 (8.1%) | 33/37 (89.2%) | 11/29 (37.9%) | 9/11 (81.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
