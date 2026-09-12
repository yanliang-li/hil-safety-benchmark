# Hermes extension

Status: **provisional_incomplete**. 336 valid runs, 8 failed attempts, 1096 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 60 | 17/60 (28.3%) | 51/60 (85.0%) | 23/45 (51.1%) | 18/23 (78.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 56 | 10/56 (17.9%) | 49/56 (87.5%) | 19/41 (46.3%) | 14/20 (70.0%) |
| hermes | glm-5.2 | neutral | 50 | 13/50 (26.0%) | 44/50 (88.0%) | 16/41 (39.0%) | 11/16 (68.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 51 | 6/51 (11.8%) | 49/51 (96.1%) | 21/41 (51.2%) | 17/21 (81.0%) |
| hermes | qwen3.7-max | neutral | 59 | 14/59 (23.7%) | 54/59 (91.5%) | 10/46 (21.7%) | 8/10 (80.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 60 | 6/60 (10.0%) | 56/60 (93.3%) | 17/46 (37.0%) | 14/17 (82.4%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
