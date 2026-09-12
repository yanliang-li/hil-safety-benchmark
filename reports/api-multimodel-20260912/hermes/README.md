# Hermes extension

Status: **provisional_incomplete**. 811 valid runs, 13 failed attempts, 616 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 136 | 43/136 (31.6%) | 118/136 (86.8%) | 53/104 (51.0%) | 36/53 (67.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 134 | 21/134 (15.7%) | 119/134 (88.8%) | 51/104 (49.0%) | 40/52 (76.9%) |
| hermes | glm-5.2 | neutral | 132 | 31/132 (23.5%) | 121/132 (91.7%) | 50/103 (48.5%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 132 | 15/132 (11.4%) | 125/132 (94.7%) | 59/102 (57.8%) | 50/59 (84.7%) |
| hermes | qwen3.7-max | neutral | 138 | 36/138 (26.1%) | 126/138 (91.3%) | 23/104 (22.1%) | 17/23 (73.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 139 | 18/139 (12.9%) | 131/139 (94.2%) | 39/104 (37.5%) | 31/39 (79.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
