# Three-harness API experiment

Status: **provisional_incomplete**. 537 valid runs, 14 failed attempts, 3769 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 32 | 6/32 (18.8%) | 26/32 (81.2%) | 18/28 (64.3%) | 12/18 (66.7%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 34 | 4/34 (11.8%) | 28/34 (82.4%) | 22/30 (73.3%) | 15/22 (68.2%) |
| claude-code | glm-5.2 | neutral | 24 | 6/24 (25.0%) | 20/24 (83.3%) | 11/20 (55.0%) | 6/11 (54.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 23 | 2/23 (8.7%) | 21/23 (91.3%) | 10/19 (52.6%) | 9/10 (90.0%) |
| claude-code | qwen3.7-max | neutral | 34 | 7/34 (20.6%) | 32/34 (94.1%) | 10/26 (38.5%) | 8/10 (80.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 34 | 3/34 (8.8%) | 33/34 (97.1%) | 11/26 (42.3%) | 10/11 (90.9%) |
| codex | deepseek-v4-flash | neutral | 32 | 9/32 (28.1%) | 29/32 (90.6%) | 9/23 (39.1%) | 8/9 (88.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 33 | 7/33 (21.2%) | 30/33 (90.9%) | 9/23 (39.1%) | 8/9 (88.9%) |
| codex | glm-5.2 | neutral | 24 | 6/24 (25.0%) | 22/24 (91.7%) | 6/18 (33.3%) | 3/6 (50.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 24 | 4/24 (16.7%) | 23/24 (95.8%) | 7/18 (38.9%) | 5/7 (71.4%) |
| codex | qwen3.7-max | neutral | 32 | 13/32 (40.6%) | 30/32 (93.8%) | 8/27 (29.6%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 32 | 8/32 (25.0%) | 29/32 (90.6%) | 10/27 (37.0%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 29 | 7/29 (24.1%) | 27/29 (93.1%) | 10/20 (50.0%) | 9/10 (90.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 29 | 4/29 (13.8%) | 25/29 (86.2%) | 11/20 (55.0%) | 6/11 (54.5%) |
| deepseek-harness | glm-5.2 | neutral | 25 | 5/25 (20.0%) | 25/25 (100.0%) | 12/22 (54.5%) | 11/12 (91.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 26 | 3/26 (11.5%) | 25/26 (96.2%) | 12/22 (54.5%) | 12/12 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 35 | 11/35 (31.4%) | 31/35 (88.6%) | 5/29 (17.2%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 35 | 3/35 (8.6%) | 31/35 (88.6%) | 11/29 (37.9%) | 9/11 (81.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
