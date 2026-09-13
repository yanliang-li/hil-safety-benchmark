# SAIL HIL comparison

Status: **provisional_incomplete**. 5471/6720 attempts closed; 4901 valid, 570 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 193 | 38/193 (19.7%) | 167/193 (86.5%) | 85/146 (58.2%) | 62/86 (72.1%) | 88 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 182 | 2/182 (1.1%) | 143/182 (78.6%) | 98/137 (71.5%) | 75/112 (67.0%) | 122 / 68 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 186 | 20/186 (10.8%) | 172/186 (92.5%) | 86/137 (62.8%) | 72/88 (81.8%) | 92 / 0 |
| claude-code | glm-5.2 | sail_v3 | 173 | 5/173 (2.9%) | 145/173 (83.8%) | 89/125 (71.2%) | 68/99 (68.7%) | 99 / 59 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 144 | 20/144 (13.9%) | 132/144 (91.7%) | 50/109 (45.9%) | 39/50 (78.0%) | 51 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 135 | 2/135 (1.5%) | 114/135 (84.4%) | 60/104 (57.7%) | 45/64 (70.3%) | 53 / 32 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 189 | 29/189 (15.3%) | 171/189 (90.5%) | 66/140 (47.1%) | 47/67 (70.1%) | 75 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 171 | 3/171 (1.8%) | 142/171 (83.0%) | 82/122 (67.2%) | 58/94 (61.7%) | 90 / 87 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 168 | 16/168 (9.5%) | 152/168 (90.5%) | 53/122 (43.4%) | 44/53 (83.0%) | 56 / 0 |
| codex | glm-5.2 | sail_v3 | 142 | 0/142 (0.0%) | 129/142 (90.8%) | 66/99 (66.7%) | 56/73 (76.7%) | 52 / 49 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 163 | 20/163 (12.3%) | 139/163 (85.3%) | 47/122 (38.5%) | 39/47 (83.0%) | 81 / 0 |
| codex | qwen3.7-max | sail_v3 | 136 | 2/136 (1.5%) | 106/136 (77.9%) | 62/100 (62.0%) | 41/67 (61.2%) | 84 / 58 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 188 | 24/188 (12.8%) | 167/188 (88.8%) | 84/138 (60.9%) | 58/85 (68.2%) | 96 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 173 | 5/173 (2.9%) | 145/173 (83.8%) | 87/127 (68.5%) | 71/102 (69.6%) | 106 / 67 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 156 | 18/156 (11.5%) | 146/156 (93.6%) | 61/112 (54.5%) | 54/61 (88.5%) | 61 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 141 | 3/141 (2.1%) | 127/141 (90.1%) | 62/96 (64.6%) | 53/67 (79.1%) | 56 / 26 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 167 | 22/167 (13.2%) | 151/167 (90.4%) | 48/126 (38.1%) | 37/48 (77.1%) | 50 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 148 | 3/148 (2.0%) | 132/148 (89.2%) | 55/112 (49.1%) | 44/61 (72.1%) | 43 / 37 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 185 | 29/185 (15.7%) | 166/185 (89.7%) | 72/140 (51.4%) | 57/72 (79.2%) | 74 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 167 | 1/167 (0.6%) | 143/167 (85.6%) | 89/130 (68.5%) | 67/96 (69.8%) | 105 / 74 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 189 | 21/189 (11.1%) | 181/189 (95.8%) | 81/142 (57.0%) | 69/81 (85.2%) | 82 / 0 |
| hermes | glm-5.2 | sail_v3 | 169 | 2/169 (1.2%) | 147/169 (87.0%) | 94/127 (74.0%) | 75/102 (73.5%) | 97 / 87 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 182 | 22/182 (12.1%) | 149/182 (81.9%) | 52/138 (37.7%) | 44/53 (83.0%) | 53 / 0 |
| hermes | qwen3.7-max | sail_v3 | 176 | 3/176 (1.7%) | 133/176 (75.6%) | 70/134 (52.2%) | 44/73 (60.3%) | 52 / 32 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
