# SAIL HIL comparison

Status: **provisional_incomplete**. 3246/6720 attempts closed; 2944 valid, 302 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 95 | 18/95 (18.9%) | 84/95 (88.4%) | 48/74 (64.9%) | 39/49 (79.6%) | 49 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 91 | 1/91 (1.1%) | 71/91 (78.0%) | 54/71 (76.1%) | 38/59 (64.4%) | 68 / 30 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 102 | 11/102 (10.8%) | 92/102 (90.2%) | 48/76 (63.2%) | 40/50 (80.0%) | 53 / 0 |
| claude-code | glm-5.2 | sail_v3 | 96 | 4/96 (4.2%) | 80/96 (83.3%) | 49/70 (70.0%) | 39/57 (68.4%) | 53 / 30 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 77 | 12/77 (15.6%) | 72/77 (93.5%) | 25/60 (41.7%) | 20/25 (80.0%) | 26 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 74 | 1/74 (1.4%) | 65/74 (87.8%) | 34/59 (57.6%) | 27/37 (73.0%) | 29 / 17 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 93 | 17/93 (18.3%) | 86/93 (92.5%) | 30/68 (44.1%) | 23/30 (76.7%) | 35 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 84 | 2/84 (2.4%) | 69/84 (82.1%) | 39/59 (66.1%) | 31/48 (64.6%) | 43 / 41 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 87 | 7/87 (8.0%) | 78/87 (89.7%) | 29/64 (45.3%) | 25/29 (86.2%) | 30 / 0 |
| codex | glm-5.2 | sail_v3 | 74 | 0/74 (0.0%) | 66/74 (89.2%) | 35/52 (67.3%) | 28/38 (73.7%) | 24 / 28 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 87 | 11/87 (12.6%) | 82/87 (94.3%) | 27/60 (45.0%) | 22/27 (81.5%) | 48 / 0 |
| codex | qwen3.7-max | sail_v3 | 73 | 0/73 (0.0%) | 59/73 (80.8%) | 31/49 (63.3%) | 22/34 (64.7%) | 38 / 30 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 100 | 10/100 (10.0%) | 90/100 (90.0%) | 42/74 (56.8%) | 31/42 (73.8%) | 48 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 91 | 2/91 (2.2%) | 77/91 (84.6%) | 46/69 (66.7%) | 36/52 (69.2%) | 52 / 29 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 75 | 8/75 (10.7%) | 70/75 (93.3%) | 29/53 (54.7%) | 27/29 (93.1%) | 29 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 62 | 2/62 (3.2%) | 57/62 (91.9%) | 26/41 (63.4%) | 24/29 (82.8%) | 25 / 8 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 80 | 10/80 (12.5%) | 71/80 (88.8%) | 26/59 (44.1%) | 19/26 (73.1%) | 27 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 78 | 2/78 (2.6%) | 68/78 (87.2%) | 27/56 (48.2%) | 20/30 (66.7%) | 22 / 23 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 94 | 13/94 (13.8%) | 85/94 (90.4%) | 36/67 (53.7%) | 28/36 (77.8%) | 38 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 85 | 0/85 (0.0%) | 71/85 (83.5%) | 42/62 (67.7%) | 31/47 (66.0%) | 52 / 37 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 100 | 12/100 (12.0%) | 94/100 (94.0%) | 50/74 (67.6%) | 41/50 (82.0%) | 50 / 0 |
| hermes | glm-5.2 | sail_v3 | 91 | 1/91 (1.1%) | 76/91 (83.5%) | 52/68 (76.5%) | 37/54 (68.5%) | 55 / 52 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 91 | 11/91 (12.1%) | 77/91 (84.6%) | 28/70 (40.0%) | 22/28 (78.6%) | 28 / 0 |
| hermes | qwen3.7-max | sail_v3 | 86 | 2/86 (2.3%) | 66/86 (76.7%) | 36/66 (54.5%) | 22/38 (57.9%) | 28 / 16 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
