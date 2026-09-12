# Hermes extension

Status: **provisional_incomplete**. 651 valid runs, 10 failed attempts, 779 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 111 | 35/111 (31.5%) | 98/111 (88.3%) | 42/83 (50.6%) | 30/42 (71.4%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 108 | 17/108 (15.7%) | 96/108 (88.9%) | 41/83 (49.4%) | 32/42 (76.2%) |
| hermes | glm-5.2 | neutral | 100 | 23/100 (23.0%) | 91/100 (91.0%) | 38/77 (49.4%) | 31/38 (81.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 104 | 12/104 (11.5%) | 99/104 (95.2%) | 46/81 (56.8%) | 39/46 (84.8%) |
| hermes | qwen3.7-max | neutral | 114 | 31/114 (27.2%) | 104/114 (91.2%) | 21/87 (24.1%) | 16/21 (76.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 114 | 14/114 (12.3%) | 107/114 (93.9%) | 35/86 (40.7%) | 28/35 (80.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
