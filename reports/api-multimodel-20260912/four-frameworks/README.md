# Four-framework API experiment

Status: **provisional_incomplete**. 3472/5760 attempts closed; 3370 valid, 102 failed, 2288 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 40/156 (25.6%) | 132/156 (84.6%) | 71/117 (60.7%) | 45/72 (62.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 28/156 (17.9%) | 131/156 (84.0%) | 72/117 (61.5%) | 49/73 (67.1%) |
| claude-code | glm-5.2 | neutral | 24/152 (15.8%) | 138/152 (90.8%) | 69/115 (60.0%) | 55/70 (78.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 17/152 (11.2%) | 139/152 (91.4%) | 68/115 (59.1%) | 55/68 (80.9%) |
| claude-code | qwen3.7-max | neutral | 47/157 (29.9%) | 149/157 (94.9%) | 46/117 (39.3%) | 30/46 (65.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 20/160 (12.5%) | 152/160 (95.0%) | 60/120 (50.0%) | 50/61 (82.0%) |
| codex | deepseek-v4-flash | neutral | 37/152 (24.3%) | 137/152 (90.1%) | 47/113 (41.6%) | 32/47 (68.1%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 24/154 (15.6%) | 139/154 (90.3%) | 42/114 (36.8%) | 29/42 (69.0%) |
| codex | glm-5.2 | neutral | 32/140 (22.9%) | 129/140 (92.1%) | 39/103 (37.9%) | 30/39 (76.9%) |
| codex | glm-5.2 | prompt_guard_v1 | 17/141 (12.1%) | 132/141 (93.6%) | 46/103 (44.7%) | 43/46 (93.5%) |
| codex | qwen3.7-max | neutral | 53/155 (34.2%) | 146/155 (94.2%) | 32/116 (27.6%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 22/154 (14.3%) | 144/154 (93.5%) | 48/117 (41.0%) | 38/48 (79.2%) |
| deepseek-harness | deepseek-v4-flash | neutral | 44/154 (28.6%) | 136/154 (88.3%) | 65/118 (55.1%) | 47/65 (72.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 24/154 (15.6%) | 136/154 (88.3%) | 68/117 (58.1%) | 50/69 (72.5%) |
| deepseek-harness | glm-5.2 | neutral | 25/136 (18.4%) | 127/136 (93.4%) | 47/97 (48.5%) | 39/47 (83.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 13/129 (10.1%) | 121/129 (93.8%) | 53/93 (57.0%) | 45/53 (84.9%) |
| deepseek-harness | qwen3.7-max | neutral | 46/159 (28.9%) | 151/159 (95.0%) | 32/119 (26.9%) | 23/32 (71.9%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 16/158 (10.1%) | 149/158 (94.3%) | 42/118 (35.6%) | 37/42 (88.1%) |
| hermes | deepseek-v4-flash | neutral | 35/111 (31.5%) | 98/111 (88.3%) | 42/83 (50.6%) | 30/42 (71.4%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 17/108 (15.7%) | 96/108 (88.9%) | 41/83 (49.4%) | 32/42 (76.2%) |
| hermes | glm-5.2 | neutral | 23/100 (23.0%) | 91/100 (91.0%) | 38/77 (49.4%) | 31/38 (81.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/104 (11.5%) | 99/104 (95.2%) | 46/81 (56.8%) | 39/46 (84.8%) |
| hermes | qwen3.7-max | neutral | 31/114 (27.2%) | 104/114 (91.2%) | 21/87 (24.1%) | 16/21 (76.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 14/114 (12.3%) | 107/114 (93.9%) | 35/86 (40.7%) | 28/35 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
