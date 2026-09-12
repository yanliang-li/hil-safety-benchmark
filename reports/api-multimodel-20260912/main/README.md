# Three-harness API experiment

Status: **provisional_incomplete**. 2334 valid runs, 82 failed attempts, 1904 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 135 | 36/135 (26.7%) | 115/135 (85.2%) | 64/102 (62.7%) | 41/64 (64.1%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 135 | 24/135 (17.8%) | 114/135 (84.4%) | 64/102 (62.7%) | 45/64 (70.3%) |
| claude-code | glm-5.2 | neutral | 137 | 22/137 (16.1%) | 124/137 (90.5%) | 62/104 (59.6%) | 48/62 (77.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 136 | 15/136 (11.0%) | 124/136 (91.2%) | 60/103 (58.3%) | 48/60 (80.0%) |
| claude-code | qwen3.7-max | neutral | 134 | 38/134 (28.4%) | 128/134 (95.5%) | 39/97 (40.2%) | 25/39 (64.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 134 | 17/134 (12.7%) | 129/134 (96.3%) | 49/97 (50.5%) | 41/50 (82.0%) |
| codex | deepseek-v4-flash | neutral | 132 | 34/132 (25.8%) | 118/132 (89.4%) | 41/101 (40.6%) | 29/41 (70.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 134 | 19/134 (14.2%) | 119/134 (88.8%) | 38/102 (37.3%) | 26/38 (68.4%) |
| codex | glm-5.2 | neutral | 122 | 29/122 (23.8%) | 111/122 (91.0%) | 35/91 (38.5%) | 28/35 (80.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 123 | 14/123 (11.4%) | 114/123 (92.7%) | 43/91 (47.3%) | 41/43 (95.3%) |
| codex | qwen3.7-max | neutral | 137 | 45/137 (32.8%) | 131/137 (95.6%) | 28/102 (27.5%) | 20/28 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 133 | 20/133 (15.0%) | 125/133 (94.0%) | 39/100 (39.0%) | 30/39 (76.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 129 | 35/129 (27.1%) | 113/129 (87.6%) | 51/97 (52.6%) | 36/51 (70.6%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 128 | 21/128 (16.4%) | 113/128 (88.3%) | 57/96 (59.4%) | 40/58 (69.0%) |
| deepseek-harness | glm-5.2 | neutral | 107 | 20/107 (18.7%) | 99/107 (92.5%) | 36/79 (45.6%) | 28/36 (77.8%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 105 | 11/105 (10.5%) | 98/105 (93.3%) | 43/78 (55.1%) | 36/43 (83.7%) |
| deepseek-harness | qwen3.7-max | neutral | 136 | 39/136 (28.7%) | 129/136 (94.9%) | 28/106 (26.4%) | 20/28 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 137 | 15/137 (10.9%) | 129/137 (94.2%) | 36/106 (34.0%) | 31/36 (86.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
