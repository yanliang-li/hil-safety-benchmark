# Four-framework API experiment

Status: **provisional_incomplete**. 2784/5760 attempts closed; 2695 valid, 89 failed, 2976 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 33/128 (25.8%) | 109/128 (85.2%) | 62/96 (64.6%) | 39/62 (62.9%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 24/129 (18.6%) | 109/129 (84.5%) | 62/97 (63.9%) | 43/62 (69.4%) |
| claude-code | glm-5.2 | neutral | 20/126 (15.9%) | 114/126 (90.5%) | 59/96 (61.5%) | 46/59 (78.0%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 13/128 (10.2%) | 116/128 (90.6%) | 59/97 (60.8%) | 47/59 (79.7%) |
| claude-code | qwen3.7-max | neutral | 36/128 (28.1%) | 122/128 (95.3%) | 39/94 (41.5%) | 25/39 (64.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 16/128 (12.5%) | 123/128 (96.1%) | 48/94 (51.1%) | 40/49 (81.6%) |
| codex | deepseek-v4-flash | neutral | 32/121 (26.4%) | 108/121 (89.3%) | 39/91 (42.9%) | 27/39 (69.2%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 19/126 (15.1%) | 112/126 (88.9%) | 35/95 (36.8%) | 24/35 (68.6%) |
| codex | glm-5.2 | neutral | 25/109 (22.9%) | 99/109 (90.8%) | 32/82 (39.0%) | 26/32 (81.2%) |
| codex | glm-5.2 | prompt_guard_v1 | 12/108 (11.1%) | 101/108 (93.5%) | 38/81 (46.9%) | 36/38 (94.7%) |
| codex | qwen3.7-max | neutral | 44/127 (34.6%) | 121/127 (95.3%) | 25/95 (26.3%) | 18/25 (72.0%) |
| codex | qwen3.7-max | prompt_guard_v1 | 20/126 (15.9%) | 118/126 (93.7%) | 39/96 (40.6%) | 30/39 (76.9%) |
| deepseek-harness | deepseek-v4-flash | neutral | 35/124 (28.2%) | 109/124 (87.9%) | 48/94 (51.1%) | 34/48 (70.8%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 21/123 (17.1%) | 108/123 (87.8%) | 54/93 (58.1%) | 36/54 (66.7%) |
| deepseek-harness | glm-5.2 | neutral | 19/103 (18.4%) | 96/103 (93.2%) | 33/76 (43.4%) | 26/33 (78.8%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 10/101 (9.9%) | 94/101 (93.1%) | 40/75 (53.3%) | 33/40 (82.5%) |
| deepseek-harness | qwen3.7-max | neutral | 38/130 (29.2%) | 123/130 (94.6%) | 26/101 (25.7%) | 19/26 (73.1%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 14/130 (10.8%) | 122/130 (93.8%) | 35/101 (34.7%) | 30/35 (85.7%) |
| hermes | deepseek-v4-flash | neutral | 24/84 (28.6%) | 73/84 (86.9%) | 33/62 (53.2%) | 24/33 (72.7%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 12/81 (14.8%) | 71/81 (87.7%) | 30/61 (49.2%) | 23/31 (74.2%) |
| hermes | glm-5.2 | neutral | 21/81 (25.9%) | 73/81 (90.1%) | 28/62 (45.2%) | 22/28 (78.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/82 (14.6%) | 78/82 (95.1%) | 33/62 (53.2%) | 27/33 (81.8%) |
| hermes | qwen3.7-max | neutral | 20/85 (23.5%) | 78/85 (91.8%) | 17/65 (26.2%) | 12/17 (70.6%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 11/87 (12.6%) | 81/87 (93.1%) | 26/66 (39.4%) | 20/26 (76.9%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
