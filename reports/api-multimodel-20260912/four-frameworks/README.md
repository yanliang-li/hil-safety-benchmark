# Four-framework API experiment

Status: **provisional_incomplete**. 2406/5760 attempts closed; 2324 valid, 82 failed, 3354 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 30/110 (27.3%) | 95/110 (86.4%) | 52/81 (64.2%) | 32/52 (61.5%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 22/112 (19.6%) | 94/112 (83.9%) | 53/83 (63.9%) | 34/53 (64.2%) |
| claude-code | glm-5.2 | neutral | 18/111 (16.2%) | 100/111 (90.1%) | 51/86 (59.3%) | 39/51 (76.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 10/109 (9.2%) | 99/109 (90.8%) | 47/83 (56.6%) | 38/47 (80.9%) |
| claude-code | qwen3.7-max | neutral | 28/110 (25.5%) | 105/110 (95.5%) | 33/83 (39.8%) | 23/33 (69.7%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 11/110 (10.0%) | 106/110 (96.4%) | 40/83 (48.2%) | 34/41 (82.9%) |
| codex | deepseek-v4-flash | neutral | 27/107 (25.2%) | 95/107 (88.8%) | 34/81 (42.0%) | 25/34 (73.5%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 16/110 (14.5%) | 98/110 (89.1%) | 30/82 (36.6%) | 21/30 (70.0%) |
| codex | glm-5.2 | neutral | 22/91 (24.2%) | 82/91 (90.1%) | 26/68 (38.2%) | 21/26 (80.8%) |
| codex | glm-5.2 | prompt_guard_v1 | 11/89 (12.4%) | 84/89 (94.4%) | 30/66 (45.5%) | 28/30 (93.3%) |
| codex | qwen3.7-max | neutral | 40/114 (35.1%) | 109/114 (95.6%) | 23/86 (26.7%) | 16/23 (69.6%) |
| codex | qwen3.7-max | prompt_guard_v1 | 18/112 (16.1%) | 105/112 (93.8%) | 35/85 (41.2%) | 27/35 (77.1%) |
| deepseek-harness | deepseek-v4-flash | neutral | 31/111 (27.9%) | 98/111 (88.3%) | 45/85 (52.9%) | 32/45 (71.1%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 19/111 (17.1%) | 98/111 (88.3%) | 49/85 (57.6%) | 34/49 (69.4%) |
| deepseek-harness | glm-5.2 | neutral | 16/90 (17.8%) | 85/90 (94.4%) | 30/65 (46.2%) | 25/30 (83.3%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 7/89 (7.9%) | 83/89 (93.3%) | 36/65 (55.4%) | 31/36 (86.1%) |
| deepseek-harness | qwen3.7-max | neutral | 35/112 (31.2%) | 107/112 (95.5%) | 21/86 (24.4%) | 14/21 (66.7%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 12/112 (10.7%) | 106/112 (94.6%) | 29/86 (33.7%) | 25/29 (86.2%) |
| hermes | deepseek-v4-flash | neutral | 20/70 (28.6%) | 61/70 (87.1%) | 27/53 (50.9%) | 22/27 (81.5%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 11/67 (16.4%) | 58/67 (86.6%) | 24/51 (47.1%) | 18/25 (72.0%) |
| hermes | glm-5.2 | neutral | 16/64 (25.0%) | 58/64 (90.6%) | 24/50 (48.0%) | 18/24 (75.0%) |
| hermes | glm-5.2 | prompt_guard_v1 | 8/68 (11.8%) | 66/68 (97.1%) | 29/52 (55.8%) | 25/29 (86.2%) |
| hermes | qwen3.7-max | neutral | 16/72 (22.2%) | 65/72 (90.3%) | 13/55 (23.6%) | 10/13 (76.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 9/73 (12.3%) | 68/73 (93.2%) | 19/55 (34.5%) | 15/19 (78.9%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
