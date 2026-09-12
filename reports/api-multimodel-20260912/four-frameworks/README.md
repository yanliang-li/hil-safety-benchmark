# Four-framework API experiment

Status: **provisional_incomplete**. 2595/5760 attempts closed; 2510 valid, 85 failed, 3165 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 32/122 (26.2%) | 104/122 (85.2%) | 59/91 (64.8%) | 36/59 (61.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 22/122 (18.0%) | 103/122 (84.4%) | 59/91 (64.8%) | 40/59 (67.8%) |
| claude-code | glm-5.2 | neutral | 19/122 (15.6%) | 110/122 (90.2%) | 56/93 (60.2%) | 43/56 (76.8%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 12/121 (9.9%) | 109/121 (90.1%) | 55/93 (59.1%) | 43/55 (78.2%) |
| claude-code | qwen3.7-max | neutral | 33/120 (27.5%) | 115/120 (95.8%) | 35/88 (39.8%) | 24/35 (68.6%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 14/122 (11.5%) | 118/122 (96.7%) | 45/90 (50.0%) | 39/46 (84.8%) |
| codex | deepseek-v4-flash | neutral | 29/113 (25.7%) | 101/113 (89.4%) | 37/86 (43.0%) | 26/37 (70.3%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 17/114 (14.9%) | 102/114 (89.5%) | 32/86 (37.2%) | 22/32 (68.8%) |
| codex | glm-5.2 | neutral | 24/97 (24.7%) | 88/97 (90.7%) | 28/73 (38.4%) | 22/28 (78.6%) |
| codex | glm-5.2 | prompt_guard_v1 | 11/101 (10.9%) | 94/101 (93.1%) | 36/77 (46.8%) | 34/36 (94.4%) |
| codex | qwen3.7-max | neutral | 40/118 (33.9%) | 112/118 (94.9%) | 23/90 (25.6%) | 16/23 (69.6%) |
| codex | qwen3.7-max | prompt_guard_v1 | 18/116 (15.5%) | 109/116 (94.0%) | 36/89 (40.4%) | 28/36 (77.8%) |
| deepseek-harness | deepseek-v4-flash | neutral | 32/117 (27.4%) | 103/117 (88.0%) | 45/88 (51.1%) | 32/45 (71.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 20/116 (17.2%) | 103/116 (88.8%) | 50/87 (57.5%) | 34/50 (68.0%) |
| deepseek-harness | glm-5.2 | neutral | 18/95 (18.9%) | 89/95 (93.7%) | 31/70 (44.3%) | 26/31 (83.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 9/94 (9.6%) | 87/94 (92.6%) | 39/70 (55.7%) | 33/39 (84.6%) |
| deepseek-harness | qwen3.7-max | neutral | 36/120 (30.0%) | 114/120 (95.0%) | 23/92 (25.0%) | 16/23 (69.6%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 13/121 (10.7%) | 114/121 (94.2%) | 32/93 (34.4%) | 28/32 (87.5%) |
| hermes | deepseek-v4-flash | neutral | 23/77 (29.9%) | 67/77 (87.0%) | 31/58 (53.4%) | 23/31 (74.2%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 12/75 (16.0%) | 66/75 (88.0%) | 27/57 (47.4%) | 21/28 (75.0%) |
| hermes | glm-5.2 | neutral | 17/75 (22.7%) | 67/75 (89.3%) | 26/57 (45.6%) | 20/26 (76.9%) |
| hermes | glm-5.2 | prompt_guard_v1 | 10/78 (12.8%) | 74/78 (94.9%) | 32/59 (54.2%) | 26/32 (81.2%) |
| hermes | qwen3.7-max | neutral | 17/76 (22.4%) | 69/76 (90.8%) | 14/58 (24.1%) | 11/14 (78.6%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 10/78 (12.8%) | 73/78 (93.6%) | 20/58 (34.5%) | 16/20 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
