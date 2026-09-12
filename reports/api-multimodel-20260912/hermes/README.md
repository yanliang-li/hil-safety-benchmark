# Hermes extension

Status: **provisional_incomplete**. 766 valid runs, 12 failed attempts, 662 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 132 | 42/132 (31.8%) | 114/132 (86.4%) | 51/100 (51.0%) | 34/51 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 130 | 21/130 (16.2%) | 115/130 (88.5%) | 48/100 (48.0%) | 37/49 (75.5%) |
| hermes | glm-5.2 | neutral | 122 | 27/122 (22.1%) | 112/122 (91.8%) | 47/96 (49.0%) | 39/47 (83.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 121 | 13/121 (10.7%) | 115/121 (95.0%) | 56/96 (58.3%) | 48/56 (85.7%) |
| hermes | qwen3.7-max | neutral | 130 | 35/130 (26.9%) | 118/130 (90.8%) | 23/98 (23.5%) | 17/23 (73.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 131 | 17/131 (13.0%) | 123/131 (93.9%) | 38/99 (38.4%) | 30/38 (78.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
