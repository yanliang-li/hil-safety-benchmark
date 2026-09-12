# Three-harness API experiment

Status: **provisional_incomplete**. 1502 valid runs, 61 failed attempts, 2757 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 86 | 24/86 (27.9%) | 72/86 (83.7%) | 42/65 (64.6%) | 25/42 (59.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 86 | 17/86 (19.8%) | 70/86 (81.4%) | 43/65 (66.2%) | 25/43 (58.1%) |
| claude-code | glm-5.2 | neutral | 84 | 14/84 (16.7%) | 77/84 (91.7%) | 37/63 (58.7%) | 30/37 (81.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 83 | 9/83 (10.8%) | 75/83 (90.4%) | 38/63 (60.3%) | 31/38 (81.6%) |
| claude-code | qwen3.7-max | neutral | 91 | 24/91 (26.4%) | 86/91 (94.5%) | 25/67 (37.3%) | 17/25 (68.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 90 | 10/90 (11.1%) | 86/90 (95.6%) | 30/67 (44.8%) | 26/31 (83.9%) |
| codex | deepseek-v4-flash | neutral | 80 | 21/80 (26.2%) | 70/80 (87.5%) | 24/59 (40.7%) | 17/24 (70.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 86 | 13/86 (15.1%) | 76/86 (88.4%) | 25/62 (40.3%) | 18/25 (72.0%) |
| codex | glm-5.2 | neutral | 77 | 22/77 (28.6%) | 69/77 (89.6%) | 20/57 (35.1%) | 15/20 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 76 | 11/76 (14.5%) | 71/76 (93.4%) | 23/56 (41.1%) | 21/23 (91.3%) |
| codex | qwen3.7-max | neutral | 85 | 31/85 (36.5%) | 81/85 (95.3%) | 18/64 (28.1%) | 11/18 (61.1%) |
| codex | qwen3.7-max | prompt_guard_v1 | 85 | 13/85 (15.3%) | 79/85 (92.9%) | 28/65 (43.1%) | 21/28 (75.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 85 | 21/85 (24.7%) | 75/85 (88.2%) | 35/65 (53.8%) | 25/35 (71.4%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 84 | 12/84 (14.3%) | 76/84 (90.5%) | 38/64 (59.4%) | 28/38 (73.7%) |
| deepseek-harness | glm-5.2 | neutral | 71 | 12/71 (16.9%) | 68/71 (95.8%) | 25/50 (50.0%) | 21/25 (84.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 71 | 7/71 (9.9%) | 66/71 (93.0%) | 29/50 (58.0%) | 25/29 (86.2%) |
| deepseek-harness | qwen3.7-max | neutral | 91 | 26/91 (28.6%) | 87/91 (95.6%) | 18/69 (26.1%) | 14/18 (77.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 91 | 9/91 (9.9%) | 86/91 (94.5%) | 25/69 (36.2%) | 23/25 (92.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
