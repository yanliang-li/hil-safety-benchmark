# Four-framework API experiment

Status: **provisional_incomplete**. 2040/5760 attempts closed; 1967 valid, 73 failed, 3720 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 26/90 (28.9%) | 76/90 (84.4%) | 43/67 (64.2%) | 25/43 (58.1%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 17/91 (18.7%) | 75/91 (82.4%) | 45/68 (66.2%) | 27/45 (60.0%) |
| claude-code | glm-5.2 | neutral | 14/88 (15.9%) | 81/88 (92.0%) | 39/67 (58.2%) | 32/39 (82.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 9/88 (10.2%) | 80/88 (90.9%) | 40/67 (59.7%) | 33/40 (82.5%) |
| claude-code | qwen3.7-max | neutral | 25/96 (26.0%) | 91/96 (94.8%) | 27/71 (38.0%) | 19/27 (70.4%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 10/97 (10.3%) | 93/97 (95.9%) | 32/71 (45.1%) | 28/33 (84.8%) |
| codex | deepseek-v4-flash | neutral | 25/93 (26.9%) | 83/93 (89.2%) | 29/69 (42.0%) | 21/29 (72.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 16/97 (16.5%) | 87/97 (89.7%) | 27/71 (38.0%) | 19/27 (70.4%) |
| codex | glm-5.2 | neutral | 22/79 (27.8%) | 71/79 (89.9%) | 20/57 (35.1%) | 15/20 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 11/80 (13.8%) | 75/80 (93.8%) | 25/58 (43.1%) | 23/25 (92.0%) |
| codex | qwen3.7-max | neutral | 34/93 (36.6%) | 88/93 (94.6%) | 19/71 (26.8%) | 12/19 (63.2%) |
| codex | qwen3.7-max | prompt_guard_v1 | 15/91 (16.5%) | 84/91 (92.3%) | 29/70 (41.4%) | 21/29 (72.4%) |
| deepseek-harness | deepseek-v4-flash | neutral | 25/94 (26.6%) | 83/94 (88.3%) | 39/73 (53.4%) | 27/39 (69.2%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 14/92 (15.2%) | 83/92 (90.2%) | 43/71 (60.6%) | 30/43 (69.8%) |
| deepseek-harness | glm-5.2 | neutral | 13/81 (16.0%) | 77/81 (95.1%) | 27/57 (47.4%) | 23/27 (85.2%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/79 (8.9%) | 74/79 (93.7%) | 31/56 (55.4%) | 27/31 (87.1%) |
| deepseek-harness | qwen3.7-max | neutral | 29/99 (29.3%) | 95/99 (96.0%) | 19/76 (25.0%) | 14/19 (73.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 12/103 (11.7%) | 98/103 (95.1%) | 26/78 (33.3%) | 23/26 (88.5%) |
| hermes | deepseek-v4-flash | neutral | 17/60 (28.3%) | 51/60 (85.0%) | 23/45 (51.1%) | 18/23 (78.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 10/56 (17.9%) | 49/56 (87.5%) | 19/41 (46.3%) | 14/20 (70.0%) |
| hermes | glm-5.2 | neutral | 13/50 (26.0%) | 44/50 (88.0%) | 16/41 (39.0%) | 11/16 (68.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 6/51 (11.8%) | 49/51 (96.1%) | 21/41 (51.2%) | 17/21 (81.0%) |
| hermes | qwen3.7-max | neutral | 14/59 (23.7%) | 54/59 (91.5%) | 10/46 (21.7%) | 8/10 (80.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/60 (10.0%) | 56/60 (93.3%) | 17/46 (37.0%) | 14/17 (82.4%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
