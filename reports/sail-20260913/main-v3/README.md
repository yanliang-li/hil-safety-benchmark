# SAIL HIL comparison

Status: **provisional_incomplete**. 3730/6720 attempts closed; 3364 valid, 366 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 114 | 20/114 (17.5%) | 98/114 (86.0%) | 54/88 (61.4%) | 43/55 (78.2%) | 55 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 109 | 1/109 (0.9%) | 81/109 (74.3%) | 61/85 (71.8%) | 41/68 (60.3%) | 78 / 39 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 129 | 14/129 (10.9%) | 117/129 (90.7%) | 62/99 (62.6%) | 50/64 (78.1%) | 67 / 0 |
| claude-code | glm-5.2 | sail_v3 | 120 | 5/120 (4.2%) | 100/120 (83.3%) | 65/90 (72.2%) | 51/73 (69.9%) | 70 / 37 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 91 | 14/91 (15.4%) | 84/91 (92.3%) | 29/68 (42.6%) | 23/29 (79.3%) | 30 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 87 | 2/87 (2.3%) | 76/87 (87.4%) | 38/68 (55.9%) | 30/42 (71.4%) | 33 / 18 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 114 | 23/114 (20.2%) | 105/114 (92.1%) | 37/82 (45.1%) | 25/37 (67.6%) | 42 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 102 | 2/102 (2.0%) | 84/102 (82.4%) | 47/70 (67.1%) | 37/57 (64.9%) | 52 / 53 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 110 | 10/110 (9.1%) | 100/110 (90.9%) | 35/78 (44.9%) | 29/35 (82.9%) | 36 / 0 |
| codex | glm-5.2 | sail_v3 | 92 | 0/92 (0.0%) | 82/92 (89.1%) | 42/62 (67.7%) | 34/47 (72.3%) | 30 / 37 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 100 | 12/100 (12.0%) | 90/100 (90.0%) | 29/72 (40.3%) | 23/29 (79.3%) | 51 / 0 |
| codex | qwen3.7-max | sail_v3 | 83 | 0/83 (0.0%) | 67/83 (80.7%) | 34/58 (58.6%) | 24/37 (64.9%) | 44 / 35 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 117 | 14/117 (12.0%) | 106/117 (90.6%) | 49/87 (56.3%) | 37/49 (75.5%) | 56 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 108 | 2/108 (1.9%) | 93/108 (86.1%) | 55/81 (67.9%) | 47/64 (73.4%) | 64 / 37 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 92 | 12/92 (13.0%) | 87/92 (94.6%) | 33/65 (50.8%) | 31/33 (93.9%) | 33 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 79 | 2/79 (2.5%) | 73/79 (92.4%) | 32/53 (60.4%) | 30/36 (83.3%) | 29 / 16 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 98 | 13/98 (13.3%) | 86/98 (87.8%) | 30/75 (40.0%) | 22/30 (73.3%) | 31 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 92 | 2/92 (2.2%) | 82/92 (89.1%) | 33/67 (49.3%) | 27/37 (73.0%) | 27 / 25 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 113 | 16/113 (14.2%) | 103/113 (91.2%) | 41/83 (49.4%) | 33/41 (80.5%) | 43 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 103 | 0/103 (0.0%) | 86/103 (83.5%) | 51/78 (65.4%) | 39/56 (69.6%) | 59 / 42 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 113 | 14/113 (12.4%) | 107/113 (94.7%) | 56/85 (65.9%) | 46/56 (82.1%) | 57 / 0 |
| hermes | glm-5.2 | sail_v3 | 104 | 1/104 (1.0%) | 88/104 (84.6%) | 60/80 (75.0%) | 42/62 (67.7%) | 62 / 59 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 111 | 13/111 (11.7%) | 91/111 (82.0%) | 35/86 (40.7%) | 28/35 (80.0%) | 35 / 0 |
| hermes | qwen3.7-max | sail_v3 | 105 | 2/105 (1.9%) | 80/105 (76.2%) | 44/83 (53.0%) | 27/46 (58.7%) | 36 / 18 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
