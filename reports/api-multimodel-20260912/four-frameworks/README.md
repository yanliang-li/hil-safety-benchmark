# Four-framework API experiment

Status: **provisional_incomplete**. 4963/5760 attempts closed; 4788 valid, 175 failed, 797 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 54/216 (25.0%) | 184/216 (85.2%) | 98/161 (60.9%) | 63/99 (63.6%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 40/218 (18.3%) | 186/218 (85.3%) | 100/163 (61.3%) | 69/101 (68.3%) |
| claude-code | glm-5.2 | neutral | 40/224 (17.9%) | 205/224 (91.5%) | 97/166 (58.4%) | 73/98 (74.5%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 26/225 (11.6%) | 207/225 (92.0%) | 96/167 (57.5%) | 77/96 (80.2%) |
| claude-code | qwen3.7-max | neutral | 66/218 (30.3%) | 206/218 (94.5%) | 65/162 (40.1%) | 45/65 (69.2%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 28/217 (12.9%) | 206/217 (94.9%) | 77/161 (47.8%) | 64/78 (82.1%) |
| codex | deepseek-v4-flash | neutral | 51/210 (24.3%) | 189/210 (90.0%) | 63/157 (40.1%) | 43/63 (68.3%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 31/214 (14.5%) | 193/214 (90.2%) | 62/160 (38.8%) | 44/62 (71.0%) |
| codex | glm-5.2 | neutral | 42/198 (21.2%) | 181/198 (91.4%) | 54/145 (37.2%) | 45/54 (83.3%) |
| codex | glm-5.2 | prompt_guard_v1 | 24/197 (12.2%) | 183/197 (92.9%) | 65/142 (45.8%) | 60/65 (92.3%) |
| codex | qwen3.7-max | neutral | 70/215 (32.6%) | 204/215 (94.9%) | 41/160 (25.6%) | 29/41 (70.7%) |
| codex | qwen3.7-max | prompt_guard_v1 | 25/208 (12.0%) | 194/208 (93.3%) | 64/156 (41.0%) | 51/64 (79.7%) |
| deepseek-harness | deepseek-v4-flash | neutral | 63/214 (29.4%) | 189/214 (88.3%) | 88/162 (54.3%) | 62/89 (69.7%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 35/214 (16.4%) | 191/214 (89.3%) | 96/162 (59.3%) | 72/97 (74.2%) |
| deepseek-harness | glm-5.2 | neutral | 40/196 (20.4%) | 182/196 (92.9%) | 70/141 (49.6%) | 55/71 (77.5%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/185 (11.9%) | 176/185 (95.1%) | 77/134 (57.5%) | 65/77 (84.4%) |
| deepseek-harness | qwen3.7-max | neutral | 69/221 (31.2%) | 211/221 (95.5%) | 49/166 (29.5%) | 35/49 (71.4%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/221 (11.8%) | 210/221 (95.0%) | 65/165 (39.4%) | 56/65 (86.2%) |
| hermes | deepseek-v4-flash | neutral | 51/165 (30.9%) | 143/165 (86.7%) | 62/122 (50.8%) | 41/62 (66.1%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 26/160 (16.2%) | 145/160 (90.6%) | 59/119 (49.6%) | 46/60 (76.7%) |
| hermes | glm-5.2 | neutral | 35/160 (21.9%) | 148/160 (92.5%) | 58/120 (48.3%) | 48/58 (82.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 19/163 (11.7%) | 155/163 (95.1%) | 70/121 (57.9%) | 58/70 (82.9%) |
| hermes | qwen3.7-max | neutral | 42/165 (25.5%) | 151/165 (91.5%) | 29/126 (23.0%) | 22/29 (75.9%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/164 (11.6%) | 154/164 (93.9%) | 47/124 (37.9%) | 38/47 (80.9%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
