# Hermes extension

Status: **provisional_incomplete**. 1385 valid runs, 31 failed attempts, 24 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 231 | 72/231 (31.2%) | 201/231 (87.0%) | 82/173 (47.4%) | 53/82 (64.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 230 | 40/230 (17.4%) | 211/230 (91.7%) | 88/172 (51.2%) | 65/89 (73.0%) |
| hermes | glm-5.2 | neutral | 227 | 54/227 (23.8%) | 211/227 (93.0%) | 78/171 (45.6%) | 64/78 (82.1%) |
| hermes | glm-5.2 | prompt_guard_v1 | 229 | 28/229 (12.2%) | 218/229 (95.2%) | 101/171 (59.1%) | 85/101 (84.2%) |
| hermes | qwen3.7-max | neutral | 232 | 61/232 (26.3%) | 215/232 (92.7%) | 41/174 (23.6%) | 32/41 (78.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 236 | 29/236 (12.3%) | 223/236 (94.5%) | 65/177 (36.7%) | 52/65 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
