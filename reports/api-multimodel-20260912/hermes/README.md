# Hermes extension

Status: **provisional_incomplete**. 82 valid runs, 4 failed attempts, 1354 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 13 | 3/13 (23.1%) | 10/13 (76.9%) | 5/10 (50.0%) | 4/5 (80.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 11 | 2/11 (18.2%) | 10/11 (90.9%) | 3/8 (37.5%) | 3/3 (100.0%) |
| hermes | glm-5.2 | neutral | 13 | 3/13 (23.1%) | 12/13 (92.3%) | 3/10 (30.0%) | 3/3 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 13 | 2/13 (15.4%) | 13/13 (100.0%) | 3/10 (30.0%) | 3/3 (100.0%) |
| hermes | qwen3.7-max | neutral | 16 | 5/16 (31.2%) | 14/16 (87.5%) | 4/14 (28.6%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 16 | 3/16 (18.8%) | 16/16 (100.0%) | 8/14 (57.1%) | 7/8 (87.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
