# Four-framework API experiment

Status: **provisional_incomplete**. 1399/5760 attempts closed; 1348 valid, 51 failed, 4361 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 16/67 (23.9%) | 56/67 (83.6%) | 32/53 (60.4%) | 22/32 (68.8%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 12/68 (17.6%) | 56/68 (82.4%) | 36/54 (66.7%) | 23/36 (63.9%) |
| claude-code | glm-5.2 | neutral | 11/66 (16.7%) | 59/66 (89.4%) | 29/50 (58.0%) | 22/29 (75.9%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 6/67 (9.0%) | 59/67 (88.1%) | 30/51 (58.8%) | 23/30 (76.7%) |
| claude-code | qwen3.7-max | neutral | 21/72 (29.2%) | 69/72 (95.8%) | 21/55 (38.2%) | 15/21 (71.4%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 8/72 (11.1%) | 70/72 (97.2%) | 26/55 (47.3%) | 23/26 (88.5%) |
| codex | deepseek-v4-flash | neutral | 16/62 (25.8%) | 53/62 (85.5%) | 17/46 (37.0%) | 13/17 (76.5%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 10/64 (15.6%) | 55/64 (85.9%) | 19/48 (39.6%) | 14/19 (73.7%) |
| codex | glm-5.2 | neutral | 13/53 (24.5%) | 48/53 (90.6%) | 14/41 (34.1%) | 10/14 (71.4%) |
| codex | glm-5.2 | prompt_guard_v1 | 6/51 (11.8%) | 49/51 (96.1%) | 15/39 (38.5%) | 13/15 (86.7%) |
| codex | qwen3.7-max | neutral | 23/68 (33.8%) | 64/68 (94.1%) | 14/51 (27.5%) | 10/14 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 11/67 (16.4%) | 63/67 (94.0%) | 19/50 (38.0%) | 15/19 (78.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 20/68 (29.4%) | 61/68 (89.7%) | 27/50 (54.0%) | 20/27 (74.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/67 (17.9%) | 62/67 (92.5%) | 29/49 (59.2%) | 22/29 (75.9%) |
| deepseek-harness | glm-5.2 | neutral | 10/56 (17.9%) | 54/56 (96.4%) | 21/41 (51.2%) | 18/21 (85.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 6/55 (10.9%) | 52/55 (94.5%) | 21/39 (53.8%) | 18/21 (85.7%) |
| deepseek-harness | qwen3.7-max | neutral | 22/68 (32.4%) | 64/68 (94.1%) | 10/52 (19.2%) | 7/10 (70.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 8/68 (11.8%) | 63/68 (92.6%) | 19/52 (36.5%) | 17/19 (89.5%) |
| hermes | deepseek-v4-flash | neutral | 10/34 (29.4%) | 30/34 (88.2%) | 12/24 (50.0%) | 10/12 (83.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 7/33 (21.2%) | 31/33 (93.9%) | 9/23 (39.1%) | 8/9 (88.9%) |
| hermes | glm-5.2 | neutral | 6/27 (22.2%) | 22/27 (81.5%) | 9/22 (40.9%) | 5/9 (55.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 4/29 (13.8%) | 27/29 (93.1%) | 12/23 (52.2%) | 8/12 (66.7%) |
| hermes | qwen3.7-max | neutral | 11/32 (34.4%) | 29/32 (90.6%) | 5/28 (17.9%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/34 (17.6%) | 32/34 (94.1%) | 9/28 (32.1%) | 7/9 (77.8%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
