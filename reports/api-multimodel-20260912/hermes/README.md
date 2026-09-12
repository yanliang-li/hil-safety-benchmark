# Hermes extension

Status: **provisional_incomplete**. 1072 valid runs, 25 failed attempts, 343 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 179 | 56/179 (31.3%) | 156/179 (87.2%) | 69/135 (51.1%) | 46/69 (66.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 175 | 31/175 (17.7%) | 159/175 (90.9%) | 69/133 (51.9%) | 53/70 (75.7%) |
| hermes | glm-5.2 | neutral | 176 | 39/176 (22.2%) | 163/176 (92.6%) | 62/131 (47.3%) | 52/62 (83.9%) |
| hermes | glm-5.2 | prompt_guard_v1 | 180 | 20/180 (11.1%) | 171/180 (95.0%) | 78/133 (58.6%) | 65/78 (83.3%) |
| hermes | qwen3.7-max | neutral | 181 | 48/181 (26.5%) | 167/181 (92.3%) | 32/139 (23.0%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 181 | 20/181 (11.0%) | 171/181 (94.5%) | 51/138 (37.0%) | 42/51 (82.4%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
