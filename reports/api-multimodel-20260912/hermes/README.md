# Hermes extension

Status: **provisional_incomplete**. 295 valid runs, 7 failed attempts, 1138 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 52 | 16/52 (30.8%) | 44/52 (84.6%) | 20/38 (52.6%) | 15/20 (75.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 50 | 9/50 (18.0%) | 43/50 (86.0%) | 18/36 (50.0%) | 12/18 (66.7%) |
| hermes | glm-5.2 | neutral | 42 | 10/42 (23.8%) | 36/42 (85.7%) | 13/33 (39.4%) | 8/13 (61.5%) |
| hermes | glm-5.2 | prompt_guard_v1 | 45 | 5/45 (11.1%) | 43/45 (95.6%) | 18/35 (51.4%) | 14/18 (77.8%) |
| hermes | qwen3.7-max | neutral | 52 | 13/52 (25.0%) | 49/52 (94.2%) | 10/39 (25.6%) | 8/10 (80.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 54 | 6/54 (11.1%) | 51/54 (94.4%) | 16/40 (40.0%) | 14/16 (87.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
