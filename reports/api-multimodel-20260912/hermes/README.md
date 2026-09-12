# Hermes extension

Status: **provisional_incomplete**. 1275 valid runs, 28 failed attempts, 137 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 212 | 65/212 (30.7%) | 185/212 (87.3%) | 77/160 (48.1%) | 50/77 (64.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 210 | 36/210 (17.1%) | 192/210 (91.4%) | 80/158 (50.6%) | 59/81 (72.8%) |
| hermes | glm-5.2 | neutral | 211 | 50/211 (23.7%) | 195/211 (92.4%) | 71/159 (44.7%) | 58/71 (81.7%) |
| hermes | glm-5.2 | prompt_guard_v1 | 215 | 24/215 (11.2%) | 204/215 (94.9%) | 95/160 (59.4%) | 80/95 (84.2%) |
| hermes | qwen3.7-max | neutral | 214 | 52/214 (24.3%) | 197/214 (92.1%) | 36/160 (22.5%) | 28/36 (77.8%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 213 | 23/213 (10.8%) | 202/213 (94.8%) | 56/158 (35.4%) | 46/56 (82.1%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
