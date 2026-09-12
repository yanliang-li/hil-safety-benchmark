# Hermes extension

Status: **provisional_incomplete**. 459 valid runs, 9 failed attempts, 972 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 77 | 23/77 (29.9%) | 67/77 (87.0%) | 31/58 (53.4%) | 23/31 (74.2%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 75 | 12/75 (16.0%) | 66/75 (88.0%) | 27/57 (47.4%) | 21/28 (75.0%) |
| hermes | glm-5.2 | neutral | 75 | 17/75 (22.7%) | 67/75 (89.3%) | 26/57 (45.6%) | 20/26 (76.9%) |
| hermes | glm-5.2 | prompt_guard_v1 | 78 | 10/78 (12.8%) | 74/78 (94.9%) | 32/59 (54.2%) | 26/32 (81.2%) |
| hermes | qwen3.7-max | neutral | 76 | 17/76 (22.4%) | 69/76 (90.8%) | 14/58 (24.1%) | 11/14 (78.6%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 78 | 10/78 (12.8%) | 73/78 (93.6%) | 20/58 (34.5%) | 16/20 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
