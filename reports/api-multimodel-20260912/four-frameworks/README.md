# Four-framework API experiment

Status: **provisional_incomplete**. 2972/5760 attempts closed; 2880 valid, 92 failed, 2788 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 36/135 (26.7%) | 115/135 (85.2%) | 64/102 (62.7%) | 41/64 (64.1%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 24/135 (17.8%) | 114/135 (84.4%) | 64/102 (62.7%) | 45/64 (70.3%) |
| claude-code | glm-5.2 | neutral | 22/137 (16.1%) | 124/137 (90.5%) | 62/104 (59.6%) | 48/62 (77.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 15/136 (11.0%) | 124/136 (91.2%) | 60/103 (58.3%) | 48/60 (80.0%) |
| claude-code | qwen3.7-max | neutral | 38/134 (28.4%) | 128/134 (95.5%) | 39/97 (40.2%) | 25/39 (64.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 17/134 (12.7%) | 129/134 (96.3%) | 49/97 (50.5%) | 41/50 (82.0%) |
| codex | deepseek-v4-flash | neutral | 34/132 (25.8%) | 118/132 (89.4%) | 41/101 (40.6%) | 29/41 (70.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 19/134 (14.2%) | 119/134 (88.8%) | 38/102 (37.3%) | 26/38 (68.4%) |
| codex | glm-5.2 | neutral | 29/122 (23.8%) | 111/122 (91.0%) | 35/91 (38.5%) | 28/35 (80.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 14/123 (11.4%) | 114/123 (92.7%) | 43/91 (47.3%) | 41/43 (95.3%) |
| codex | qwen3.7-max | neutral | 45/137 (32.8%) | 131/137 (95.6%) | 28/102 (27.5%) | 20/28 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 20/133 (15.0%) | 125/133 (94.0%) | 39/100 (39.0%) | 30/39 (76.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 35/129 (27.1%) | 113/129 (87.6%) | 51/97 (52.6%) | 36/51 (70.6%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 21/128 (16.4%) | 113/128 (88.3%) | 57/96 (59.4%) | 40/58 (69.0%) |
| deepseek-harness | glm-5.2 | neutral | 20/107 (18.7%) | 99/107 (92.5%) | 36/79 (45.6%) | 28/36 (77.8%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 11/105 (10.5%) | 98/105 (93.3%) | 43/78 (55.1%) | 36/43 (83.7%) |
| deepseek-harness | qwen3.7-max | neutral | 39/136 (28.7%) | 129/136 (94.9%) | 28/106 (26.4%) | 20/28 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 15/137 (10.9%) | 129/137 (94.2%) | 36/106 (34.0%) | 31/36 (86.1%) |
| hermes | deepseek-v4-flash | neutral | 30/96 (31.2%) | 84/96 (87.5%) | 37/70 (52.9%) | 26/37 (70.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 15/91 (16.5%) | 81/91 (89.0%) | 32/67 (47.8%) | 24/33 (72.7%) |
| hermes | glm-5.2 | neutral | 21/86 (24.4%) | 78/86 (90.7%) | 31/65 (47.7%) | 25/31 (80.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/88 (13.6%) | 84/88 (95.5%) | 36/66 (54.5%) | 30/36 (83.3%) |
| hermes | qwen3.7-max | neutral | 22/92 (23.9%) | 83/92 (90.2%) | 18/71 (25.4%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 11/93 (11.8%) | 86/93 (92.5%) | 28/71 (39.4%) | 21/28 (75.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
