# Hermes extension

Status: **provisional_incomplete**. 628 valid runs, 10 failed attempts, 802 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 107 | 33/107 (30.8%) | 95/107 (88.8%) | 42/81 (51.9%) | 30/42 (71.4%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 106 | 16/106 (15.1%) | 94/106 (88.7%) | 41/81 (50.6%) | 32/42 (76.2%) |
| hermes | glm-5.2 | neutral | 99 | 23/99 (23.2%) | 90/99 (90.9%) | 38/77 (49.4%) | 31/38 (81.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 101 | 12/101 (11.9%) | 96/101 (95.0%) | 44/78 (56.4%) | 37/44 (84.1%) |
| hermes | qwen3.7-max | neutral | 107 | 30/107 (28.0%) | 97/107 (90.7%) | 18/80 (22.5%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 108 | 14/108 (13.0%) | 101/108 (93.5%) | 32/80 (40.0%) | 25/32 (78.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
