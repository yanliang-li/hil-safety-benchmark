# Four-framework API experiment

Status: **provisional_incomplete**. 1524/5760 attempts closed; 1471 valid, 53 failed, 4236 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 18/71 (25.4%) | 60/71 (84.5%) | 34/55 (61.8%) | 23/34 (67.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 14/70 (20.0%) | 58/70 (82.9%) | 37/55 (67.3%) | 23/37 (62.2%) |
| claude-code | glm-5.2 | neutral | 12/75 (16.0%) | 68/75 (90.7%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 7/75 (9.3%) | 67/75 (89.3%) | 34/57 (59.6%) | 27/34 (79.4%) |
| claude-code | qwen3.7-max | neutral | 23/77 (29.9%) | 73/77 (94.8%) | 22/58 (37.9%) | 16/22 (72.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 9/76 (11.8%) | 73/76 (96.1%) | 28/58 (48.3%) | 24/28 (85.7%) |
| codex | deepseek-v4-flash | neutral | 18/67 (26.9%) | 58/67 (86.6%) | 18/50 (36.0%) | 14/18 (77.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 11/70 (15.7%) | 61/70 (87.1%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | neutral | 15/59 (25.4%) | 54/59 (91.5%) | 16/44 (36.4%) | 12/16 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 8/60 (13.3%) | 58/60 (96.7%) | 20/44 (45.5%) | 18/20 (90.0%) |
| codex | qwen3.7-max | neutral | 24/71 (33.8%) | 67/71 (94.4%) | 14/53 (26.4%) | 10/14 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 11/72 (15.3%) | 67/72 (93.1%) | 20/54 (37.0%) | 16/20 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 20/73 (27.4%) | 64/73 (87.7%) | 29/53 (54.7%) | 20/29 (69.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/72 (16.7%) | 66/72 (91.7%) | 31/52 (59.6%) | 23/31 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 11/63 (17.5%) | 60/63 (95.2%) | 22/45 (48.9%) | 19/22 (86.4%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/58 (12.1%) | 55/58 (94.8%) | 22/41 (53.7%) | 19/22 (86.4%) |
| deepseek-harness | qwen3.7-max | neutral | 22/71 (31.0%) | 67/71 (94.4%) | 11/53 (20.8%) | 8/11 (72.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 8/71 (11.3%) | 66/71 (93.0%) | 20/53 (37.7%) | 18/20 (90.0%) |
| hermes | deepseek-v4-flash | neutral | 14/41 (34.1%) | 37/41 (90.2%) | 15/29 (51.7%) | 11/15 (73.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 8/38 (21.1%) | 35/38 (92.1%) | 11/26 (42.3%) | 9/11 (81.8%) |
| hermes | glm-5.2 | neutral | 7/32 (21.9%) | 26/32 (81.2%) | 12/27 (44.4%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 4/34 (11.8%) | 32/34 (94.1%) | 15/28 (53.6%) | 11/15 (73.3%) |
| hermes | qwen3.7-max | neutral | 12/37 (32.4%) | 34/37 (91.9%) | 5/30 (16.7%) | 3/5 (60.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/38 (15.8%) | 36/38 (94.7%) | 10/30 (33.3%) | 8/10 (80.0%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
