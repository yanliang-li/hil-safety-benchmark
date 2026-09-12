# Hermes extension

Status: **provisional_incomplete**. 220 valid runs, 6 failed attempts, 1214 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 41 | 14/41 (34.1%) | 37/41 (90.2%) | 15/29 (51.7%) | 11/15 (73.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 38 | 8/38 (21.1%) | 35/38 (92.1%) | 11/26 (42.3%) | 9/11 (81.8%) |
| hermes | glm-5.2 | neutral | 32 | 7/32 (21.9%) | 26/32 (81.2%) | 12/27 (44.4%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 34 | 4/34 (11.8%) | 32/34 (94.1%) | 15/28 (53.6%) | 11/15 (73.3%) |
| hermes | qwen3.7-max | neutral | 37 | 12/37 (32.4%) | 34/37 (91.9%) | 5/30 (16.7%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 38 | 6/38 (15.8%) | 36/38 (94.7%) | 10/30 (33.3%) | 8/10 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
