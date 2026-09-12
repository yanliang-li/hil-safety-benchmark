# Four-framework API experiment

Status: **provisional_incomplete**. 1028/5760 attempts closed; 994 valid, 34 failed, 4732 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 7/47 (14.9%) | 38/47 (80.9%) | 29/41 (70.7%) | 20/29 (69.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 4/47 (8.5%) | 39/47 (83.0%) | 32/41 (78.0%) | 22/32 (68.8%) |
| claude-code | glm-5.2 | neutral | 8/48 (16.7%) | 41/48 (85.4%) | 21/37 (56.8%) | 14/21 (66.7%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 4/49 (8.2%) | 42/49 (85.7%) | 23/38 (60.5%) | 17/23 (73.9%) |
| claude-code | qwen3.7-max | neutral | 14/54 (25.9%) | 52/54 (96.3%) | 15/42 (35.7%) | 11/15 (73.3%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 5/53 (9.4%) | 52/53 (98.1%) | 17/41 (41.5%) | 16/17 (94.1%) |
| codex | deepseek-v4-flash | neutral | 15/49 (30.6%) | 43/49 (87.8%) | 13/35 (37.1%) | 10/13 (76.9%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 10/50 (20.0%) | 44/50 (88.0%) | 13/36 (36.1%) | 10/13 (76.9%) |
| codex | glm-5.2 | neutral | 10/42 (23.8%) | 37/42 (88.1%) | 10/31 (32.3%) | 6/10 (60.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 5/41 (12.2%) | 39/41 (95.1%) | 10/30 (33.3%) | 8/10 (80.0%) |
| codex | qwen3.7-max | neutral | 17/50 (34.0%) | 48/50 (96.0%) | 12/37 (32.4%) | 10/12 (83.3%) |
| codex | qwen3.7-max | prompt_guard_v1 | 9/51 (17.6%) | 48/51 (94.1%) | 15/38 (39.5%) | 12/15 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 14/52 (26.9%) | 46/52 (88.5%) | 19/37 (51.4%) | 15/19 (78.9%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 9/52 (17.3%) | 47/52 (90.4%) | 21/36 (58.3%) | 15/21 (71.4%) |
| deepseek-harness | glm-5.2 | neutral | 7/44 (15.9%) | 44/44 (100.0%) | 18/32 (56.2%) | 15/18 (83.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 5/45 (11.1%) | 44/45 (97.8%) | 18/32 (56.2%) | 16/18 (88.9%) |
| deepseek-harness | qwen3.7-max | neutral | 17/53 (32.1%) | 49/53 (92.5%) | 8/40 (20.0%) | 6/8 (75.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 6/51 (11.8%) | 47/51 (92.2%) | 15/38 (39.5%) | 13/15 (86.7%) |
| hermes | deepseek-v4-flash | neutral | 5/20 (25.0%) | 17/20 (85.0%) | 8/15 (53.3%) | 6/8 (75.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 2/19 (10.5%) | 17/19 (89.5%) | 6/14 (42.9%) | 5/6 (83.3%) |
| hermes | glm-5.2 | neutral | 4/17 (23.5%) | 15/17 (88.2%) | 4/13 (30.8%) | 4/4 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 3/17 (17.6%) | 16/17 (94.1%) | 5/13 (38.5%) | 5/5 (100.0%) |
| hermes | qwen3.7-max | neutral | 8/21 (38.1%) | 19/21 (90.5%) | 5/18 (27.8%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 4/22 (18.2%) | 21/22 (95.5%) | 8/18 (44.4%) | 7/8 (87.5%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
