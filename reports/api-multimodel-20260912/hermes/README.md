# Hermes extension

Status: **provisional_incomplete**. 921 valid runs, 24 failed attempts, 495 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 155 | 49/155 (31.6%) | 135/155 (87.1%) | 59/115 (51.3%) | 39/59 (66.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 150 | 25/150 (16.7%) | 135/150 (90.0%) | 56/113 (49.6%) | 43/57 (75.4%) |
| hermes | glm-5.2 | neutral | 149 | 33/149 (22.1%) | 138/149 (92.6%) | 54/114 (47.4%) | 44/54 (81.5%) |
| hermes | glm-5.2 | prompt_guard_v1 | 154 | 18/154 (11.7%) | 147/154 (95.5%) | 67/117 (57.3%) | 56/67 (83.6%) |
| hermes | qwen3.7-max | neutral | 157 | 42/157 (26.8%) | 144/157 (91.7%) | 27/119 (22.7%) | 20/27 (74.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 156 | 19/156 (12.2%) | 147/156 (94.2%) | 45/117 (38.5%) | 36/45 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
