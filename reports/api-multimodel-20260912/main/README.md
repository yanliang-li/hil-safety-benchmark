# Three-harness API experiment

Status: **provisional_incomplete**. 2492 valid runs, 87 failed attempts, 1741 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 141 | 37/141 (26.2%) | 120/141 (85.1%) | 66/106 (62.3%) | 42/66 (63.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 141 | 25/141 (17.7%) | 119/141 (84.4%) | 66/106 (62.3%) | 47/67 (70.1%) |
| claude-code | glm-5.2 | neutral | 147 | 23/147 (15.6%) | 134/147 (91.2%) | 66/111 (59.5%) | 52/66 (78.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 147 | 16/147 (10.9%) | 134/147 (91.2%) | 66/111 (59.5%) | 53/66 (80.3%) |
| claude-code | qwen3.7-max | neutral | 145 | 42/145 (29.0%) | 138/145 (95.2%) | 43/107 (40.2%) | 28/43 (65.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 145 | 17/145 (11.7%) | 138/145 (95.2%) | 53/107 (49.5%) | 45/54 (83.3%) |
| codex | deepseek-v4-flash | neutral | 139 | 36/139 (25.9%) | 124/139 (89.2%) | 43/105 (41.0%) | 30/43 (69.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 139 | 21/139 (15.1%) | 124/139 (89.2%) | 39/105 (37.1%) | 26/39 (66.7%) |
| codex | glm-5.2 | neutral | 127 | 30/127 (23.6%) | 116/127 (91.3%) | 35/93 (37.6%) | 28/35 (80.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 129 | 15/129 (11.6%) | 120/129 (93.0%) | 43/95 (45.3%) | 41/43 (95.3%) |
| codex | qwen3.7-max | neutral | 145 | 50/145 (34.5%) | 139/145 (95.9%) | 30/108 (27.8%) | 21/30 (70.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 145 | 22/145 (15.2%) | 137/145 (94.5%) | 44/110 (40.0%) | 35/44 (79.5%) |
| deepseek-harness | deepseek-v4-flash | neutral | 136 | 37/136 (27.2%) | 119/136 (87.5%) | 57/104 (54.8%) | 40/57 (70.2%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 136 | 22/136 (16.2%) | 119/136 (87.5%) | 63/104 (60.6%) | 45/64 (70.3%) |
| deepseek-harness | glm-5.2 | neutral | 124 | 23/124 (18.5%) | 116/124 (93.5%) | 43/88 (48.9%) | 35/43 (81.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 118 | 12/118 (10.2%) | 111/118 (94.1%) | 48/84 (57.1%) | 41/48 (85.4%) |
| deepseek-harness | qwen3.7-max | neutral | 145 | 41/145 (28.3%) | 138/145 (95.2%) | 29/108 (26.9%) | 21/29 (72.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 143 | 15/143 (10.5%) | 135/143 (94.4%) | 37/107 (34.6%) | 32/37 (86.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
