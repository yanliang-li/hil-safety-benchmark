# SAIL HIL comparison

Status: **provisional_incomplete**. 6219/6720 attempts closed; 5585 valid, 634 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 228 | 43/228 (18.9%) | 198/228 (86.8%) | 102/171 (59.6%) | 75/103 (72.8%) | 107 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 215 | 2/215 (0.9%) | 169/215 (78.6%) | 117/161 (72.7%) | 87/132 (65.9%) | 144 / 78 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 212 | 22/212 (10.4%) | 194/212 (91.5%) | 98/156 (62.8%) | 81/100 (81.0%) | 104 / 0 |
| claude-code | glm-5.2 | sail_v3 | 200 | 5/200 (2.5%) | 165/200 (82.5%) | 101/145 (69.7%) | 77/113 (68.1%) | 115 / 69 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 168 | 22/168 (13.1%) | 154/168 (91.7%) | 58/126 (46.0%) | 44/58 (75.9%) | 59 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 159 | 2/159 (1.3%) | 132/159 (83.0%) | 73/123 (59.3%) | 52/77 (67.5%) | 66 / 40 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 222 | 35/222 (15.8%) | 201/222 (90.5%) | 75/166 (45.2%) | 55/76 (72.4%) | 89 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 199 | 4/199 (2.0%) | 166/199 (83.4%) | 95/143 (66.4%) | 70/111 (63.1%) | 101 / 103 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 203 | 21/203 (10.3%) | 184/203 (90.6%) | 64/145 (44.1%) | 55/64 (85.9%) | 67 / 0 |
| codex | glm-5.2 | sail_v3 | 170 | 1/170 (0.6%) | 154/170 (90.6%) | 77/117 (65.8%) | 66/88 (75.0%) | 62 / 55 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 189 | 24/189 (12.7%) | 162/189 (85.7%) | 54/139 (38.8%) | 44/54 (81.5%) | 97 / 0 |
| codex | qwen3.7-max | sail_v3 | 161 | 2/161 (1.2%) | 126/161 (78.3%) | 72/117 (61.5%) | 49/78 (62.8%) | 97 / 68 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 222 | 28/222 (12.6%) | 196/222 (88.3%) | 99/164 (60.4%) | 69/100 (69.0%) | 111 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 202 | 5/202 (2.5%) | 169/202 (83.7%) | 101/148 (68.2%) | 81/117 (69.2%) | 121 / 77 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 183 | 23/183 (12.6%) | 172/183 (94.0%) | 72/133 (54.1%) | 64/72 (88.9%) | 72 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 165 | 3/165 (1.8%) | 148/165 (89.7%) | 70/112 (62.5%) | 60/76 (78.9%) | 64 / 31 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 200 | 28/200 (14.0%) | 179/200 (89.5%) | 56/146 (38.4%) | 44/56 (78.6%) | 58 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 179 | 5/179 (2.8%) | 157/179 (87.7%) | 66/130 (50.8%) | 51/75 (68.0%) | 50 / 50 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 213 | 33/213 (15.5%) | 192/213 (90.1%) | 85/162 (52.5%) | 68/85 (80.0%) | 87 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 193 | 1/193 (0.5%) | 165/193 (85.5%) | 102/149 (68.5%) | 77/111 (69.4%) | 118 / 84 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 217 | 25/217 (11.5%) | 208/217 (95.9%) | 93/161 (57.8%) | 77/93 (82.8%) | 95 / 0 |
| hermes | glm-5.2 | sail_v3 | 192 | 4/192 (2.1%) | 168/192 (87.5%) | 107/142 (75.4%) | 85/118 (72.0%) | 110 / 104 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 210 | 24/210 (11.4%) | 174/210 (82.9%) | 60/156 (38.5%) | 50/61 (82.0%) | 61 / 0 |
| hermes | qwen3.7-max | sail_v3 | 205 | 3/205 (1.5%) | 153/205 (74.6%) | 79/154 (51.3%) | 50/82 (61.0%) | 58 / 37 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
