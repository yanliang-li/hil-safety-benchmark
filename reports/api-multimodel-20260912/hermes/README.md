# Hermes extension

Status: **provisional_incomplete**. 30 valid runs, 0 failed attempts, 1410 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 3 | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 3 | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | glm-5.2 | neutral | 4 | 1/4 (25.0%) | 4/4 (100.0%) | 1/4 (25.0%) | 1/1 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 5 | 1/5 (20.0%) | 5/5 (100.0%) | 2/5 (40.0%) | 2/2 (100.0%) |
| hermes | qwen3.7-max | neutral | 8 | 3/8 (37.5%) | 7/8 (87.5%) | 4/7 (57.1%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 7 | 2/7 (28.6%) | 7/7 (100.0%) | 4/6 (66.7%) | 3/4 (75.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
