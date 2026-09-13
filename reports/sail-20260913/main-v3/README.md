# SAIL HIL comparison

Status: **provisional_incomplete**. 5974/6720 attempts closed; 5364 valid, 610 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 217 | 43/217 (19.8%) | 189/217 (87.1%) | 97/164 (59.1%) | 71/98 (72.4%) | 101 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 205 | 2/205 (1.0%) | 161/205 (78.5%) | 111/154 (72.1%) | 83/126 (65.9%) | 138 / 78 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 200 | 21/200 (10.5%) | 184/200 (92.0%) | 93/147 (63.3%) | 78/95 (82.1%) | 99 / 0 |
| claude-code | glm-5.2 | sail_v3 | 187 | 5/187 (2.7%) | 155/187 (82.9%) | 95/135 (70.4%) | 73/106 (68.9%) | 108 / 64 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 161 | 22/161 (13.7%) | 148/161 (91.9%) | 56/122 (45.9%) | 43/56 (76.8%) | 57 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 154 | 2/154 (1.3%) | 129/154 (83.8%) | 70/119 (58.8%) | 51/74 (68.9%) | 62 / 38 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 209 | 32/209 (15.3%) | 188/209 (90.0%) | 72/157 (45.9%) | 53/73 (72.6%) | 85 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 187 | 3/187 (1.6%) | 156/187 (83.4%) | 91/135 (67.4%) | 67/105 (63.8%) | 98 / 93 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 193 | 20/193 (10.4%) | 174/193 (90.2%) | 59/138 (42.8%) | 50/59 (84.7%) | 62 / 0 |
| codex | glm-5.2 | sail_v3 | 164 | 1/164 (0.6%) | 148/164 (90.2%) | 74/112 (66.1%) | 63/85 (74.1%) | 59 / 55 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 186 | 24/186 (12.9%) | 159/186 (85.5%) | 54/138 (39.1%) | 44/54 (81.5%) | 97 / 0 |
| codex | qwen3.7-max | sail_v3 | 157 | 2/157 (1.3%) | 122/157 (77.7%) | 72/115 (62.6%) | 49/78 (62.8%) | 97 / 68 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 212 | 27/212 (12.7%) | 188/212 (88.7%) | 95/159 (59.7%) | 67/96 (69.8%) | 107 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 193 | 5/193 (2.6%) | 162/193 (83.9%) | 98/144 (68.1%) | 80/114 (70.2%) | 116 / 73 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 174 | 21/174 (12.1%) | 164/174 (94.3%) | 67/126 (53.2%) | 60/67 (89.6%) | 67 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 157 | 3/157 (1.9%) | 141/157 (89.8%) | 67/108 (62.0%) | 57/73 (78.1%) | 61 / 30 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 183 | 25/183 (13.7%) | 165/183 (90.2%) | 54/138 (39.1%) | 42/54 (77.8%) | 56 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 163 | 3/163 (1.8%) | 143/163 (87.7%) | 63/123 (51.2%) | 49/70 (70.0%) | 48 / 45 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 206 | 33/206 (16.0%) | 185/206 (89.8%) | 81/155 (52.3%) | 64/81 (79.0%) | 83 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 187 | 1/187 (0.5%) | 159/187 (85.0%) | 99/143 (69.2%) | 75/108 (69.4%) | 114 / 83 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 207 | 22/207 (10.6%) | 198/207 (95.7%) | 89/156 (57.1%) | 76/89 (85.4%) | 90 / 0 |
| hermes | glm-5.2 | sail_v3 | 186 | 2/186 (1.1%) | 162/186 (87.1%) | 105/140 (75.0%) | 83/114 (72.8%) | 109 / 97 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 201 | 22/201 (10.9%) | 167/201 (83.1%) | 58/150 (38.7%) | 50/59 (84.7%) | 59 / 0 |
| hermes | qwen3.7-max | sail_v3 | 197 | 3/197 (1.5%) | 149/197 (75.6%) | 77/148 (52.0%) | 49/80 (61.2%) | 57 / 34 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
