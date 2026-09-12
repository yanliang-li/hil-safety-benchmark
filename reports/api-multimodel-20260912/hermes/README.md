# Hermes extension

Status: **provisional_incomplete**. 859 valid runs, 15 failed attempts, 566 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 141 | 45/141 (31.9%) | 123/141 (87.2%) | 54/107 (50.5%) | 36/54 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 142 | 23/142 (16.2%) | 127/142 (89.4%) | 53/107 (49.5%) | 40/54 (74.1%) |
| hermes | glm-5.2 | neutral | 137 | 32/137 (23.4%) | 126/137 (92.0%) | 50/106 (47.2%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 139 | 16/139 (11.5%) | 132/139 (95.0%) | 59/106 (55.7%) | 50/59 (84.7%) |
| hermes | qwen3.7-max | neutral | 149 | 40/149 (26.8%) | 136/149 (91.3%) | 26/113 (23.0%) | 19/26 (73.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 151 | 19/151 (12.6%) | 142/151 (94.0%) | 43/113 (38.1%) | 34/43 (79.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
