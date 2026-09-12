# Hermes extension

Status: **provisional_incomplete**. 977 valid runs, 25 failed attempts, 438 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 165 | 51/165 (30.9%) | 143/165 (86.7%) | 62/122 (50.8%) | 41/62 (66.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 160 | 26/160 (16.2%) | 145/160 (90.6%) | 59/119 (49.6%) | 46/60 (76.7%) |
| hermes | glm-5.2 | neutral | 160 | 35/160 (21.9%) | 148/160 (92.5%) | 58/120 (48.3%) | 48/58 (82.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 163 | 19/163 (11.7%) | 155/163 (95.1%) | 70/121 (57.9%) | 58/70 (82.9%) |
| hermes | qwen3.7-max | neutral | 165 | 42/165 (25.5%) | 151/165 (91.5%) | 29/126 (23.0%) | 22/29 (75.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 164 | 19/164 (11.6%) | 154/164 (93.9%) | 47/124 (37.9%) | 38/47 (80.9%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
