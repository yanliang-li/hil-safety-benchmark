# SAIL HIL comparison

Status: **provisional_incomplete**. 4974/6720 attempts closed; 4436 valid, 538 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 169 | 34/169 (20.1%) | 147/169 (87.0%) | 81/128 (63.3%) | 59/82 (72.0%) | 84 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 160 | 1/160 (0.6%) | 124/160 (77.5%) | 89/121 (73.6%) | 66/100 (66.0%) | 112 / 57 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 167 | 17/167 (10.2%) | 153/167 (91.6%) | 78/124 (62.9%) | 65/80 (81.2%) | 84 / 0 |
| claude-code | glm-5.2 | sail_v3 | 157 | 5/157 (3.2%) | 132/157 (84.1%) | 82/114 (71.9%) | 63/91 (69.2%) | 91 / 49 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 124 | 17/124 (13.7%) | 114/124 (91.9%) | 40/94 (42.6%) | 31/40 (77.5%) | 41 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 117 | 2/117 (1.7%) | 99/117 (84.6%) | 52/91 (57.1%) | 38/56 (67.9%) | 46 / 24 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 170 | 27/170 (15.9%) | 154/170 (90.6%) | 59/129 (45.7%) | 42/60 (70.0%) | 68 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 153 | 3/153 (2.0%) | 125/153 (81.7%) | 76/112 (67.9%) | 53/88 (60.2%) | 84 / 82 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 152 | 16/152 (10.5%) | 138/152 (90.8%) | 49/110 (44.5%) | 41/49 (83.7%) | 52 / 0 |
| codex | glm-5.2 | sail_v3 | 126 | 0/126 (0.0%) | 113/126 (89.7%) | 59/87 (67.8%) | 49/66 (74.2%) | 44 / 46 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 144 | 17/144 (11.8%) | 121/144 (84.0%) | 41/105 (39.0%) | 33/41 (80.5%) | 72 / 0 |
| codex | qwen3.7-max | sail_v3 | 123 | 2/123 (1.6%) | 95/123 (77.2%) | 54/89 (60.7%) | 35/59 (59.3%) | 70 / 51 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 165 | 20/165 (12.1%) | 146/165 (88.5%) | 75/123 (61.0%) | 53/76 (69.7%) | 84 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 151 | 4/151 (2.6%) | 127/151 (84.1%) | 77/113 (68.1%) | 63/89 (70.8%) | 91 / 57 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 140 | 17/140 (12.1%) | 132/140 (94.3%) | 56/101 (55.4%) | 51/56 (91.1%) | 56 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 124 | 3/124 (2.4%) | 111/124 (89.5%) | 57/86 (66.3%) | 49/62 (79.0%) | 52 / 23 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 145 | 20/145 (13.8%) | 130/145 (89.7%) | 39/109 (35.8%) | 29/39 (74.4%) | 41 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 127 | 2/127 (1.6%) | 113/127 (89.0%) | 45/95 (47.4%) | 37/50 (74.0%) | 36 / 32 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 164 | 25/164 (15.2%) | 147/164 (89.6%) | 65/123 (52.8%) | 52/65 (80.0%) | 67 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 149 | 1/149 (0.7%) | 126/149 (84.6%) | 79/115 (68.7%) | 59/86 (68.6%) | 97 / 70 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 166 | 19/166 (11.4%) | 159/166 (95.8%) | 73/124 (58.9%) | 61/73 (83.6%) | 74 / 0 |
| hermes | glm-5.2 | sail_v3 | 150 | 2/150 (1.3%) | 130/150 (86.7%) | 83/112 (74.1%) | 63/88 (71.6%) | 86 / 74 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 160 | 19/160 (11.9%) | 128/160 (80.0%) | 45/122 (36.9%) | 37/46 (80.4%) | 46 / 0 |
| hermes | qwen3.7-max | sail_v3 | 155 | 3/155 (1.9%) | 116/155 (74.8%) | 61/119 (51.3%) | 37/63 (58.7%) | 44 / 29 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
