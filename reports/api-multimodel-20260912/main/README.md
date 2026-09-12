# Three-harness API experiment

Status: **provisional_incomplete**. 1910 valid runs, 73 failed attempts, 2337 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 110 | 30/110 (27.3%) | 95/110 (86.4%) | 52/81 (64.2%) | 32/52 (61.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 112 | 22/112 (19.6%) | 94/112 (83.9%) | 53/83 (63.9%) | 34/53 (64.2%) |
| claude-code | glm-5.2 | neutral | 111 | 18/111 (16.2%) | 100/111 (90.1%) | 51/86 (59.3%) | 39/51 (76.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 109 | 10/109 (9.2%) | 99/109 (90.8%) | 47/83 (56.6%) | 38/47 (80.9%) |
| claude-code | qwen3.7-max | neutral | 110 | 28/110 (25.5%) | 105/110 (95.5%) | 33/83 (39.8%) | 23/33 (69.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 110 | 11/110 (10.0%) | 106/110 (96.4%) | 40/83 (48.2%) | 34/41 (82.9%) |
| codex | deepseek-v4-flash | neutral | 107 | 27/107 (25.2%) | 95/107 (88.8%) | 34/81 (42.0%) | 25/34 (73.5%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 110 | 16/110 (14.5%) | 98/110 (89.1%) | 30/82 (36.6%) | 21/30 (70.0%) |
| codex | glm-5.2 | neutral | 91 | 22/91 (24.2%) | 82/91 (90.1%) | 26/68 (38.2%) | 21/26 (80.8%) |
| codex | glm-5.2 | prompt_guard_v1 | 89 | 11/89 (12.4%) | 84/89 (94.4%) | 30/66 (45.5%) | 28/30 (93.3%) |
| codex | qwen3.7-max | neutral | 114 | 40/114 (35.1%) | 109/114 (95.6%) | 23/86 (26.7%) | 16/23 (69.6%) |
| codex | qwen3.7-max | prompt_guard_v1 | 112 | 18/112 (16.1%) | 105/112 (93.8%) | 35/85 (41.2%) | 27/35 (77.1%) |
| deepseek-harness | deepseek-v4-flash | neutral | 111 | 31/111 (27.9%) | 98/111 (88.3%) | 45/85 (52.9%) | 32/45 (71.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 111 | 19/111 (17.1%) | 98/111 (88.3%) | 49/85 (57.6%) | 34/49 (69.4%) |
| deepseek-harness | glm-5.2 | neutral | 90 | 16/90 (17.8%) | 85/90 (94.4%) | 30/65 (46.2%) | 25/30 (83.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 89 | 7/89 (7.9%) | 83/89 (93.3%) | 36/65 (55.4%) | 31/36 (86.1%) |
| deepseek-harness | qwen3.7-max | neutral | 112 | 35/112 (31.2%) | 107/112 (95.5%) | 21/86 (24.4%) | 14/21 (66.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 112 | 12/112 (10.7%) | 106/112 (94.6%) | 29/86 (33.7%) | 25/29 (86.2%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
