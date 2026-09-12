# Four-framework API experiment

Status: **provisional_incomplete**. 875/5760 attempts closed; 844 valid, 31 failed, 4885 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 7/44 (15.9%) | 36/44 (81.8%) | 27/39 (69.2%) | 19/27 (70.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 4/44 (9.1%) | 36/44 (81.8%) | 30/39 (76.9%) | 21/30 (70.0%) |
| claude-code | glm-5.2 | neutral | 8/43 (18.6%) | 36/43 (83.7%) | 19/34 (55.9%) | 12/19 (63.2%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 3/41 (7.3%) | 35/41 (85.4%) | 21/32 (65.6%) | 15/21 (71.4%) |
| claude-code | qwen3.7-max | neutral | 12/45 (26.7%) | 43/45 (95.6%) | 14/36 (38.9%) | 10/14 (71.4%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 3/44 (6.8%) | 43/44 (97.7%) | 15/35 (42.9%) | 14/15 (93.3%) |
| codex | deepseek-v4-flash | neutral | 15/45 (33.3%) | 40/45 (88.9%) | 12/31 (38.7%) | 9/12 (75.0%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 10/47 (21.3%) | 41/47 (87.2%) | 13/33 (39.4%) | 10/13 (76.9%) |
| codex | glm-5.2 | neutral | 9/41 (22.0%) | 36/41 (87.8%) | 10/30 (33.3%) | 6/10 (60.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 4/38 (10.5%) | 36/38 (94.7%) | 10/27 (37.0%) | 8/10 (80.0%) |
| codex | qwen3.7-max | neutral | 14/42 (33.3%) | 40/42 (95.2%) | 10/32 (31.2%) | 8/10 (80.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 8/42 (19.0%) | 39/42 (92.9%) | 12/33 (36.4%) | 10/12 (83.3%) |
| deepseek-harness | deepseek-v4-flash | neutral | 10/45 (22.2%) | 40/45 (88.9%) | 19/32 (59.4%) | 15/19 (78.9%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 6/44 (13.6%) | 39/44 (88.6%) | 20/31 (64.5%) | 14/20 (70.0%) |
| deepseek-harness | glm-5.2 | neutral | 7/36 (19.4%) | 36/36 (100.0%) | 15/28 (53.6%) | 13/15 (86.7%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 5/36 (13.9%) | 35/36 (97.2%) | 14/27 (51.9%) | 13/14 (92.9%) |
| deepseek-harness | qwen3.7-max | neutral | 14/43 (32.6%) | 39/43 (90.7%) | 5/32 (15.6%) | 3/5 (60.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 4/42 (9.5%) | 38/42 (90.5%) | 12/31 (38.7%) | 10/12 (83.3%) |
| hermes | deepseek-v4-flash | neutral | 3/13 (23.1%) | 10/13 (76.9%) | 5/10 (50.0%) | 4/5 (80.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 2/11 (18.2%) | 10/11 (90.9%) | 3/8 (37.5%) | 3/3 (100.0%) |
| hermes | glm-5.2 | neutral | 3/13 (23.1%) | 12/13 (92.3%) | 3/10 (30.0%) | 3/3 (100.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 2/13 (15.4%) | 13/13 (100.0%) | 3/10 (30.0%) | 3/3 (100.0%) |
| hermes | qwen3.7-max | neutral | 5/16 (31.2%) | 14/16 (87.5%) | 4/14 (28.6%) | 2/4 (50.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 3/16 (18.8%) | 16/16 (100.0%) | 8/14 (57.1%) | 7/8 (87.5%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
