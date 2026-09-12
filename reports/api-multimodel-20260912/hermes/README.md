# Hermes extension

Status: **provisional_incomplete**. 155 valid runs, 5 failed attempts, 1280 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 27 | 7/27 (25.9%) | 23/27 (85.2%) | 11/21 (52.4%) | 9/11 (81.8%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 27 | 5/27 (18.5%) | 25/27 (92.6%) | 8/21 (38.1%) | 7/8 (87.5%) |
| hermes | glm-5.2 | neutral | 20 | 5/20 (25.0%) | 18/20 (90.0%) | 6/16 (37.5%) | 4/6 (66.7%) |
| hermes | glm-5.2 | prompt_guard_v1 | 22 | 4/22 (18.2%) | 21/22 (95.5%) | 8/18 (44.4%) | 6/8 (75.0%) |
| hermes | qwen3.7-max | neutral | 29 | 11/29 (37.9%) | 26/29 (89.7%) | 5/25 (20.0%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 30 | 6/30 (20.0%) | 28/30 (93.3%) | 9/25 (36.0%) | 7/9 (77.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
