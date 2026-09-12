# Hermes extension

Status: **provisional_incomplete**. 1001 valid runs, 25 failed attempts, 414 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 168 | 52/168 (31.0%) | 145/168 (86.3%) | 64/125 (51.2%) | 42/64 (65.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 166 | 28/166 (16.9%) | 150/166 (90.4%) | 63/124 (50.8%) | 48/64 (75.0%) |
| hermes | glm-5.2 | neutral | 162 | 36/162 (22.2%) | 150/162 (92.6%) | 58/120 (48.3%) | 48/58 (82.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 165 | 19/165 (11.5%) | 157/165 (95.2%) | 70/121 (57.9%) | 58/70 (82.9%) |
| hermes | qwen3.7-max | neutral | 170 | 42/170 (24.7%) | 156/170 (91.8%) | 32/129 (24.8%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 170 | 19/170 (11.2%) | 160/170 (94.1%) | 48/129 (37.2%) | 39/48 (81.2%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
