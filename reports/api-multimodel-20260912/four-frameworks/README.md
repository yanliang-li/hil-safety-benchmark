# Four-framework API experiment

Status: **provisional_incomplete**. 459/5760 attempts closed; 446 valid, 13 failed, 5301 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 3/21 (14.3%) | 16/21 (76.2%) | 11/17 (64.7%) | 6/11 (54.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 2/21 (9.5%) | 16/21 (76.2%) | 13/17 (76.5%) | 7/13 (53.8%) |
| claude-code | glm-5.2 | neutral | 4/20 (20.0%) | 16/20 (80.0%) | 9/16 (56.2%) | 5/9 (55.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 2/20 (10.0%) | 18/20 (90.0%) | 9/16 (56.2%) | 8/9 (88.9%) |
| claude-code | qwen3.7-max | neutral | 5/30 (16.7%) | 28/30 (93.3%) | 8/23 (34.8%) | 7/8 (87.5%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 2/29 (6.9%) | 28/29 (96.6%) | 8/22 (36.4%) | 7/8 (87.5%) |
| codex | deepseek-v4-flash | neutral | 7/25 (28.0%) | 22/25 (88.0%) | 7/19 (36.8%) | 6/7 (85.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 4/25 (16.0%) | 22/25 (88.0%) | 8/19 (42.1%) | 7/8 (87.5%) |
| codex | glm-5.2 | neutral | 6/20 (30.0%) | 18/20 (90.0%) | 4/15 (26.7%) | 3/4 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 4/20 (20.0%) | 19/20 (95.0%) | 6/15 (40.0%) | 5/6 (83.3%) |
| codex | qwen3.7-max | neutral | 11/27 (40.7%) | 25/27 (92.6%) | 8/22 (36.4%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 7/28 (25.0%) | 25/28 (89.3%) | 10/23 (43.5%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 6/19 (31.6%) | 18/19 (94.7%) | 5/12 (41.7%) | 4/5 (80.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 2/19 (10.5%) | 16/19 (84.2%) | 6/12 (50.0%) | 3/6 (50.0%) |
| deepseek-harness | glm-5.2 | neutral | 5/23 (21.7%) | 23/23 (100.0%) | 11/20 (55.0%) | 10/11 (90.9%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 3/23 (13.0%) | 22/23 (95.7%) | 10/19 (52.6%) | 10/10 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 10/31 (32.3%) | 27/31 (87.1%) | 5/25 (20.0%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 3/31 (9.7%) | 27/31 (87.1%) | 10/25 (40.0%) | 8/10 (80.0%) |
| hermes | deepseek-v4-flash | neutral | 1/2 (50.0%) | 2/2 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 1/2 (50.0%) | 2/2 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | glm-5.2 | neutral | 1/2 (50.0%) | 2/2 (100.0%) | 0/2 (0.0%) | N/A |
| hermes | glm-5.2 | prompt_guard_v1 | 1/2 (50.0%) | 2/2 (100.0%) | 0/2 (0.0%) | N/A |
| hermes | qwen3.7-max | neutral | 0/3 (0.0%) | 2/3 (66.7%) | 1/2 (50.0%) | 1/1 (100.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 1/3 (33.3%) | 3/3 (100.0%) | 1/2 (50.0%) | 1/1 (100.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
