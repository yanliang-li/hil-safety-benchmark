# Four-framework API experiment

Status: **provisional_incomplete**. 1865/5760 attempts closed; 1797 valid, 68 failed, 3895 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 24/86 (27.9%) | 72/86 (83.7%) | 42/65 (64.6%) | 25/42 (59.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 17/86 (19.8%) | 70/86 (81.4%) | 43/65 (66.2%) | 25/43 (58.1%) |
| claude-code | glm-5.2 | neutral | 14/84 (16.7%) | 77/84 (91.7%) | 37/63 (58.7%) | 30/37 (81.1%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 9/83 (10.8%) | 75/83 (90.4%) | 38/63 (60.3%) | 31/38 (81.6%) |
| claude-code | qwen3.7-max | neutral | 24/91 (26.4%) | 86/91 (94.5%) | 25/67 (37.3%) | 17/25 (68.0%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 10/90 (11.1%) | 86/90 (95.6%) | 30/67 (44.8%) | 26/31 (83.9%) |
| codex | deepseek-v4-flash | neutral | 21/80 (26.2%) | 70/80 (87.5%) | 24/59 (40.7%) | 17/24 (70.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 13/86 (15.1%) | 76/86 (88.4%) | 25/62 (40.3%) | 18/25 (72.0%) |
| codex | glm-5.2 | neutral | 22/77 (28.6%) | 69/77 (89.6%) | 20/57 (35.1%) | 15/20 (75.0%) |
| codex | glm-5.2 | prompt_guard_v1 | 11/76 (14.5%) | 71/76 (93.4%) | 23/56 (41.1%) | 21/23 (91.3%) |
| codex | qwen3.7-max | neutral | 31/85 (36.5%) | 81/85 (95.3%) | 18/64 (28.1%) | 11/18 (61.1%) |
| codex | qwen3.7-max | prompt_guard_v1 | 13/85 (15.3%) | 79/85 (92.9%) | 28/65 (43.1%) | 21/28 (75.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 21/85 (24.7%) | 75/85 (88.2%) | 35/65 (53.8%) | 25/35 (71.4%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 12/84 (14.3%) | 76/84 (90.5%) | 38/64 (59.4%) | 28/38 (73.7%) |
| deepseek-harness | glm-5.2 | neutral | 12/71 (16.9%) | 68/71 (95.8%) | 25/50 (50.0%) | 21/25 (84.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/71 (9.9%) | 66/71 (93.0%) | 29/50 (58.0%) | 25/29 (86.2%) |
| deepseek-harness | qwen3.7-max | neutral | 26/91 (28.6%) | 87/91 (95.6%) | 18/69 (26.1%) | 14/18 (77.8%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 9/91 (9.9%) | 86/91 (94.5%) | 25/69 (36.2%) | 23/25 (92.0%) |
| hermes | deepseek-v4-flash | neutral | 16/52 (30.8%) | 44/52 (84.6%) | 20/38 (52.6%) | 15/20 (75.0%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 9/50 (18.0%) | 43/50 (86.0%) | 18/36 (50.0%) | 12/18 (66.7%) |
| hermes | glm-5.2 | neutral | 10/42 (23.8%) | 36/42 (85.7%) | 13/33 (39.4%) | 8/13 (61.5%) |
| hermes | glm-5.2 | prompt_guard_v1 | 5/45 (11.1%) | 43/45 (95.6%) | 18/35 (51.4%) | 14/18 (77.8%) |
| hermes | qwen3.7-max | neutral | 13/52 (25.0%) | 49/52 (94.2%) | 10/39 (25.6%) | 8/10 (80.0%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 6/54 (11.1%) | 51/54 (94.4%) | 16/40 (40.0%) | 14/16 (87.5%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
