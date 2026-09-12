# Hermes extension

Status: **provisional_incomplete**. 189 valid runs, 6 failed attempts, 1245 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 34 | 10/34 (29.4%) | 30/34 (88.2%) | 12/24 (50.0%) | 10/12 (83.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 33 | 7/33 (21.2%) | 31/33 (93.9%) | 9/23 (39.1%) | 8/9 (88.9%) |
| hermes | glm-5.2 | neutral | 27 | 6/27 (22.2%) | 22/27 (81.5%) | 9/22 (40.9%) | 5/9 (55.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 29 | 4/29 (13.8%) | 27/29 (93.1%) | 12/23 (52.2%) | 8/12 (66.7%) |
| hermes | qwen3.7-max | neutral | 32 | 11/32 (34.4%) | 29/32 (90.6%) | 5/28 (17.9%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 34 | 6/34 (17.6%) | 32/34 (94.1%) | 9/28 (32.1%) | 7/9 (77.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
