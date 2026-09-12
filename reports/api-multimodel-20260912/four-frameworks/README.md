# Four-framework API experiment

Status: **provisional_incomplete**. 3368/5760 attempts closed; 3267 valid, 101 failed, 2392 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 40/153 (26.1%) | 130/153 (85.0%) | 70/114 (61.4%) | 44/71 (62.0%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 28/152 (18.4%) | 128/152 (84.2%) | 70/114 (61.4%) | 48/71 (67.6%) |
| claude-code | glm-5.2 | neutral | 23/151 (15.2%) | 137/151 (90.7%) | 69/114 (60.5%) | 55/70 (78.6%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 16/151 (10.6%) | 138/151 (91.4%) | 68/114 (59.6%) | 55/68 (80.9%) |
| claude-code | qwen3.7-max | neutral | 44/154 (28.6%) | 146/154 (94.8%) | 46/115 (40.0%) | 30/46 (65.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 18/153 (11.8%) | 146/153 (95.4%) | 57/114 (50.0%) | 48/58 (82.8%) |
| codex | deepseek-v4-flash | neutral | 36/147 (24.5%) | 132/147 (89.8%) | 46/111 (41.4%) | 31/46 (67.4%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 22/149 (14.8%) | 134/149 (89.9%) | 41/112 (36.6%) | 28/41 (68.3%) |
| codex | glm-5.2 | neutral | 31/135 (23.0%) | 124/135 (91.9%) | 36/99 (36.4%) | 28/36 (77.8%) |
| codex | glm-5.2 | prompt_guard_v1 | 15/136 (11.0%) | 127/136 (93.4%) | 46/99 (46.5%) | 43/46 (93.5%) |
| codex | qwen3.7-max | neutral | 52/153 (34.0%) | 144/153 (94.1%) | 32/115 (27.8%) | 22/32 (68.8%) |
| codex | qwen3.7-max | prompt_guard_v1 | 22/151 (14.6%) | 141/151 (93.4%) | 47/114 (41.2%) | 37/47 (78.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 40/144 (27.8%) | 126/144 (87.5%) | 60/110 (54.5%) | 42/60 (70.0%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 24/145 (16.6%) | 127/145 (87.6%) | 64/110 (58.2%) | 46/65 (70.8%) |
| deepseek-harness | glm-5.2 | neutral | 25/133 (18.8%) | 124/133 (93.2%) | 47/95 (49.5%) | 39/47 (83.0%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 13/126 (10.3%) | 118/126 (93.7%) | 51/90 (56.7%) | 43/51 (84.3%) |
| deepseek-harness | qwen3.7-max | neutral | 43/153 (28.1%) | 146/153 (95.4%) | 32/115 (27.8%) | 23/32 (71.9%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 15/153 (9.8%) | 145/153 (94.8%) | 42/115 (36.5%) | 37/42 (88.1%) |
| hermes | deepseek-v4-flash | neutral | 33/107 (30.8%) | 95/107 (88.8%) | 42/81 (51.9%) | 30/42 (71.4%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 16/106 (15.1%) | 94/106 (88.7%) | 41/81 (50.6%) | 32/42 (76.2%) |
| hermes | glm-5.2 | neutral | 23/99 (23.2%) | 90/99 (90.9%) | 38/77 (49.4%) | 31/38 (81.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 12/101 (11.9%) | 96/101 (95.0%) | 44/78 (56.4%) | 37/44 (84.1%) |
| hermes | qwen3.7-max | neutral | 30/107 (28.0%) | 97/107 (90.7%) | 18/80 (22.5%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 14/108 (13.0%) | 101/108 (93.5%) | 32/80 (40.0%) | 25/32 (78.1%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
