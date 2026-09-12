# Hermes extension

Status: **provisional_incomplete**. 1045 valid runs, 25 failed attempts, 370 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 177 | 55/177 (31.1%) | 154/177 (87.0%) | 68/133 (51.1%) | 45/68 (66.2%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 172 | 29/172 (16.9%) | 156/172 (90.7%) | 68/130 (52.3%) | 52/69 (75.4%) |
| hermes | glm-5.2 | neutral | 170 | 37/170 (21.8%) | 158/170 (92.9%) | 61/126 (48.4%) | 51/61 (83.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 172 | 20/172 (11.6%) | 164/172 (95.3%) | 73/126 (57.9%) | 61/73 (83.6%) |
| hermes | qwen3.7-max | neutral | 177 | 46/177 (26.0%) | 163/177 (92.1%) | 32/135 (23.7%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 177 | 19/177 (10.7%) | 167/177 (94.4%) | 51/134 (38.1%) | 42/51 (82.4%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
