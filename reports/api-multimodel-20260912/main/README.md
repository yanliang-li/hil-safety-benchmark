# Three-harness API experiment

Status: **provisional_incomplete**. 2719 valid runs, 92 failed attempts, 1509 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 156 | 40/156 (25.6%) | 132/156 (84.6%) | 71/117 (60.7%) | 45/72 (62.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 156 | 28/156 (17.9%) | 131/156 (84.0%) | 72/117 (61.5%) | 49/73 (67.1%) |
| claude-code | glm-5.2 | neutral | 152 | 24/152 (15.8%) | 138/152 (90.8%) | 69/115 (60.0%) | 55/70 (78.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 152 | 17/152 (11.2%) | 139/152 (91.4%) | 68/115 (59.1%) | 55/68 (80.9%) |
| claude-code | qwen3.7-max | neutral | 157 | 47/157 (29.9%) | 149/157 (94.9%) | 46/117 (39.3%) | 30/46 (65.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 160 | 20/160 (12.5%) | 152/160 (95.0%) | 60/120 (50.0%) | 50/61 (82.0%) |
| codex | deepseek-v4-flash | neutral | 152 | 37/152 (24.3%) | 137/152 (90.1%) | 47/113 (41.6%) | 32/47 (68.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 154 | 24/154 (15.6%) | 139/154 (90.3%) | 42/114 (36.8%) | 29/42 (69.0%) |
| codex | glm-5.2 | neutral | 140 | 32/140 (22.9%) | 129/140 (92.1%) | 39/103 (37.9%) | 30/39 (76.9%) |
| codex | glm-5.2 | prompt_guard_v1 | 141 | 17/141 (12.1%) | 132/141 (93.6%) | 46/103 (44.7%) | 43/46 (93.5%) |
| codex | qwen3.7-max | neutral | 155 | 53/155 (34.2%) | 146/155 (94.2%) | 32/116 (27.6%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 154 | 22/154 (14.3%) | 144/154 (93.5%) | 48/117 (41.0%) | 38/48 (79.2%) |
| deepseek-harness | deepseek-v4-flash | neutral | 154 | 44/154 (28.6%) | 136/154 (88.3%) | 65/118 (55.1%) | 47/65 (72.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 154 | 24/154 (15.6%) | 136/154 (88.3%) | 68/117 (58.1%) | 50/69 (72.5%) |
| deepseek-harness | glm-5.2 | neutral | 136 | 25/136 (18.4%) | 127/136 (93.4%) | 47/97 (48.5%) | 39/47 (83.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 129 | 13/129 (10.1%) | 121/129 (93.8%) | 53/93 (57.0%) | 45/53 (84.9%) |
| deepseek-harness | qwen3.7-max | neutral | 159 | 46/159 (28.9%) | 151/159 (95.0%) | 32/119 (26.9%) | 23/32 (71.9%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 158 | 16/158 (10.1%) | 149/158 (94.3%) | 42/118 (35.6%) | 37/42 (88.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
