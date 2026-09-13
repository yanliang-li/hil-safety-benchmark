# SAIL HIL comparison

Status: **provisional_incomplete**. 5722/6720 attempts closed; 5135 valid, 587 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 206 | 40/206 (19.4%) | 178/206 (86.4%) | 91/155 (58.7%) | 65/92 (70.7%) | 94 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 196 | 2/196 (1.0%) | 154/196 (78.6%) | 106/147 (72.1%) | 79/121 (65.3%) | 134 / 75 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 193 | 21/193 (10.9%) | 178/193 (92.2%) | 89/141 (63.1%) | 74/91 (81.3%) | 95 / 0 |
| claude-code | glm-5.2 | sail_v3 | 181 | 5/181 (2.8%) | 150/181 (82.9%) | 93/130 (71.5%) | 71/104 (68.3%) | 106 / 63 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 155 | 22/155 (14.2%) | 143/155 (92.3%) | 52/116 (44.8%) | 41/52 (78.8%) | 53 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 147 | 2/147 (1.4%) | 124/147 (84.4%) | 66/112 (58.9%) | 49/70 (70.0%) | 58 / 36 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 200 | 31/200 (15.5%) | 180/200 (90.0%) | 68/149 (45.6%) | 49/69 (71.0%) | 77 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 180 | 3/180 (1.7%) | 150/180 (83.3%) | 87/129 (67.4%) | 63/100 (63.0%) | 95 / 90 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 180 | 17/180 (9.4%) | 163/180 (90.6%) | 56/131 (42.7%) | 47/56 (83.9%) | 59 / 0 |
| codex | glm-5.2 | sail_v3 | 154 | 0/154 (0.0%) | 140/154 (90.9%) | 71/108 (65.7%) | 60/79 (75.9%) | 56 / 52 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 175 | 22/175 (12.6%) | 150/175 (85.7%) | 52/133 (39.1%) | 42/52 (80.8%) | 94 / 0 |
| codex | qwen3.7-max | sail_v3 | 148 | 2/148 (1.4%) | 116/148 (78.4%) | 70/111 (63.1%) | 47/75 (62.7%) | 93 / 62 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 198 | 25/198 (12.6%) | 176/198 (88.9%) | 88/145 (60.7%) | 60/89 (67.4%) | 100 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 181 | 5/181 (2.8%) | 152/181 (84.0%) | 89/132 (67.4%) | 74/105 (70.5%) | 109 / 69 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 162 | 19/162 (11.7%) | 152/162 (93.8%) | 62/115 (53.9%) | 55/62 (88.7%) | 62 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 147 | 3/147 (2.0%) | 131/147 (89.1%) | 63/99 (63.6%) | 53/69 (76.8%) | 57 / 29 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 174 | 23/174 (13.2%) | 158/174 (90.8%) | 51/130 (39.2%) | 40/51 (78.4%) | 53 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 155 | 3/155 (1.9%) | 136/155 (87.7%) | 58/116 (50.0%) | 45/65 (69.2%) | 45 / 40 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 194 | 31/194 (16.0%) | 174/194 (89.7%) | 77/148 (52.0%) | 61/77 (79.2%) | 79 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 174 | 1/174 (0.6%) | 149/174 (85.6%) | 94/136 (69.1%) | 71/101 (70.3%) | 109 / 78 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 201 | 22/201 (10.9%) | 192/201 (95.5%) | 88/152 (57.9%) | 75/88 (85.2%) | 89 / 0 |
| hermes | glm-5.2 | sail_v3 | 180 | 2/180 (1.1%) | 156/180 (86.7%) | 103/136 (75.7%) | 82/112 (73.2%) | 108 / 96 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 191 | 22/191 (11.5%) | 158/191 (82.7%) | 57/143 (39.9%) | 49/58 (84.5%) | 58 / 0 |
| hermes | qwen3.7-max | sail_v3 | 185 | 3/185 (1.6%) | 141/185 (76.2%) | 74/139 (53.2%) | 47/77 (61.0%) | 55 / 33 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
