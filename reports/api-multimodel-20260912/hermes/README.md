# Hermes extension

Status: **provisional_incomplete**. 881 valid runs, 16 failed attempts, 543 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 147 | 46/147 (31.3%) | 127/147 (86.4%) | 57/110 (51.8%) | 37/57 (64.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 144 | 23/144 (16.0%) | 129/144 (89.6%) | 54/109 (49.5%) | 41/55 (74.5%) |
| hermes | glm-5.2 | neutral | 141 | 32/141 (22.7%) | 130/141 (92.2%) | 50/109 (45.9%) | 41/50 (82.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 144 | 16/144 (11.1%) | 137/144 (95.1%) | 60/109 (55.0%) | 50/60 (83.3%) |
| hermes | qwen3.7-max | neutral | 153 | 41/153 (26.8%) | 140/153 (91.5%) | 27/116 (23.3%) | 20/27 (74.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 152 | 19/152 (12.5%) | 143/152 (94.1%) | 44/114 (38.6%) | 35/44 (79.5%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
