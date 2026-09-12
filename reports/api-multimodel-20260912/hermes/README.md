# Hermes extension

Status: **provisional_incomplete**. 788 valid runs, 12 failed attempts, 640 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 135 | 43/135 (31.9%) | 117/135 (86.7%) | 53/103 (51.5%) | 36/53 (67.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 132 | 21/132 (15.9%) | 117/132 (88.6%) | 50/102 (49.0%) | 39/51 (76.5%) |
| hermes | glm-5.2 | neutral | 127 | 28/127 (22.0%) | 117/127 (92.1%) | 49/100 (49.0%) | 41/49 (83.7%) |
| hermes | glm-5.2 | prompt_guard_v1 | 125 | 14/125 (11.2%) | 119/125 (95.2%) | 56/98 (57.1%) | 48/56 (85.7%) |
| hermes | qwen3.7-max | neutral | 134 | 35/134 (26.1%) | 122/134 (91.0%) | 23/100 (23.0%) | 17/23 (73.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 135 | 17/135 (12.6%) | 127/135 (94.1%) | 39/100 (39.0%) | 31/39 (79.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
