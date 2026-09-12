# Four-framework API experiment

Status: **provisional_incomplete**. 4086/5760 attempts closed; 3966 valid, 120 failed, 1674 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 45/180 (25.0%) | 151/180 (83.9%) | 80/134 (59.7%) | 51/81 (63.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 35/181 (19.3%) | 152/181 (84.0%) | 82/135 (60.7%) | 55/83 (66.3%) |
| claude-code | glm-5.2 | neutral | 32/193 (16.6%) | 178/193 (92.2%) | 81/144 (56.2%) | 63/82 (76.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 22/192 (11.5%) | 177/192 (92.2%) | 79/144 (54.9%) | 62/79 (78.5%) |
| claude-code | qwen3.7-max | neutral | 51/179 (28.5%) | 169/179 (94.4%) | 54/135 (40.0%) | 37/54 (68.5%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 21/178 (11.8%) | 170/178 (95.5%) | 65/134 (48.5%) | 54/66 (81.8%) |
| codex | deepseek-v4-flash | neutral | 44/176 (25.0%) | 159/176 (90.3%) | 57/133 (42.9%) | 40/57 (70.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 26/176 (14.8%) | 158/176 (89.8%) | 53/132 (40.2%) | 37/53 (69.8%) |
| codex | glm-5.2 | neutral | 36/163 (22.1%) | 150/163 (92.0%) | 43/116 (37.1%) | 34/43 (79.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 19/164 (11.6%) | 153/164 (93.3%) | 54/117 (46.2%) | 50/54 (92.6%) |
| codex | qwen3.7-max | neutral | 60/180 (33.3%) | 170/180 (94.4%) | 37/137 (27.0%) | 27/37 (73.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 24/178 (13.5%) | 167/178 (93.8%) | 57/137 (41.6%) | 45/57 (78.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 52/176 (29.5%) | 156/176 (88.6%) | 69/134 (51.5%) | 49/69 (71.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 27/177 (15.3%) | 158/177 (89.3%) | 78/134 (58.2%) | 58/79 (73.4%) |
| deepseek-harness | glm-5.2 | neutral | 33/161 (20.5%) | 150/161 (93.2%) | 59/119 (49.6%) | 46/59 (78.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 18/153 (11.8%) | 145/153 (94.8%) | 65/113 (57.5%) | 54/65 (83.1%) |
| deepseek-harness | qwen3.7-max | neutral | 55/185 (29.7%) | 177/185 (95.7%) | 39/140 (27.9%) | 28/39 (71.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 20/186 (10.8%) | 177/186 (95.2%) | 50/140 (35.7%) | 43/50 (86.0%) |
| hermes | deepseek-v4-flash | neutral | 43/135 (31.9%) | 117/135 (86.7%) | 53/103 (51.5%) | 36/53 (67.9%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 21/132 (15.9%) | 117/132 (88.6%) | 50/102 (49.0%) | 39/51 (76.5%) |
| hermes | glm-5.2 | neutral | 28/127 (22.0%) | 117/127 (92.1%) | 49/100 (49.0%) | 41/49 (83.7%) |
| hermes | glm-5.2 | prompt_guard_v1 | 14/125 (11.2%) | 119/125 (95.2%) | 56/98 (57.1%) | 48/56 (85.7%) |
| hermes | qwen3.7-max | neutral | 35/134 (26.1%) | 122/134 (91.0%) | 23/100 (23.0%) | 17/23 (73.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 17/135 (12.6%) | 127/135 (94.1%) | 39/100 (39.0%) | 31/39 (79.5%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
