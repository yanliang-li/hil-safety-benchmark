# Hermes extension

Status: **provisional_incomplete**. 14 valid runs, 0 failed attempts, 1426 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 2 | 1/2 (50.0%) | 2/2 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 2 | 1/2 (50.0%) | 2/2 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | glm-5.2 | neutral | 2 | 1/2 (50.0%) | 2/2 (100.0%) | 0/2 (0.0%) | N/A |
| hermes | glm-5.2 | prompt_guard_v1 | 2 | 1/2 (50.0%) | 2/2 (100.0%) | 0/2 (0.0%) | N/A |
| hermes | qwen3.7-max | neutral | 3 | 0/3 (0.0%) | 2/3 (66.7%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 3 | 1/3 (33.3%) | 3/3 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
