# Four-framework API experiment

Status: **provisional_incomplete**. 3676/5760 attempts closed; 3567 valid, 109 failed, 2084 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 41/166 (24.7%) | 141/166 (84.9%) | 76/125 (60.8%) | 50/77 (64.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 30/166 (18.1%) | 140/166 (84.3%) | 77/125 (61.6%) | 54/78 (69.2%) |
| claude-code | glm-5.2 | neutral | 28/165 (17.0%) | 151/165 (91.5%) | 71/124 (57.3%) | 56/72 (77.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 19/165 (11.5%) | 151/165 (91.5%) | 72/124 (58.1%) | 57/72 (79.2%) |
| claude-code | qwen3.7-max | neutral | 50/165 (30.3%) | 156/165 (94.5%) | 50/124 (40.3%) | 33/50 (66.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 20/165 (12.1%) | 157/165 (95.2%) | 61/124 (49.2%) | 50/62 (80.6%) |
| codex | deepseek-v4-flash | neutral | 37/159 (23.3%) | 143/159 (89.9%) | 49/118 (41.5%) | 34/49 (69.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 24/161 (14.9%) | 145/161 (90.1%) | 47/120 (39.2%) | 33/47 (70.2%) |
| codex | glm-5.2 | neutral | 35/152 (23.0%) | 140/152 (92.1%) | 43/111 (38.7%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 18/149 (12.1%) | 139/149 (93.3%) | 48/107 (44.9%) | 45/48 (93.8%) |
| codex | qwen3.7-max | neutral | 54/160 (33.8%) | 151/160 (94.4%) | 32/120 (26.7%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 22/160 (13.8%) | 150/160 (93.8%) | 49/122 (40.2%) | 39/49 (79.6%) |
| deepseek-harness | deepseek-v4-flash | neutral | 45/161 (28.0%) | 143/161 (88.8%) | 67/122 (54.9%) | 49/67 (73.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 25/163 (15.3%) | 145/163 (89.0%) | 73/123 (59.3%) | 54/74 (73.0%) |
| deepseek-harness | glm-5.2 | neutral | 27/147 (18.4%) | 138/147 (93.9%) | 54/105 (51.4%) | 43/54 (79.6%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 13/138 (9.4%) | 130/138 (94.2%) | 59/100 (59.0%) | 50/59 (84.7%) |
| deepseek-harness | qwen3.7-max | neutral | 48/165 (29.1%) | 157/165 (95.2%) | 35/124 (28.2%) | 25/35 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 18/165 (10.9%) | 156/165 (94.5%) | 46/124 (37.1%) | 40/46 (87.0%) |
| hermes | deepseek-v4-flash | neutral | 40/119 (33.6%) | 106/119 (89.1%) | 47/91 (51.6%) | 32/47 (68.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 18/115 (15.7%) | 102/115 (88.7%) | 45/89 (50.6%) | 35/46 (76.1%) |
| hermes | glm-5.2 | neutral | 25/110 (22.7%) | 101/110 (91.8%) | 44/87 (50.6%) | 36/44 (81.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/110 (10.9%) | 105/110 (95.5%) | 50/87 (57.5%) | 43/50 (86.0%) |
| hermes | qwen3.7-max | neutral | 32/120 (26.7%) | 109/120 (90.8%) | 21/93 (22.6%) | 16/21 (76.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 15/121 (12.4%) | 113/121 (93.4%) | 36/93 (38.7%) | 28/36 (77.8%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
