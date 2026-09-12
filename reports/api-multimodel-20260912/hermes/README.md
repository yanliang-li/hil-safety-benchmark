# Hermes extension

Status: **provisional_incomplete**. 414 valid runs, 9 failed attempts, 1017 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 70 | 20/70 (28.6%) | 61/70 (87.1%) | 27/53 (50.9%) | 22/27 (81.5%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 67 | 11/67 (16.4%) | 58/67 (86.6%) | 24/51 (47.1%) | 18/25 (72.0%) |
| hermes | glm-5.2 | neutral | 64 | 16/64 (25.0%) | 58/64 (90.6%) | 24/50 (48.0%) | 18/24 (75.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 68 | 8/68 (11.8%) | 66/68 (97.1%) | 29/52 (55.8%) | 25/29 (86.2%) |
| hermes | qwen3.7-max | neutral | 72 | 16/72 (22.2%) | 65/72 (90.3%) | 13/55 (23.6%) | 10/13 (76.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 73 | 9/73 (12.3%) | 68/73 (93.2%) | 19/55 (34.5%) | 15/19 (78.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
