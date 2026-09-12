# Hermes extension

Status: **provisional_incomplete**. 235 valid runs, 6 failed attempts, 1199 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 41 | 14/41 (34.1%) | 37/41 (90.2%) | 15/29 (51.7%) | 11/15 (73.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 41 | 9/41 (22.0%) | 38/41 (92.7%) | 12/29 (41.4%) | 10/12 (83.3%) |
| hermes | glm-5.2 | neutral | 36 | 8/36 (22.2%) | 30/36 (83.3%) | 12/28 (42.9%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 39 | 4/39 (10.3%) | 37/39 (94.9%) | 16/30 (53.3%) | 12/16 (75.0%) |
| hermes | qwen3.7-max | neutral | 39 | 12/39 (30.8%) | 36/39 (92.3%) | 5/31 (16.1%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 39 | 6/39 (15.4%) | 37/39 (94.9%) | 10/31 (32.3%) | 8/10 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
