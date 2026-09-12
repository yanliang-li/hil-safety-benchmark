# Hermes extension

Status: **complete**. 1400 valid runs, 40 failed attempts, 0 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 233 | 73/233 (31.3%) | 203/233 (87.1%) | 83/175 (47.4%) | 54/83 (65.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 230 | 40/230 (17.4%) | 211/230 (91.7%) | 88/172 (51.2%) | 65/89 (73.0%) |
| hermes | glm-5.2 | neutral | 232 | 54/232 (23.3%) | 215/232 (92.7%) | 80/176 (45.5%) | 65/80 (81.2%) |
| hermes | glm-5.2 | prompt_guard_v1 | 234 | 28/234 (12.0%) | 223/234 (95.3%) | 105/176 (59.7%) | 88/105 (83.8%) |
| hermes | qwen3.7-max | neutral | 234 | 61/234 (26.1%) | 217/234 (92.7%) | 41/175 (23.4%) | 32/41 (78.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 237 | 29/237 (12.2%) | 224/237 (94.5%) | 65/178 (36.5%) | 52/65 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
