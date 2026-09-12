# Hermes extension

Status: **provisional_incomplete**. 695 valid runs, 12 failed attempts, 733 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 119 | 40/119 (33.6%) | 106/119 (89.1%) | 47/91 (51.6%) | 32/47 (68.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 115 | 18/115 (15.7%) | 102/115 (88.7%) | 45/89 (50.6%) | 35/46 (76.1%) |
| hermes | glm-5.2 | neutral | 110 | 25/110 (22.7%) | 101/110 (91.8%) | 44/87 (50.6%) | 36/44 (81.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 110 | 12/110 (10.9%) | 105/110 (95.5%) | 50/87 (57.5%) | 43/50 (86.0%) |
| hermes | qwen3.7-max | neutral | 120 | 32/120 (26.7%) | 109/120 (90.8%) | 21/93 (22.6%) | 16/21 (76.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 121 | 15/121 (12.4%) | 113/121 (93.4%) | 36/93 (38.7%) | 28/36 (77.8%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
