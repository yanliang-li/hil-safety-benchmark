# Three-harness API experiment

Status: **provisional_incomplete**. 1631 valid runs, 65 failed attempts, 2624 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 90 | 26/90 (28.9%) | 76/90 (84.4%) | 43/67 (64.2%) | 25/43 (58.1%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 91 | 17/91 (18.7%) | 75/91 (82.4%) | 45/68 (66.2%) | 27/45 (60.0%) |
| claude-code | glm-5.2 | neutral | 88 | 14/88 (15.9%) | 81/88 (92.0%) | 39/67 (58.2%) | 32/39 (82.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 88 | 9/88 (10.2%) | 80/88 (90.9%) | 40/67 (59.7%) | 33/40 (82.5%) |
| claude-code | qwen3.7-max | neutral | 96 | 25/96 (26.0%) | 91/96 (94.8%) | 27/71 (38.0%) | 19/27 (70.4%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 97 | 10/97 (10.3%) | 93/97 (95.9%) | 32/71 (45.1%) | 28/33 (84.8%) |
| codex | deepseek-v4-flash | neutral | 93 | 25/93 (26.9%) | 83/93 (89.2%) | 29/69 (42.0%) | 21/29 (72.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 97 | 16/97 (16.5%) | 87/97 (89.7%) | 27/71 (38.0%) | 19/27 (70.4%) |
| codex | glm-5.2 | neutral | 79 | 22/79 (27.8%) | 71/79 (89.9%) | 20/57 (35.1%) | 15/20 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 80 | 11/80 (13.8%) | 75/80 (93.8%) | 25/58 (43.1%) | 23/25 (92.0%) |
| codex | qwen3.7-max | neutral | 93 | 34/93 (36.6%) | 88/93 (94.6%) | 19/71 (26.8%) | 12/19 (63.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 91 | 15/91 (16.5%) | 84/91 (92.3%) | 29/70 (41.4%) | 21/29 (72.4%) |
| deepseek-harness | deepseek-v4-flash | neutral | 94 | 25/94 (26.6%) | 83/94 (88.3%) | 39/73 (53.4%) | 27/39 (69.2%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 92 | 14/92 (15.2%) | 83/92 (90.2%) | 43/71 (60.6%) | 30/43 (69.8%) |
| deepseek-harness | glm-5.2 | neutral | 81 | 13/81 (16.0%) | 77/81 (95.1%) | 27/57 (47.4%) | 23/27 (85.2%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 79 | 7/79 (8.9%) | 74/79 (93.7%) | 31/56 (55.4%) | 27/31 (87.1%) |
| deepseek-harness | qwen3.7-max | neutral | 99 | 29/99 (29.3%) | 95/99 (96.0%) | 19/76 (25.0%) | 14/19 (73.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 103 | 12/103 (11.7%) | 98/103 (95.1%) | 26/78 (33.3%) | 23/26 (88.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
