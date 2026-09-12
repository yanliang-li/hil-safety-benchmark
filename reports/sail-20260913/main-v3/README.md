# SAIL HIL comparison

Status: **provisional_incomplete**. 5229/6720 attempts closed; 4671 valid, 558 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 179 | 37/179 (20.7%) | 155/179 (86.6%) | 81/136 (59.6%) | 59/82 (72.0%) | 84 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 170 | 1/170 (0.6%) | 133/170 (78.2%) | 94/129 (72.9%) | 72/106 (67.9%) | 116 / 64 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 176 | 19/176 (10.8%) | 162/176 (92.0%) | 82/130 (63.1%) | 69/84 (82.1%) | 88 / 0 |
| claude-code | glm-5.2 | sail_v3 | 165 | 5/165 (3.0%) | 137/165 (83.0%) | 86/120 (71.7%) | 65/96 (67.7%) | 97 / 57 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 131 | 19/131 (14.5%) | 120/131 (91.6%) | 45/99 (45.5%) | 35/45 (77.8%) | 46 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 124 | 2/124 (1.6%) | 103/124 (83.1%) | 56/96 (58.3%) | 41/60 (68.3%) | 50 / 31 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 179 | 28/179 (15.6%) | 163/179 (91.1%) | 62/133 (46.6%) | 44/63 (69.8%) | 71 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 161 | 3/161 (1.9%) | 133/161 (82.6%) | 78/115 (67.8%) | 55/90 (61.1%) | 87 / 86 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 160 | 16/160 (10.0%) | 144/160 (90.0%) | 51/116 (44.0%) | 42/51 (82.4%) | 54 / 0 |
| codex | glm-5.2 | sail_v3 | 134 | 0/134 (0.0%) | 121/134 (90.3%) | 63/93 (67.7%) | 53/70 (75.7%) | 49 / 49 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 151 | 19/151 (12.6%) | 128/151 (84.8%) | 43/112 (38.4%) | 35/43 (81.4%) | 75 / 0 |
| codex | qwen3.7-max | sail_v3 | 128 | 2/128 (1.6%) | 100/128 (78.1%) | 57/94 (60.6%) | 38/62 (61.3%) | 77 / 52 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 177 | 22/177 (12.4%) | 156/177 (88.1%) | 80/130 (61.5%) | 54/81 (66.7%) | 90 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 163 | 4/163 (2.5%) | 135/163 (82.8%) | 83/120 (69.2%) | 67/97 (69.1%) | 101 / 63 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 150 | 17/150 (11.3%) | 140/150 (93.3%) | 60/109 (55.0%) | 53/60 (88.3%) | 60 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 134 | 3/134 (2.2%) | 121/134 (90.3%) | 60/92 (65.2%) | 51/65 (78.5%) | 55 / 24 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 155 | 22/155 (14.2%) | 139/155 (89.7%) | 42/117 (35.9%) | 31/42 (73.8%) | 44 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 136 | 3/136 (2.2%) | 120/136 (88.2%) | 51/103 (49.5%) | 40/57 (70.2%) | 39 / 37 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 174 | 25/174 (14.4%) | 156/174 (89.7%) | 68/130 (52.3%) | 55/68 (80.9%) | 70 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 159 | 1/159 (0.6%) | 136/159 (85.5%) | 83/122 (68.0%) | 62/90 (68.9%) | 102 / 71 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 177 | 19/177 (10.7%) | 170/177 (96.0%) | 77/131 (58.8%) | 65/77 (84.4%) | 78 / 0 |
| hermes | glm-5.2 | sail_v3 | 161 | 2/161 (1.2%) | 139/161 (86.3%) | 89/119 (74.8%) | 70/97 (72.2%) | 93 / 79 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 177 | 21/177 (11.9%) | 144/177 (81.4%) | 51/135 (37.8%) | 43/52 (82.7%) | 52 / 0 |
| hermes | qwen3.7-max | sail_v3 | 172 | 3/172 (1.7%) | 130/172 (75.6%) | 69/132 (52.3%) | 43/71 (60.6%) | 51 / 31 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
