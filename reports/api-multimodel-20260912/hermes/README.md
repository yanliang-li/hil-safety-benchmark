# Hermes extension

Status: **provisional_incomplete**. 583 valid runs, 10 failed attempts, 847 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 101 | 31/101 (30.7%) | 89/101 (88.1%) | 39/75 (52.0%) | 28/39 (71.8%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 97 | 16/97 (16.5%) | 87/97 (89.7%) | 36/73 (49.3%) | 28/37 (75.7%) |
| hermes | glm-5.2 | neutral | 90 | 22/90 (24.4%) | 82/90 (91.1%) | 33/68 (48.5%) | 27/33 (81.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 92 | 12/92 (13.0%) | 88/92 (95.7%) | 38/69 (55.1%) | 32/38 (84.2%) |
| hermes | qwen3.7-max | neutral | 101 | 26/101 (25.7%) | 91/101 (90.1%) | 18/77 (23.4%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 102 | 13/102 (12.7%) | 95/102 (93.1%) | 30/77 (39.0%) | 23/30 (76.7%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
