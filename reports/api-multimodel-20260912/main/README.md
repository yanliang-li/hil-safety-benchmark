# Three-harness API experiment

Status: **provisional_incomplete**. 2872 valid runs, 97 failed attempts, 1351 pending out of 4320 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 166 | 41/166 (24.7%) | 141/166 (84.9%) | 76/125 (60.8%) | 50/77 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 166 | 30/166 (18.1%) | 140/166 (84.3%) | 77/125 (61.6%) | 54/78 (69.2%) |
| claude-code | glm-5.2 | neutral | 165 | 28/165 (17.0%) | 151/165 (91.5%) | 71/124 (57.3%) | 56/72 (77.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 165 | 19/165 (11.5%) | 151/165 (91.5%) | 72/124 (58.1%) | 57/72 (79.2%) |
| claude-code | qwen3.7-max | neutral | 165 | 50/165 (30.3%) | 156/165 (94.5%) | 50/124 (40.3%) | 33/50 (66.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 165 | 20/165 (12.1%) | 157/165 (95.2%) | 61/124 (49.2%) | 50/62 (80.6%) |
| codex | deepseek-v4-flash | neutral | 159 | 37/159 (23.3%) | 143/159 (89.9%) | 49/118 (41.5%) | 34/49 (69.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 161 | 24/161 (14.9%) | 145/161 (90.1%) | 47/120 (39.2%) | 33/47 (70.2%) |
| codex | glm-5.2 | neutral | 152 | 35/152 (23.0%) | 140/152 (92.1%) | 43/111 (38.7%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 149 | 18/149 (12.1%) | 139/149 (93.3%) | 48/107 (44.9%) | 45/48 (93.8%) |
| codex | qwen3.7-max | neutral | 160 | 54/160 (33.8%) | 151/160 (94.4%) | 32/120 (26.7%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 160 | 22/160 (13.8%) | 150/160 (93.8%) | 49/122 (40.2%) | 39/49 (79.6%) |
| deepseek-harness | deepseek-v4-flash | neutral | 161 | 45/161 (28.0%) | 143/161 (88.8%) | 67/122 (54.9%) | 49/67 (73.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 163 | 25/163 (15.3%) | 145/163 (89.0%) | 73/123 (59.3%) | 54/74 (73.0%) |
| deepseek-harness | glm-5.2 | neutral | 147 | 27/147 (18.4%) | 138/147 (93.9%) | 54/105 (51.4%) | 43/54 (79.6%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 138 | 13/138 (9.4%) | 130/138 (94.2%) | 59/100 (59.0%) | 50/59 (84.7%) |
| deepseek-harness | qwen3.7-max | neutral | 165 | 48/165 (29.1%) | 157/165 (95.2%) | 35/124 (28.2%) | 25/35 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 165 | 18/165 (10.9%) | 156/165 (94.5%) | 46/124 (37.1%) | 40/46 (87.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
