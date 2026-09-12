# Hermes extension

Status: **provisional_incomplete**. 736 valid runs, 12 failed attempts, 692 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 125 | 41/125 (32.8%) | 110/125 (88.0%) | 50/95 (52.6%) | 34/50 (68.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 124 | 20/124 (16.1%) | 110/124 (88.7%) | 48/96 (50.0%) | 37/49 (75.5%) |
| hermes | glm-5.2 | neutral | 118 | 26/118 (22.0%) | 108/118 (91.5%) | 46/93 (49.5%) | 38/46 (82.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 116 | 12/116 (10.3%) | 110/116 (94.8%) | 53/92 (57.6%) | 45/53 (84.9%) |
| hermes | qwen3.7-max | neutral | 126 | 33/126 (26.2%) | 115/126 (91.3%) | 22/96 (22.9%) | 17/22 (77.3%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 127 | 16/127 (12.6%) | 119/127 (93.7%) | 37/96 (38.5%) | 29/37 (78.4%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
