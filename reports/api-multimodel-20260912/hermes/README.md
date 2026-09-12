# Hermes extension

Status: **provisional_incomplete**. 833 valid runs, 15 failed attempts, 592 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 139 | 45/139 (32.4%) | 121/139 (87.1%) | 54/106 (50.9%) | 36/54 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 138 | 22/138 (15.9%) | 123/138 (89.1%) | 53/107 (49.5%) | 40/54 (74.1%) |
| hermes | glm-5.2 | neutral | 133 | 32/133 (24.1%) | 122/133 (91.7%) | 50/104 (48.1%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 135 | 16/135 (11.9%) | 128/135 (94.8%) | 59/103 (57.3%) | 50/59 (84.7%) |
| hermes | qwen3.7-max | neutral | 144 | 37/144 (25.7%) | 131/144 (91.0%) | 25/108 (23.1%) | 19/25 (76.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 144 | 19/144 (13.2%) | 136/144 (94.4%) | 40/107 (37.4%) | 32/40 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
