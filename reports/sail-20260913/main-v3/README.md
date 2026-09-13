# SAIL HIL comparison

Status: **provisional_incomplete**. 6484/6720 attempts closed; 5830 valid, 654 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 237 | 44/237 (18.6%) | 206/237 (86.9%) | 105/177 (59.3%) | 79/107 (73.8%) | 111 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 223 | 2/223 (0.9%) | 175/223 (78.5%) | 121/166 (72.9%) | 91/138 (65.9%) | 149 / 80 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 228 | 23/228 (10.1%) | 208/228 (91.2%) | 107/170 (62.9%) | 89/109 (81.7%) | 113 / 0 |
| claude-code | glm-5.2 | sail_v3 | 212 | 5/212 (2.4%) | 177/212 (83.5%) | 108/155 (69.7%) | 83/120 (69.2%) | 124 / 70 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 180 | 23/180 (12.8%) | 166/180 (92.2%) | 62/135 (45.9%) | 48/62 (77.4%) | 63 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 170 | 3/170 (1.8%) | 141/170 (82.9%) | 78/131 (59.5%) | 55/82 (67.1%) | 70 / 42 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 226 | 35/226 (15.5%) | 205/226 (90.7%) | 77/169 (45.6%) | 57/78 (73.1%) | 91 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 203 | 4/203 (2.0%) | 170/203 (83.7%) | 97/146 (66.4%) | 72/113 (63.7%) | 103 / 103 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 213 | 23/213 (10.8%) | 194/213 (91.1%) | 68/154 (44.2%) | 59/68 (86.8%) | 71 / 0 |
| codex | glm-5.2 | sail_v3 | 182 | 1/182 (0.5%) | 165/182 (90.7%) | 82/125 (65.6%) | 71/95 (74.7%) | 65 / 60 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 196 | 24/196 (12.2%) | 167/196 (85.2%) | 54/145 (37.2%) | 44/54 (81.5%) | 97 / 0 |
| codex | qwen3.7-max | sail_v3 | 170 | 2/170 (1.2%) | 133/170 (78.2%) | 74/125 (59.2%) | 49/80 (61.2%) | 99 / 68 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 233 | 30/233 (12.9%) | 205/233 (88.0%) | 105/173 (60.7%) | 72/106 (67.9%) | 121 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 215 | 5/215 (2.3%) | 178/215 (82.8%) | 108/159 (67.9%) | 87/126 (69.0%) | 128 / 83 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 194 | 24/194 (12.4%) | 182/194 (93.8%) | 79/140 (56.4%) | 70/79 (88.6%) | 80 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 173 | 4/173 (2.3%) | 156/173 (90.2%) | 77/119 (64.7%) | 66/83 (79.5%) | 71 / 31 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 206 | 28/206 (13.6%) | 185/206 (89.8%) | 58/152 (38.2%) | 46/58 (79.3%) | 60 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 185 | 5/185 (2.7%) | 163/185 (88.1%) | 68/136 (50.0%) | 53/77 (68.8%) | 52 / 50 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 225 | 36/225 (16.0%) | 202/225 (89.8%) | 88/170 (51.8%) | 71/89 (79.8%) | 91 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 206 | 2/206 (1.0%) | 176/206 (85.4%) | 109/158 (69.0%) | 83/120 (69.2%) | 126 / 94 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 230 | 27/230 (11.7%) | 220/230 (95.7%) | 100/172 (58.1%) | 84/100 (84.0%) | 102 / 0 |
| hermes | glm-5.2 | sail_v3 | 207 | 4/207 (1.9%) | 180/207 (87.0%) | 117/154 (76.0%) | 93/128 (72.7%) | 118 / 113 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 222 | 25/222 (11.3%) | 184/222 (82.9%) | 63/165 (38.2%) | 52/64 (81.2%) | 64 / 0 |
| hermes | qwen3.7-max | sail_v3 | 216 | 3/216 (1.4%) | 162/216 (75.0%) | 82/162 (50.6%) | 51/86 (59.3%) | 61 / 40 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
