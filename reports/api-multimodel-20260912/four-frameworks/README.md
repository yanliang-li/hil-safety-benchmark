# Four-framework API experiment

Status: **provisional_incomplete**. 628/5760 attempts closed; 614 valid, 14 failed, 5132 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 6/36 (16.7%) | 29/36 (80.6%) | 20/32 (62.5%) | 14/20 (70.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 4/36 (11.1%) | 29/36 (80.6%) | 24/32 (75.0%) | 16/24 (66.7%) |
| claude-code | glm-5.2 | neutral | 6/27 (22.2%) | 21/27 (77.8%) | 11/22 (50.0%) | 6/11 (54.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 3/27 (11.1%) | 23/27 (85.2%) | 12/22 (54.5%) | 9/12 (75.0%) |
| claude-code | qwen3.7-max | neutral | 9/36 (25.0%) | 34/36 (94.4%) | 11/28 (39.3%) | 8/11 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 3/35 (8.6%) | 34/35 (97.1%) | 11/27 (40.7%) | 10/11 (90.9%) |
| codex | deepseek-v4-flash | neutral | 10/34 (29.4%) | 30/34 (88.2%) | 9/24 (37.5%) | 8/9 (88.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 7/34 (20.6%) | 30/34 (88.2%) | 9/24 (37.5%) | 8/9 (88.9%) |
| codex | glm-5.2 | neutral | 6/27 (22.2%) | 24/27 (88.9%) | 7/20 (35.0%) | 4/7 (57.1%) |
| codex | glm-5.2 | prompt_guard_v1 | 4/25 (16.0%) | 24/25 (96.0%) | 7/19 (36.8%) | 5/7 (71.4%) |
| codex | qwen3.7-max | neutral | 13/33 (39.4%) | 31/33 (93.9%) | 8/27 (29.6%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 8/33 (24.2%) | 30/33 (90.9%) | 10/27 (37.0%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 7/32 (21.9%) | 29/32 (90.6%) | 12/22 (54.5%) | 10/12 (83.3%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 5/31 (16.1%) | 27/31 (87.1%) | 12/21 (57.1%) | 7/12 (58.3%) |
| deepseek-harness | glm-5.2 | neutral | 6/28 (21.4%) | 28/28 (100.0%) | 13/23 (56.5%) | 12/13 (92.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 4/29 (13.8%) | 28/29 (96.6%) | 13/23 (56.5%) | 13/13 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 11/37 (29.7%) | 33/37 (89.2%) | 5/29 (17.2%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 3/37 (8.1%) | 33/37 (89.2%) | 11/29 (37.9%) | 9/11 (81.8%) |
| hermes | deepseek-v4-flash | neutral | 2/4 (50.0%) | 4/4 (100.0%) | 2/4 (50.0%) | 2/2 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | glm-5.2 | neutral | 1/6 (16.7%) | 6/6 (100.0%) | 2/5 (40.0%) | 2/2 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 1/7 (14.3%) | 7/7 (100.0%) | 3/6 (50.0%) | 3/3 (100.0%) |
| hermes | qwen3.7-max | neutral | 3/9 (33.3%) | 7/9 (77.8%) | 4/8 (50.0%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 2/8 (25.0%) | 8/8 (100.0%) | 5/7 (71.4%) | 4/5 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
