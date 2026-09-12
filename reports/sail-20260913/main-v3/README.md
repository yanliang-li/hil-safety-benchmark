# SAIL HIL comparison

Status: **provisional_incomplete**. 4730/6720 attempts closed; 4201 valid, 529 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 158 | 30/158 (19.0%) | 139/158 (88.0%) | 74/120 (61.7%) | 57/75 (76.0%) | 76 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 150 | 1/150 (0.7%) | 117/150 (78.0%) | 82/114 (71.9%) | 61/92 (66.3%) | 102 / 51 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 158 | 17/158 (10.8%) | 144/158 (91.1%) | 73/119 (61.3%) | 60/75 (80.0%) | 79 / 0 |
| claude-code | glm-5.2 | sail_v3 | 147 | 5/147 (3.4%) | 123/147 (83.7%) | 76/108 (70.4%) | 59/85 (69.4%) | 83 / 46 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 115 | 15/115 (13.0%) | 105/115 (91.3%) | 36/86 (41.9%) | 29/36 (80.6%) | 37 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 109 | 2/109 (1.8%) | 92/109 (84.4%) | 48/84 (57.1%) | 35/52 (67.3%) | 42 / 22 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 158 | 25/158 (15.8%) | 143/158 (90.5%) | 53/118 (44.9%) | 36/53 (67.9%) | 61 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 141 | 3/141 (2.1%) | 115/141 (81.6%) | 67/101 (66.3%) | 49/79 (62.0%) | 72 / 77 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 144 | 16/144 (11.1%) | 131/144 (91.0%) | 46/105 (43.8%) | 39/46 (84.8%) | 48 / 0 |
| codex | glm-5.2 | sail_v3 | 118 | 0/118 (0.0%) | 106/118 (89.8%) | 55/82 (67.1%) | 46/62 (74.2%) | 41 / 44 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 127 | 14/127 (11.0%) | 104/127 (81.9%) | 33/91 (36.3%) | 26/33 (78.8%) | 58 / 0 |
| codex | qwen3.7-max | sail_v3 | 106 | 0/106 (0.0%) | 80/106 (75.5%) | 42/75 (56.0%) | 28/46 (60.9%) | 49 / 44 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 159 | 20/159 (12.6%) | 141/159 (88.7%) | 73/119 (61.3%) | 52/74 (70.3%) | 82 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 145 | 4/145 (2.8%) | 123/145 (84.8%) | 75/109 (68.8%) | 62/87 (71.3%) | 88 / 55 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 133 | 16/133 (12.0%) | 126/133 (94.7%) | 51/95 (53.7%) | 47/51 (92.2%) | 51 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 119 | 3/119 (2.5%) | 107/119 (89.9%) | 53/82 (64.6%) | 46/58 (79.3%) | 48 / 21 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 137 | 19/137 (13.9%) | 123/137 (89.8%) | 37/102 (36.3%) | 28/37 (75.7%) | 39 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 121 | 2/121 (1.7%) | 107/121 (88.4%) | 43/90 (47.8%) | 35/48 (72.9%) | 35 / 31 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 156 | 25/156 (16.0%) | 141/156 (90.4%) | 59/117 (50.4%) | 48/59 (81.4%) | 61 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 140 | 1/140 (0.7%) | 119/140 (85.0%) | 74/108 (68.5%) | 56/81 (69.1%) | 90 / 65 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 155 | 19/155 (12.3%) | 148/155 (95.5%) | 72/117 (61.5%) | 60/72 (83.3%) | 73 / 0 |
| hermes | glm-5.2 | sail_v3 | 139 | 2/139 (1.4%) | 119/139 (85.6%) | 81/105 (77.1%) | 61/86 (70.9%) | 84 / 73 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 147 | 17/147 (11.6%) | 115/147 (78.2%) | 43/111 (38.7%) | 35/44 (79.5%) | 44 / 0 |
| hermes | qwen3.7-max | sail_v3 | 141 | 2/141 (1.4%) | 104/141 (73.8%) | 55/108 (50.9%) | 34/57 (59.6%) | 42 / 25 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
