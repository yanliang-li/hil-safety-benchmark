# Hermes extension

Status: **provisional_incomplete**. 37 valid runs, 0 failed attempts, 1403 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 4 | 2/4 (50.0%) | 4/4 (100.0%) | 2/4 (50.0%) | 2/2 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 3 | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | glm-5.2 | neutral | 6 | 1/6 (16.7%) | 6/6 (100.0%) | 2/5 (40.0%) | 2/2 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 7 | 1/7 (14.3%) | 7/7 (100.0%) | 3/6 (50.0%) | 3/3 (100.0%) |
| hermes | qwen3.7-max | neutral | 9 | 3/9 (33.3%) | 7/9 (77.8%) | 4/8 (50.0%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 8 | 2/8 (25.0%) | 8/8 (100.0%) | 5/7 (71.4%) | 4/5 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
