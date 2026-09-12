# Four-framework API experiment

Status: **provisional_incomplete**. 3877/5760 attempts closed; 3764 valid, 113 failed, 1883 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 43/172 (25.0%) | 146/172 (84.9%) | 77/129 (59.7%) | 51/78 (65.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 32/172 (18.6%) | 146/172 (84.9%) | 78/129 (60.5%) | 55/79 (69.6%) |
| claude-code | glm-5.2 | neutral | 30/177 (16.9%) | 162/177 (91.5%) | 76/134 (56.7%) | 60/77 (77.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 20/177 (11.3%) | 162/177 (91.5%) | 77/134 (57.5%) | 61/77 (79.2%) |
| claude-code | qwen3.7-max | neutral | 51/174 (29.3%) | 165/174 (94.8%) | 53/132 (40.2%) | 36/53 (67.9%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 21/174 (12.1%) | 166/174 (95.4%) | 64/132 (48.5%) | 53/65 (81.5%) |
| codex | deepseek-v4-flash | neutral | 41/167 (24.6%) | 150/167 (89.8%) | 53/124 (42.7%) | 36/53 (67.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 26/170 (15.3%) | 152/170 (89.4%) | 50/126 (39.7%) | 34/50 (68.0%) |
| codex | glm-5.2 | neutral | 36/157 (22.9%) | 145/157 (92.4%) | 43/112 (38.4%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 19/154 (12.3%) | 144/154 (93.5%) | 49/109 (45.0%) | 46/49 (93.9%) |
| codex | qwen3.7-max | neutral | 56/174 (32.2%) | 164/174 (94.3%) | 37/131 (28.2%) | 27/37 (73.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 23/172 (13.4%) | 161/172 (93.6%) | 55/131 (42.0%) | 43/55 (78.2%) |
| deepseek-harness | deepseek-v4-flash | neutral | 49/168 (29.2%) | 149/168 (88.7%) | 68/128 (53.1%) | 49/68 (72.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 27/169 (16.0%) | 151/169 (89.3%) | 74/128 (57.8%) | 55/75 (73.3%) |
| deepseek-harness | glm-5.2 | neutral | 29/154 (18.8%) | 143/154 (92.9%) | 56/112 (50.0%) | 44/56 (78.6%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 15/147 (10.2%) | 139/147 (94.6%) | 61/108 (56.5%) | 51/61 (83.6%) |
| deepseek-harness | qwen3.7-max | neutral | 53/174 (30.5%) | 166/174 (95.4%) | 35/131 (26.7%) | 25/35 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 19/176 (10.8%) | 167/176 (94.9%) | 46/132 (34.8%) | 40/46 (87.0%) |
| hermes | deepseek-v4-flash | neutral | 41/125 (32.8%) | 110/125 (88.0%) | 50/95 (52.6%) | 34/50 (68.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 20/124 (16.1%) | 110/124 (88.7%) | 48/96 (50.0%) | 37/49 (75.5%) |
| hermes | glm-5.2 | neutral | 26/118 (22.0%) | 108/118 (91.5%) | 46/93 (49.5%) | 38/46 (82.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/116 (10.3%) | 110/116 (94.8%) | 53/92 (57.6%) | 45/53 (84.9%) |
| hermes | qwen3.7-max | neutral | 33/126 (26.2%) | 115/126 (91.3%) | 22/96 (22.9%) | 17/22 (77.3%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 16/127 (12.6%) | 119/127 (93.7%) | 37/96 (38.5%) | 29/37 (78.4%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
