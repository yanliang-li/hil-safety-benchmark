# Four-framework API experiment

Status: **provisional_incomplete**. 1604/5760 attempts closed; 1545 valid, 59 failed, 4156 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 18/75 (24.0%) | 64/75 (85.3%) | 35/56 (62.5%) | 24/35 (68.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 14/76 (18.4%) | 64/76 (84.2%) | 38/56 (67.9%) | 24/38 (63.2%) |
| claude-code | glm-5.2 | neutral | 13/78 (16.7%) | 71/78 (91.0%) | 34/59 (57.6%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 8/79 (10.1%) | 71/79 (89.9%) | 35/59 (59.3%) | 28/35 (80.0%) |
| claude-code | qwen3.7-max | neutral | 23/78 (29.5%) | 74/78 (94.9%) | 22/59 (37.3%) | 16/22 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 9/79 (11.4%) | 76/79 (96.2%) | 28/60 (46.7%) | 24/28 (85.7%) |
| codex | deepseek-v4-flash | neutral | 19/71 (26.8%) | 62/71 (87.3%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 11/71 (15.5%) | 62/71 (87.3%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | neutral | 17/65 (26.2%) | 58/65 (89.2%) | 18/48 (37.5%) | 13/18 (72.2%) |
| codex | glm-5.2 | prompt_guard_v1 | 9/67 (13.4%) | 63/67 (94.0%) | 22/49 (44.9%) | 20/22 (90.9%) |
| codex | qwen3.7-max | neutral | 25/75 (33.3%) | 71/75 (94.7%) | 15/56 (26.8%) | 11/15 (73.3%) |
| codex | qwen3.7-max | prompt_guard_v1 | 12/74 (16.2%) | 69/74 (93.2%) | 20/56 (35.7%) | 16/20 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 20/74 (27.0%) | 65/74 (87.8%) | 30/54 (55.6%) | 21/30 (70.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/72 (16.7%) | 66/72 (91.7%) | 31/52 (59.6%) | 23/31 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 11/63 (17.5%) | 60/63 (95.2%) | 22/45 (48.9%) | 19/22 (86.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/63 (11.1%) | 59/63 (93.7%) | 23/43 (53.5%) | 20/23 (87.0%) |
| deepseek-harness | qwen3.7-max | neutral | 23/74 (31.1%) | 70/74 (94.6%) | 14/56 (25.0%) | 10/14 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 8/76 (10.5%) | 71/76 (93.4%) | 23/58 (39.7%) | 21/23 (91.3%) |
| hermes | deepseek-v4-flash | neutral | 14/41 (34.1%) | 37/41 (90.2%) | 15/29 (51.7%) | 11/15 (73.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 9/41 (22.0%) | 38/41 (92.7%) | 12/29 (41.4%) | 10/12 (83.3%) |
| hermes | glm-5.2 | neutral | 8/36 (22.2%) | 30/36 (83.3%) | 12/28 (42.9%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 4/39 (10.3%) | 37/39 (94.9%) | 16/30 (53.3%) | 12/16 (75.0%) |
| hermes | qwen3.7-max | neutral | 12/39 (30.8%) | 36/39 (92.3%) | 5/31 (16.1%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/39 (15.4%) | 37/39 (94.9%) | 10/31 (32.3%) | 8/10 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
