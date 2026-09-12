# Hermes extension

Status: **provisional_incomplete**. 376 valid runs, 8 failed attempts, 1056 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 64 | 18/64 (28.1%) | 55/64 (85.9%) | 25/48 (52.1%) | 20/25 (80.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 62 | 10/62 (16.1%) | 53/62 (85.5%) | 22/47 (46.8%) | 16/23 (69.6%) |
| hermes | glm-5.2 | neutral | 57 | 14/57 (24.6%) | 51/57 (89.5%) | 20/46 (43.5%) | 15/20 (75.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 57 | 7/57 (12.3%) | 55/57 (96.5%) | 24/46 (52.2%) | 20/24 (83.3%) |
| hermes | qwen3.7-max | neutral | 67 | 15/67 (22.4%) | 60/67 (89.6%) | 12/51 (23.5%) | 9/12 (75.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 69 | 8/69 (11.6%) | 64/69 (92.8%) | 19/52 (36.5%) | 15/19 (78.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
