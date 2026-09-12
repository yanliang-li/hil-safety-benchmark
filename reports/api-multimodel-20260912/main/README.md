# Three-harness API experiment

Status: **provisional_incomplete**. 1772 valid runs, 70 failed attempts, 2478 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 99 | 29/99 (29.3%) | 84/99 (84.8%) | 47/73 (64.4%) | 27/47 (57.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 97 | 19/97 (19.6%) | 81/97 (83.5%) | 47/71 (66.2%) | 29/47 (61.7%) |
| claude-code | glm-5.2 | neutral | 99 | 16/99 (16.2%) | 90/99 (90.9%) | 45/75 (60.0%) | 35/45 (77.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 98 | 10/98 (10.2%) | 88/98 (89.8%) | 44/75 (58.7%) | 36/44 (81.8%) |
| claude-code | qwen3.7-max | neutral | 102 | 27/102 (26.5%) | 97/102 (95.1%) | 30/76 (39.5%) | 21/30 (70.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 102 | 11/102 (10.8%) | 98/102 (96.1%) | 36/76 (47.4%) | 31/37 (83.8%) |
| codex | deepseek-v4-flash | neutral | 102 | 26/102 (25.5%) | 91/102 (89.2%) | 34/77 (44.2%) | 25/34 (73.5%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 105 | 16/105 (15.2%) | 93/105 (88.6%) | 29/79 (36.7%) | 20/29 (69.0%) |
| codex | glm-5.2 | neutral | 88 | 22/88 (25.0%) | 79/88 (89.8%) | 25/65 (38.5%) | 20/25 (80.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 85 | 11/85 (12.9%) | 80/85 (94.1%) | 27/62 (43.5%) | 25/27 (92.6%) |
| codex | qwen3.7-max | neutral | 104 | 39/104 (37.5%) | 99/104 (95.2%) | 20/76 (26.3%) | 13/20 (65.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 101 | 17/101 (16.8%) | 94/101 (93.1%) | 31/76 (40.8%) | 23/31 (74.2%) |
| deepseek-harness | deepseek-v4-flash | neutral | 101 | 27/101 (26.7%) | 90/101 (89.1%) | 44/79 (55.7%) | 31/44 (70.5%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 100 | 17/100 (17.0%) | 89/100 (89.0%) | 46/78 (59.0%) | 32/46 (69.6%) |
| deepseek-harness | glm-5.2 | neutral | 86 | 14/86 (16.3%) | 81/86 (94.2%) | 28/62 (45.2%) | 24/28 (85.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 83 | 7/83 (8.4%) | 78/83 (94.0%) | 33/60 (55.0%) | 29/33 (87.9%) |
| deepseek-harness | qwen3.7-max | neutral | 110 | 34/110 (30.9%) | 105/110 (95.5%) | 20/84 (23.8%) | 14/20 (70.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 110 | 12/110 (10.9%) | 104/110 (94.5%) | 28/84 (33.3%) | 24/28 (85.7%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
