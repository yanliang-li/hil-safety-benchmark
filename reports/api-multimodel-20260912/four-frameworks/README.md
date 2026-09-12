# Four-framework API experiment

Status: **provisional_incomplete**. 1710/5760 attempts closed; 1648 valid, 62 failed, 4050 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 22/83 (26.5%) | 70/83 (84.3%) | 39/62 (62.9%) | 25/39 (64.1%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 16/82 (19.5%) | 69/82 (84.1%) | 39/61 (63.9%) | 25/39 (64.1%) |
| claude-code | glm-5.2 | neutral | 14/80 (17.5%) | 73/80 (91.2%) | 34/60 (56.7%) | 27/34 (79.4%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 9/80 (11.2%) | 72/80 (90.0%) | 35/60 (58.3%) | 28/35 (80.0%) |
| claude-code | qwen3.7-max | neutral | 23/81 (28.4%) | 77/81 (95.1%) | 23/61 (37.7%) | 16/23 (69.6%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 10/83 (12.0%) | 80/83 (96.4%) | 28/63 (44.4%) | 25/29 (86.2%) |
| codex | deepseek-v4-flash | neutral | 21/76 (27.6%) | 67/76 (88.2%) | 22/56 (39.3%) | 16/22 (72.7%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 13/77 (16.9%) | 68/77 (88.3%) | 22/58 (37.9%) | 16/22 (72.7%) |
| codex | glm-5.2 | neutral | 18/72 (25.0%) | 64/72 (88.9%) | 20/53 (37.7%) | 15/20 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 9/71 (12.7%) | 66/71 (93.0%) | 22/52 (42.3%) | 20/22 (90.9%) |
| codex | qwen3.7-max | neutral | 28/79 (35.4%) | 75/79 (94.9%) | 17/59 (28.8%) | 11/17 (64.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 13/78 (16.7%) | 73/78 (93.6%) | 22/58 (37.9%) | 17/22 (77.3%) |
| deepseek-harness | deepseek-v4-flash | neutral | 20/77 (26.0%) | 67/77 (87.0%) | 32/57 (56.1%) | 23/32 (71.9%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/78 (15.4%) | 70/78 (89.7%) | 36/58 (62.1%) | 26/36 (72.2%) |
| deepseek-harness | glm-5.2 | neutral | 12/67 (17.9%) | 64/67 (95.5%) | 24/47 (51.1%) | 20/24 (83.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/65 (10.8%) | 61/65 (93.8%) | 25/45 (55.6%) | 22/25 (88.0%) |
| deepseek-harness | qwen3.7-max | neutral | 23/81 (28.4%) | 77/81 (95.1%) | 16/61 (26.2%) | 12/16 (75.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 8/81 (9.9%) | 76/81 (93.8%) | 24/61 (39.3%) | 22/24 (91.7%) |
| hermes | deepseek-v4-flash | neutral | 16/47 (34.0%) | 40/47 (85.1%) | 17/34 (50.0%) | 12/17 (70.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 9/45 (20.0%) | 40/45 (88.9%) | 15/32 (46.9%) | 10/15 (66.7%) |
| hermes | glm-5.2 | neutral | 8/39 (20.5%) | 33/39 (84.6%) | 12/30 (40.0%) | 7/12 (58.3%) |
| hermes | glm-5.2 | prompt_guard_v1 | 4/41 (9.8%) | 39/41 (95.1%) | 16/31 (51.6%) | 12/16 (75.0%) |
| hermes | qwen3.7-max | neutral | 12/42 (28.6%) | 39/42 (92.9%) | 6/34 (17.6%) | 4/6 (66.7%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/43 (14.0%) | 41/43 (95.3%) | 12/34 (35.3%) | 10/12 (83.3%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
