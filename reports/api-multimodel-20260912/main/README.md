# Three-harness API experiment

Status: **provisional_incomplete**. 666 valid runs, 25 failed attempts, 3629 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 42 | 7/42 (16.7%) | 34/42 (81.0%) | 26/38 (68.4%) | 18/26 (69.2%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 42 | 4/42 (9.5%) | 34/42 (81.0%) | 29/38 (76.3%) | 20/29 (69.0%) |
| claude-code | glm-5.2 | neutral | 37 | 7/37 (18.9%) | 30/37 (81.1%) | 16/29 (55.2%) | 10/16 (62.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 34 | 3/34 (8.8%) | 28/34 (82.4%) | 15/26 (57.7%) | 10/15 (66.7%) |
| claude-code | qwen3.7-max | neutral | 41 | 10/41 (24.4%) | 39/41 (95.1%) | 13/33 (39.4%) | 9/13 (69.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 41 | 3/41 (7.3%) | 40/41 (97.6%) | 14/33 (42.4%) | 13/14 (92.9%) |
| codex | deepseek-v4-flash | neutral | 39 | 12/39 (30.8%) | 35/39 (89.7%) | 11/27 (40.7%) | 8/11 (72.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 38 | 8/38 (21.1%) | 34/38 (89.5%) | 11/26 (42.3%) | 9/11 (81.8%) |
| codex | glm-5.2 | neutral | 33 | 7/33 (21.2%) | 29/33 (87.9%) | 9/25 (36.0%) | 6/9 (66.7%) |
| codex | glm-5.2 | prompt_guard_v1 | 31 | 4/31 (12.9%) | 29/31 (93.5%) | 9/22 (40.9%) | 7/9 (77.8%) |
| codex | qwen3.7-max | neutral | 37 | 14/37 (37.8%) | 35/37 (94.6%) | 8/29 (27.6%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 37 | 8/37 (21.6%) | 34/37 (91.9%) | 11/29 (37.9%) | 9/11 (81.8%) |
| deepseek-harness | deepseek-v4-flash | neutral | 37 | 7/37 (18.9%) | 34/37 (91.9%) | 15/25 (60.0%) | 13/15 (86.7%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37 | 5/37 (13.5%) | 33/37 (89.2%) | 15/25 (60.0%) | 10/15 (66.7%) |
| deepseek-harness | glm-5.2 | neutral | 32 | 6/32 (18.8%) | 32/32 (100.0%) | 14/25 (56.0%) | 12/14 (85.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 32 | 4/32 (12.5%) | 31/32 (96.9%) | 14/24 (58.3%) | 13/14 (92.9%) |
| deepseek-harness | qwen3.7-max | neutral | 38 | 11/38 (28.9%) | 34/38 (89.5%) | 5/29 (17.2%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 38 | 3/38 (7.9%) | 34/38 (89.5%) | 11/29 (37.9%) | 9/11 (81.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
