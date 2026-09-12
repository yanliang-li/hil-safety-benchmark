# Three-harness API experiment

Status: **provisional_incomplete**. 2639 valid runs, 91 failed attempts, 1590 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 153 | 40/153 (26.1%) | 130/153 (85.0%) | 70/114 (61.4%) | 44/71 (62.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 152 | 28/152 (18.4%) | 128/152 (84.2%) | 70/114 (61.4%) | 48/71 (67.6%) |
| claude-code | glm-5.2 | neutral | 151 | 23/151 (15.2%) | 137/151 (90.7%) | 69/114 (60.5%) | 55/70 (78.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 151 | 16/151 (10.6%) | 138/151 (91.4%) | 68/114 (59.6%) | 55/68 (80.9%) |
| claude-code | qwen3.7-max | neutral | 154 | 44/154 (28.6%) | 146/154 (94.8%) | 46/115 (40.0%) | 30/46 (65.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 153 | 18/153 (11.8%) | 146/153 (95.4%) | 57/114 (50.0%) | 48/58 (82.8%) |
| codex | deepseek-v4-flash | neutral | 147 | 36/147 (24.5%) | 132/147 (89.8%) | 46/111 (41.4%) | 31/46 (67.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 149 | 22/149 (14.8%) | 134/149 (89.9%) | 41/112 (36.6%) | 28/41 (68.3%) |
| codex | glm-5.2 | neutral | 135 | 31/135 (23.0%) | 124/135 (91.9%) | 36/99 (36.4%) | 28/36 (77.8%) |
| codex | glm-5.2 | prompt_guard_v1 | 136 | 15/136 (11.0%) | 127/136 (93.4%) | 46/99 (46.5%) | 43/46 (93.5%) |
| codex | qwen3.7-max | neutral | 153 | 52/153 (34.0%) | 144/153 (94.1%) | 32/115 (27.8%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 151 | 22/151 (14.6%) | 141/151 (93.4%) | 47/114 (41.2%) | 37/47 (78.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 144 | 40/144 (27.8%) | 126/144 (87.5%) | 60/110 (54.5%) | 42/60 (70.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 145 | 24/145 (16.6%) | 127/145 (87.6%) | 64/110 (58.2%) | 46/65 (70.8%) |
| deepseek-harness | glm-5.2 | neutral | 133 | 25/133 (18.8%) | 124/133 (93.2%) | 47/95 (49.5%) | 39/47 (83.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 126 | 13/126 (10.3%) | 118/126 (93.7%) | 51/90 (56.7%) | 43/51 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 153 | 43/153 (28.1%) | 146/153 (95.4%) | 32/115 (27.8%) | 23/32 (71.9%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 153 | 15/153 (9.8%) | 145/153 (94.8%) | 42/115 (36.5%) | 37/42 (88.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
