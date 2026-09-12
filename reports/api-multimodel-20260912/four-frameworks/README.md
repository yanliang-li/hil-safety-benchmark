# Four-framework API experiment

Status: **provisional_incomplete**. 1551/5760 attempts closed; 1494 valid, 57 failed, 4209 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 18/71 (25.4%) | 60/71 (84.5%) | 34/55 (61.8%) | 23/34 (67.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 14/71 (19.7%) | 59/71 (83.1%) | 37/55 (67.3%) | 23/37 (62.2%) |
| claude-code | glm-5.2 | neutral | 12/75 (16.0%) | 68/75 (90.7%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 7/75 (9.3%) | 67/75 (89.3%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | qwen3.7-max | neutral | 23/77 (29.9%) | 73/77 (94.8%) | 22/58 (37.9%) | 16/22 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 9/77 (11.7%) | 74/77 (96.1%) | 28/58 (48.3%) | 24/28 (85.7%) |
| codex | deepseek-v4-flash | neutral | 18/67 (26.9%) | 58/67 (86.6%) | 18/50 (36.0%) | 14/18 (77.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 11/70 (15.7%) | 61/70 (87.1%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | neutral | 17/64 (26.6%) | 58/64 (90.6%) | 18/47 (38.3%) | 13/18 (72.2%) |
| codex | glm-5.2 | prompt_guard_v1 | 8/63 (12.7%) | 60/63 (95.2%) | 22/47 (46.8%) | 20/22 (90.9%) |
| codex | qwen3.7-max | neutral | 24/72 (33.3%) | 68/72 (94.4%) | 15/54 (27.8%) | 11/15 (73.3%) |
| codex | qwen3.7-max | prompt_guard_v1 | 11/72 (15.3%) | 67/72 (93.1%) | 20/54 (37.0%) | 16/20 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 20/73 (27.4%) | 64/73 (87.7%) | 29/53 (54.7%) | 20/29 (69.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/72 (16.7%) | 66/72 (91.7%) | 31/52 (59.6%) | 23/31 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 11/63 (17.5%) | 60/63 (95.2%) | 22/45 (48.9%) | 19/22 (86.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/62 (11.3%) | 58/62 (93.5%) | 23/43 (53.5%) | 20/23 (87.0%) |
| deepseek-harness | qwen3.7-max | neutral | 22/71 (31.0%) | 67/71 (94.4%) | 11/53 (20.8%) | 8/11 (72.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 8/71 (11.3%) | 66/71 (93.0%) | 20/53 (37.7%) | 18/20 (90.0%) |
| hermes | deepseek-v4-flash | neutral | 14/41 (34.1%) | 37/41 (90.2%) | 15/29 (51.7%) | 11/15 (73.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 9/40 (22.5%) | 37/40 (92.5%) | 12/28 (42.9%) | 10/12 (83.3%) |
| hermes | glm-5.2 | neutral | 8/35 (22.9%) | 29/35 (82.9%) | 12/27 (44.4%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 4/37 (10.8%) | 35/37 (94.6%) | 15/28 (53.6%) | 11/15 (73.3%) |
| hermes | qwen3.7-max | neutral | 12/37 (32.4%) | 34/37 (91.9%) | 5/30 (16.7%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/38 (15.8%) | 36/38 (94.7%) | 10/30 (33.3%) | 8/10 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
