# Four-framework API experiment

Status: **provisional_incomplete**. 5074/5760 attempts closed; 4894 valid, 180 failed, 686 pending.

| Framework | Requested model | Condition | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | neutral | 57/224 (25.4%) | 192/224 (85.7%) | 100/167 (59.9%) | 64/101 (63.4%) |
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 43/223 (19.3%) | 191/223 (85.7%) | 100/166 (60.2%) | 69/101 (68.3%) |
| claude-code | glm-5.2 | neutral | 40/228 (17.5%) | 208/228 (91.2%) | 99/169 (58.6%) | 75/100 (75.0%) |
| claude-code | glm-5.2 | prompt_guard_v1 | 27/228 (11.8%) | 210/228 (92.1%) | 97/169 (57.4%) | 78/97 (80.4%) |
| claude-code | qwen3.7-max | neutral | 66/224 (29.5%) | 212/224 (94.6%) | 67/166 (40.4%) | 47/67 (70.1%) |
| claude-code | qwen3.7-max | prompt_guard_v1 | 28/223 (12.6%) | 212/223 (95.1%) | 80/165 (48.5%) | 67/81 (82.7%) |
| codex | deepseek-v4-flash | neutral | 51/211 (24.2%) | 190/211 (90.0%) | 64/158 (40.5%) | 44/64 (68.8%) |
| codex | deepseek-v4-flash | prompt_guard_v1 | 31/215 (14.4%) | 194/215 (90.2%) | 63/161 (39.1%) | 45/63 (71.4%) |
| codex | glm-5.2 | neutral | 43/200 (21.5%) | 183/200 (91.5%) | 54/145 (37.2%) | 45/54 (83.3%) |
| codex | glm-5.2 | prompt_guard_v1 | 24/198 (12.1%) | 184/198 (92.9%) | 65/143 (45.5%) | 60/65 (92.3%) |
| codex | qwen3.7-max | neutral | 73/221 (33.0%) | 210/221 (95.0%) | 42/164 (25.6%) | 30/42 (71.4%) |
| codex | qwen3.7-max | prompt_guard_v1 | 25/212 (11.8%) | 198/212 (93.4%) | 65/159 (40.9%) | 52/65 (80.0%) |
| deepseek-harness | deepseek-v4-flash | neutral | 65/218 (29.8%) | 193/218 (88.5%) | 90/164 (54.9%) | 63/91 (69.2%) |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37/220 (16.8%) | 197/220 (89.5%) | 98/164 (59.8%) | 73/99 (73.7%) |
| deepseek-harness | glm-5.2 | neutral | 41/202 (20.3%) | 187/202 (92.6%) | 71/145 (49.0%) | 56/72 (77.8%) |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 22/191 (11.5%) | 181/191 (94.8%) | 79/138 (57.2%) | 66/79 (83.5%) |
| deepseek-harness | qwen3.7-max | neutral | 71/227 (31.3%) | 216/227 (95.2%) | 50/172 (29.1%) | 36/50 (72.0%) |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 26/228 (11.4%) | 216/228 (94.7%) | 67/171 (39.2%) | 58/67 (86.6%) |
| hermes | deepseek-v4-flash | neutral | 52/168 (31.0%) | 145/168 (86.3%) | 64/125 (51.2%) | 42/64 (65.6%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 28/166 (16.9%) | 150/166 (90.4%) | 63/124 (50.8%) | 48/64 (75.0%) |
| hermes | glm-5.2 | neutral | 36/162 (22.2%) | 150/162 (92.6%) | 58/120 (48.3%) | 48/58 (82.8%) |
| hermes | glm-5.2 | prompt_guard_v1 | 19/165 (11.5%) | 157/165 (95.2%) | 70/121 (57.9%) | 58/70 (82.9%) |
| hermes | qwen3.7-max | neutral | 42/170 (24.7%) | 156/170 (91.8%) | 32/129 (24.8%) | 25/32 (78.1%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 19/170 (11.2%) | 160/170 (94.1%) | 48/129 (37.2%) | 39/48 (81.2%) |

Hermes was added later, with a configured 65,536-token context; Codex and DeepSeek Harness use 32,768, and Claude Code retains native context handling. Different framework prompts, runtimes, calendar periods and serving behavior remain possible confounds.

Each condition consults a different subset; conditional success rates do not estimate a causal effect of feedback.

The 80 cases are reused exploratory tasks, not an untouched test set. Independent risk-recognition and semantic question-quality labels remain unavailable. Main safety rates exclude failed attempts; the all-attempt audit retains observed unsafe actions in failed traces and sensitivity bounds. No partial-table defense improvement is asserted.
