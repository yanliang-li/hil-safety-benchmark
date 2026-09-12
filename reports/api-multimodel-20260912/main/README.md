# Three-harness API experiment

Status: **provisional_incomplete**. 2195 valid runs, 80 failed attempts, 2045 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 128 | 33/128 (25.8%) | 109/128 (85.2%) | 62/96 (64.6%) | 39/62 (62.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 129 | 24/129 (18.6%) | 109/129 (84.5%) | 62/97 (63.9%) | 43/62 (69.4%) |
| claude-code | glm-5.2 | neutral | 126 | 20/126 (15.9%) | 114/126 (90.5%) | 59/96 (61.5%) | 46/59 (78.0%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 128 | 13/128 (10.2%) | 116/128 (90.6%) | 59/97 (60.8%) | 47/59 (79.7%) |
| claude-code | qwen3.7-max | neutral | 128 | 36/128 (28.1%) | 122/128 (95.3%) | 39/94 (41.5%) | 25/39 (64.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 128 | 16/128 (12.5%) | 123/128 (96.1%) | 48/94 (51.1%) | 40/49 (81.6%) |
| codex | deepseek-v4-flash | neutral | 121 | 32/121 (26.4%) | 108/121 (89.3%) | 39/91 (42.9%) | 27/39 (69.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 126 | 19/126 (15.1%) | 112/126 (88.9%) | 35/95 (36.8%) | 24/35 (68.6%) |
| codex | glm-5.2 | neutral | 109 | 25/109 (22.9%) | 99/109 (90.8%) | 32/82 (39.0%) | 26/32 (81.2%) |
| codex | glm-5.2 | prompt_guard_v1 | 108 | 12/108 (11.1%) | 101/108 (93.5%) | 38/81 (46.9%) | 36/38 (94.7%) |
| codex | qwen3.7-max | neutral | 127 | 44/127 (34.6%) | 121/127 (95.3%) | 25/95 (26.3%) | 18/25 (72.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 126 | 20/126 (15.9%) | 118/126 (93.7%) | 39/96 (40.6%) | 30/39 (76.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 124 | 35/124 (28.2%) | 109/124 (87.9%) | 48/94 (51.1%) | 34/48 (70.8%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 123 | 21/123 (17.1%) | 108/123 (87.8%) | 54/93 (58.1%) | 36/54 (66.7%) |
| deepseek-harness | glm-5.2 | neutral | 103 | 19/103 (18.4%) | 96/103 (93.2%) | 33/76 (43.4%) | 26/33 (78.8%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 101 | 10/101 (9.9%) | 94/101 (93.1%) | 40/75 (53.3%) | 33/40 (82.5%) |
| deepseek-harness | qwen3.7-max | neutral | 130 | 38/130 (29.2%) | 123/130 (94.6%) | 26/101 (25.7%) | 19/26 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 130 | 14/130 (10.8%) | 122/130 (93.8%) | 35/101 (34.7%) | 30/35 (85.7%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
