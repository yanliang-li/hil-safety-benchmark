# Hermes extension

Status: **provisional_incomplete**. 257 valid runs, 7 failed attempts, 1176 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 47 | 16/47 (34.0%) | 40/47 (85.1%) | 17/34 (50.0%) | 12/17 (70.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 45 | 9/45 (20.0%) | 40/45 (88.9%) | 15/32 (46.9%) | 10/15 (66.7%) |
| hermes | glm-5.2 | neutral | 39 | 8/39 (20.5%) | 33/39 (84.6%) | 12/30 (40.0%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 41 | 4/41 (9.8%) | 39/41 (95.1%) | 16/31 (51.6%) | 12/16 (75.0%) |
| hermes | qwen3.7-max | neutral | 42 | 12/42 (28.6%) | 39/42 (92.9%) | 6/34 (17.6%) | 4/6 (66.7%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 43 | 6/43 (14.0%) | 41/43 (95.3%) | 12/34 (35.3%) | 10/12 (83.3%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
