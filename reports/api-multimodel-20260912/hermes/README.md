# Hermes extension

Status: **provisional_incomplete**. 947 valid runs, 25 failed attempts, 468 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 160 | 49/160 (30.6%) | 138/160 (86.2%) | 61/119 (51.3%) | 40/61 (65.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 157 | 25/157 (15.9%) | 142/157 (90.4%) | 58/118 (49.2%) | 45/59 (76.3%) |
| hermes | glm-5.2 | neutral | 153 | 33/153 (21.6%) | 141/153 (92.2%) | 56/117 (47.9%) | 46/56 (82.1%) |
| hermes | glm-5.2 | prompt_guard_v1 | 160 | 19/160 (11.9%) | 152/160 (95.0%) | 69/120 (57.5%) | 57/69 (82.6%) |
| hermes | qwen3.7-max | neutral | 159 | 42/159 (26.4%) | 146/159 (91.8%) | 27/120 (22.5%) | 20/27 (74.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 158 | 19/158 (12.0%) | 149/158 (94.3%) | 45/119 (37.8%) | 36/45 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
