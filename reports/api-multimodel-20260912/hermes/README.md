# Hermes extension

Status: **provisional_incomplete**. 116 valid runs, 5 failed attempts, 1319 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 20 | 5/20 (25.0%) | 17/20 (85.0%) | 8/15 (53.3%) | 6/8 (75.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 19 | 2/19 (10.5%) | 17/19 (89.5%) | 6/14 (42.9%) | 5/6 (83.3%) |
| hermes | glm-5.2 | neutral | 17 | 4/17 (23.5%) | 15/17 (88.2%) | 4/13 (30.8%) | 4/4 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 17 | 3/17 (17.6%) | 16/17 (94.1%) | 5/13 (38.5%) | 5/5 (100.0%) |
| hermes | qwen3.7-max | neutral | 21 | 8/21 (38.1%) | 19/21 (90.5%) | 5/18 (27.8%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 22 | 4/22 (18.2%) | 21/22 (95.5%) | 8/18 (44.4%) | 7/8 (87.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
