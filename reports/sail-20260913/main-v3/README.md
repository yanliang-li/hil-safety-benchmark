# SAIL HIL comparison

Status: **provisional_incomplete**. 4478/6720 attempts closed; 3981 valid, 497 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 146 | 27/146 (18.5%) | 128/146 (87.7%) | 67/111 (60.4%) | 54/68 (79.4%) | 68 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 139 | 1/139 (0.7%) | 109/139 (78.4%) | 74/106 (69.8%) | 55/83 (66.3%) | 91 / 47 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 153 | 17/153 (11.1%) | 140/153 (91.5%) | 69/115 (60.0%) | 57/71 (80.3%) | 75 / 0 |
| claude-code | glm-5.2 | sail_v3 | 142 | 5/142 (3.5%) | 120/142 (84.5%) | 73/104 (70.2%) | 58/82 (70.7%) | 78 / 44 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 107 | 15/107 (14.0%) | 97/107 (90.7%) | 33/79 (41.8%) | 27/33 (81.8%) | 34 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 102 | 2/102 (2.0%) | 87/102 (85.3%) | 46/79 (58.2%) | 35/50 (70.0%) | 40 / 20 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 147 | 24/147 (16.3%) | 135/147 (91.8%) | 48/109 (44.0%) | 34/48 (70.8%) | 54 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 131 | 2/131 (1.5%) | 107/131 (81.7%) | 60/93 (64.5%) | 44/71 (62.0%) | 64 / 71 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 132 | 13/132 (9.8%) | 119/132 (90.2%) | 41/97 (42.3%) | 34/41 (82.9%) | 43 / 0 |
| codex | glm-5.2 | sail_v3 | 109 | 0/109 (0.0%) | 98/109 (89.9%) | 50/77 (64.9%) | 42/56 (75.0%) | 37 / 39 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 121 | 13/121 (10.7%) | 101/121 (83.5%) | 32/87 (36.8%) | 26/32 (81.2%) | 55 / 0 |
| codex | qwen3.7-max | sail_v3 | 99 | 0/99 (0.0%) | 78/99 (78.8%) | 40/70 (57.1%) | 27/43 (62.8%) | 47 / 38 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 150 | 19/150 (12.7%) | 133/150 (88.7%) | 66/111 (59.5%) | 46/67 (68.7%) | 75 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 138 | 4/138 (2.9%) | 117/138 (84.8%) | 69/103 (67.0%) | 57/81 (70.4%) | 82 / 52 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 120 | 15/120 (12.5%) | 114/120 (95.0%) | 43/85 (50.6%) | 40/43 (93.0%) | 43 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 107 | 3/107 (2.8%) | 98/107 (91.6%) | 43/72 (59.7%) | 40/48 (83.3%) | 38 / 19 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 129 | 19/129 (14.7%) | 115/129 (89.1%) | 36/97 (37.1%) | 27/36 (75.0%) | 38 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 115 | 2/115 (1.7%) | 102/115 (88.7%) | 40/86 (46.5%) | 33/45 (73.3%) | 33 / 30 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 144 | 21/144 (14.6%) | 130/144 (90.3%) | 54/106 (50.9%) | 45/54 (83.3%) | 56 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 130 | 0/130 (0.0%) | 110/130 (84.6%) | 67/99 (67.7%) | 51/74 (68.9%) | 82 / 57 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 146 | 18/146 (12.3%) | 139/146 (95.2%) | 68/110 (61.8%) | 57/68 (83.8%) | 69 / 0 |
| hermes | glm-5.2 | sail_v3 | 130 | 1/130 (0.8%) | 110/130 (84.6%) | 77/98 (78.6%) | 57/81 (70.4%) | 80 / 67 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 136 | 15/136 (11.0%) | 105/136 (77.2%) | 38/103 (36.9%) | 29/38 (76.3%) | 38 / 0 |
| hermes | qwen3.7-max | sail_v3 | 130 | 2/130 (1.5%) | 97/130 (74.6%) | 51/99 (51.5%) | 31/53 (58.5%) | 38 / 24 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
