# Four-framework API experiment

Status: **provisional_incomplete**. 3172/5760 attempts closed; 3075 valid, 97 failed, 2588 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 37/141 (26.2%) | 120/141 (85.1%) | 66/106 (62.3%) | 42/66 (63.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 25/141 (17.7%) | 119/141 (84.4%) | 66/106 (62.3%) | 47/67 (70.1%) |
| claude-code | glm-5.2 | neutral | 23/147 (15.6%) | 134/147 (91.2%) | 66/111 (59.5%) | 52/66 (78.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 16/147 (10.9%) | 134/147 (91.2%) | 66/111 (59.5%) | 53/66 (80.3%) |
| claude-code | qwen3.7-max | neutral | 42/145 (29.0%) | 138/145 (95.2%) | 43/107 (40.2%) | 28/43 (65.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 17/145 (11.7%) | 138/145 (95.2%) | 53/107 (49.5%) | 45/54 (83.3%) |
| codex | deepseek-v4-flash | neutral | 36/139 (25.9%) | 124/139 (89.2%) | 43/105 (41.0%) | 30/43 (69.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 21/139 (15.1%) | 124/139 (89.2%) | 39/105 (37.1%) | 26/39 (66.7%) |
| codex | glm-5.2 | neutral | 30/127 (23.6%) | 116/127 (91.3%) | 35/93 (37.6%) | 28/35 (80.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 15/129 (11.6%) | 120/129 (93.0%) | 43/95 (45.3%) | 41/43 (95.3%) |
| codex | qwen3.7-max | neutral | 50/145 (34.5%) | 139/145 (95.9%) | 30/108 (27.8%) | 21/30 (70.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 22/145 (15.2%) | 137/145 (94.5%) | 44/110 (40.0%) | 35/44 (79.5%) |
| deepseek-harness | deepseek-v4-flash | neutral | 37/136 (27.2%) | 119/136 (87.5%) | 57/104 (54.8%) | 40/57 (70.2%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 22/136 (16.2%) | 119/136 (87.5%) | 63/104 (60.6%) | 45/64 (70.3%) |
| deepseek-harness | glm-5.2 | neutral | 23/124 (18.5%) | 116/124 (93.5%) | 43/88 (48.9%) | 35/43 (81.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 12/118 (10.2%) | 111/118 (94.1%) | 48/84 (57.1%) | 41/48 (85.4%) |
| deepseek-harness | qwen3.7-max | neutral | 41/145 (28.3%) | 138/145 (95.2%) | 29/108 (26.9%) | 21/29 (72.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 15/143 (10.5%) | 135/143 (94.4%) | 37/107 (34.6%) | 32/37 (86.5%) |
| hermes | deepseek-v4-flash | neutral | 31/101 (30.7%) | 89/101 (88.1%) | 39/75 (52.0%) | 28/39 (71.8%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 16/97 (16.5%) | 87/97 (89.7%) | 36/73 (49.3%) | 28/37 (75.7%) |
| hermes | glm-5.2 | neutral | 22/90 (24.4%) | 82/90 (91.1%) | 33/68 (48.5%) | 27/33 (81.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/92 (13.0%) | 88/92 (95.7%) | 38/69 (55.1%) | 32/38 (84.2%) |
| hermes | qwen3.7-max | neutral | 26/101 (25.7%) | 91/101 (90.1%) | 18/77 (23.4%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 13/102 (12.7%) | 95/102 (93.1%) | 30/77 (39.0%) | 23/30 (76.7%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
