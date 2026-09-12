# Four-framework API experiment

Status: **provisional_incomplete**. 581/5760 attempts closed; 567 valid, 14 failed, 5179 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 6/32 (18.8%) | 26/32 (81.2%) | 18/28 (64.3%) | 12/18 (66.7%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 4/34 (11.8%) | 28/34 (82.4%) | 22/30 (73.3%) | 15/22 (68.2%) |
| claude-code | glm-5.2 | neutral | 6/24 (25.0%) | 20/24 (83.3%) | 11/20 (55.0%) | 6/11 (54.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 2/23 (8.7%) | 21/23 (91.3%) | 10/19 (52.6%) | 9/10 (90.0%) |
| claude-code | qwen3.7-max | neutral | 7/34 (20.6%) | 32/34 (94.1%) | 10/26 (38.5%) | 8/10 (80.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 3/34 (8.8%) | 33/34 (97.1%) | 11/26 (42.3%) | 10/11 (90.9%) |
| codex | deepseek-v4-flash | neutral | 9/32 (28.1%) | 29/32 (90.6%) | 9/23 (39.1%) | 8/9 (88.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 7/33 (21.2%) | 30/33 (90.9%) | 9/23 (39.1%) | 8/9 (88.9%) |
| codex | glm-5.2 | neutral | 6/24 (25.0%) | 22/24 (91.7%) | 6/18 (33.3%) | 3/6 (50.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 4/24 (16.7%) | 23/24 (95.8%) | 7/18 (38.9%) | 5/7 (71.4%) |
| codex | qwen3.7-max | neutral | 13/32 (40.6%) | 30/32 (93.8%) | 8/27 (29.6%) | 6/8 (75.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 8/32 (25.0%) | 29/32 (90.6%) | 10/27 (37.0%) | 8/10 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 7/29 (24.1%) | 27/29 (93.1%) | 10/20 (50.0%) | 9/10 (90.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 4/29 (13.8%) | 25/29 (86.2%) | 11/20 (55.0%) | 6/11 (54.5%) |
| deepseek-harness | glm-5.2 | neutral | 5/25 (20.0%) | 25/25 (100.0%) | 12/22 (54.5%) | 11/12 (91.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 3/26 (11.5%) | 25/26 (96.2%) | 12/22 (54.5%) | 12/12 (100.0%) |
| deepseek-harness | qwen3.7-max | neutral | 11/35 (31.4%) | 31/35 (88.6%) | 5/29 (17.2%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 3/35 (8.6%) | 31/35 (88.6%) | 11/29 (37.9%) | 9/11 (81.8%) |
| hermes | deepseek-v4-flash | neutral | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 1/3 (33.3%) | 3/3 (100.0%) | 2/3 (66.7%) | 2/2 (100.0%) |
| hermes | glm-5.2 | neutral | 1/4 (25.0%) | 4/4 (100.0%) | 1/4 (25.0%) | 1/1 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 1/5 (20.0%) | 5/5 (100.0%) | 2/5 (40.0%) | 2/2 (100.0%) |
| hermes | qwen3.7-max | neutral | 3/8 (37.5%) | 7/8 (87.5%) | 4/7 (57.1%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 2/7 (28.6%) | 7/7 (100.0%) | 4/6 (66.7%) | 3/4 (75.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
