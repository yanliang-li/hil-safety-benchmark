# SAIL HIL comparison

Status: **complete**. 6720/6720 attempts closed; 6019 valid, 701 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 240 | 45/240 (18.8%) | 209/240 (87.1%) | 108/180 (60.0%) | 80/110 (72.7%) | 114 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 227 | 2/227 (0.9%) | 178/227 (78.4%) | 125/170 (73.5%) | 94/142 (66.2%) | 152 / 84 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 240 | 25/240 (10.4%) | 220/240 (91.7%) | 113/180 (62.8%) | 93/115 (80.9%) | 119 / 0 |
| claude-code | glm-5.2 | sail_v3 | 224 | 6/224 (2.7%) | 187/224 (83.5%) | 116/165 (70.3%) | 87/128 (68.0%) | 135 / 76 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 185 | 24/185 (13.0%) | 171/185 (92.4%) | 64/138 (46.4%) | 50/64 (78.1%) | 65 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 173 | 3/173 (1.7%) | 144/173 (83.2%) | 79/134 (59.0%) | 56/83 (67.5%) | 70 / 44 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 238 | 38/238 (16.0%) | 216/238 (90.8%) | 81/178 (45.5%) | 60/82 (73.2%) | 97 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 215 | 4/215 (1.9%) | 179/215 (83.3%) | 102/155 (65.8%) | 76/119 (63.9%) | 108 / 106 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 220 | 24/220 (10.9%) | 201/220 (91.4%) | 71/160 (44.4%) | 61/71 (85.9%) | 75 / 0 |
| codex | glm-5.2 | sail_v3 | 187 | 1/187 (0.5%) | 170/187 (90.9%) | 85/130 (65.4%) | 74/98 (75.5%) | 67 / 62 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 206 | 25/206 (12.1%) | 174/206 (84.5%) | 55/151 (36.4%) | 44/55 (80.0%) | 99 / 0 |
| codex | qwen3.7-max | sail_v3 | 177 | 2/177 (1.1%) | 138/177 (78.0%) | 76/129 (58.9%) | 50/82 (61.0%) | 104 / 70 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 240 | 31/240 (12.9%) | 210/240 (87.5%) | 109/180 (60.6%) | 75/110 (68.2%) | 125 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 221 | 5/221 (2.3%) | 183/221 (82.8%) | 113/165 (68.5%) | 91/131 (69.5%) | 132 / 85 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 201 | 24/201 (11.9%) | 189/201 (94.0%) | 82/145 (56.6%) | 72/82 (87.8%) | 83 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 181 | 4/181 (2.2%) | 164/181 (90.6%) | 80/125 (64.0%) | 68/86 (79.1%) | 74 / 31 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 215 | 29/215 (13.5%) | 192/215 (89.3%) | 63/160 (39.4%) | 50/63 (79.4%) | 65 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 191 | 5/191 (2.6%) | 167/191 (87.4%) | 70/142 (49.3%) | 55/79 (69.6%) | 54 / 50 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 239 | 37/239 (15.5%) | 213/239 (89.1%) | 96/179 (53.6%) | 76/97 (78.4%) | 100 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 218 | 2/218 (0.9%) | 186/218 (85.3%) | 114/165 (69.1%) | 88/127 (69.3%) | 133 / 102 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 239 | 28/239 (11.7%) | 228/239 (95.4%) | 105/180 (58.3%) | 88/105 (83.8%) | 107 / 0 |
| hermes | glm-5.2 | sail_v3 | 216 | 4/216 (1.9%) | 187/216 (86.6%) | 124/161 (77.0%) | 97/135 (71.9%) | 127 / 115 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 228 | 25/228 (11.0%) | 188/228 (82.5%) | 65/170 (38.2%) | 54/66 (81.8%) | 66 / 0 |
| hermes | qwen3.7-max | sail_v3 | 220 | 3/220 (1.4%) | 164/220 (74.5%) | 84/165 (50.9%) | 53/88 (60.2%) | 63 / 43 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
