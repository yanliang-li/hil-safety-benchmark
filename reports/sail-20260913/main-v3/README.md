# SAIL HIL comparison

Status: **provisional_incomplete**. 2496/6720 attempts closed; 2253 valid, 243 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 67 | 14/67 (20.9%) | 58/67 (86.6%) | 31/49 (63.3%) | 24/32 (75.0%) | 32 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 65 | 1/65 (1.5%) | 49/65 (75.4%) | 36/48 (75.0%) | 23/40 (57.5%) | 44 / 24 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 66 | 0/66 (0.0%) | 53/66 (80.3%) | 0/48 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 67 | 6/67 (9.0%) | 61/67 (91.0%) | 33/51 (64.7%) | 26/33 (78.8%) | 36 / 0 |
| claude-code | glm-5.2 | sail_v3 | 64 | 2/64 (3.1%) | 56/64 (87.5%) | 32/48 (66.7%) | 26/34 (76.5%) | 30 / 13 |
| claude-code | glm-5.2 | sail_v3_no_human | 65 | 0/65 (0.0%) | 57/65 (87.7%) | 0/49 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 55 | 9/55 (16.4%) | 50/55 (90.9%) | 17/43 (39.5%) | 12/17 (70.6%) | 18 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 53 | 1/53 (1.9%) | 44/53 (83.0%) | 25/43 (58.1%) | 17/27 (63.0%) | 21 / 13 |
| claude-code | qwen3.7-max | sail_v3_no_human | 53 | 0/53 (0.0%) | 46/53 (86.8%) | 0/39 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 73 | 13/73 (17.8%) | 66/73 (90.4%) | 24/54 (44.4%) | 17/24 (70.8%) | 29 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 67 | 2/67 (3.0%) | 54/67 (80.6%) | 32/48 (66.7%) | 23/38 (60.5%) | 35 / 32 |
| codex | deepseek-v4-flash | sail_v3_no_human | 71 | 0/71 (0.0%) | 55/71 (77.5%) | 0/52 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 65 | 7/65 (10.8%) | 57/65 (87.7%) | 20/46 (43.5%) | 16/20 (80.0%) | 21 / 0 |
| codex | glm-5.2 | sail_v3 | 56 | 0/56 (0.0%) | 48/56 (85.7%) | 27/38 (71.1%) | 21/30 (70.0%) | 18 / 23 |
| codex | glm-5.2 | sail_v3_no_human | 57 | 0/57 (0.0%) | 51/57 (89.5%) | 0/38 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 60 | 8/60 (13.3%) | 55/60 (91.7%) | 18/43 (41.9%) | 15/18 (83.3%) | 33 / 0 |
| codex | qwen3.7-max | sail_v3 | 49 | 0/49 (0.0%) | 38/49 (77.6%) | 18/34 (52.9%) | 13/21 (61.9%) | 23 / 18 |
| codex | qwen3.7-max | sail_v3_no_human | 64 | 1/64 (1.6%) | 51/64 (79.7%) | 0/46 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 70 | 8/70 (11.4%) | 63/70 (90.0%) | 28/53 (52.8%) | 20/28 (71.4%) | 31 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 62 | 2/62 (3.2%) | 53/62 (85.5%) | 30/48 (62.5%) | 23/34 (67.6%) | 33 / 17 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 70 | 0/70 (0.0%) | 57/70 (81.4%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 60 | 7/60 (11.7%) | 56/60 (93.3%) | 24/42 (57.1%) | 23/24 (95.8%) | 24 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 54 | 2/54 (3.7%) | 50/54 (92.6%) | 25/37 (67.6%) | 23/28 (82.1%) | 24 / 8 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 59 | 0/59 (0.0%) | 51/59 (86.4%) | 0/43 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 59 | 8/59 (13.6%) | 52/59 (88.1%) | 17/44 (38.6%) | 11/17 (64.7%) | 18 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 59 | 2/59 (3.4%) | 52/59 (88.1%) | 18/42 (42.9%) | 14/21 (66.7%) | 14 / 17 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 63 | 0/63 (0.0%) | 49/63 (77.8%) | 0/46 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 67 | 11/67 (16.4%) | 62/67 (92.5%) | 24/49 (49.0%) | 19/24 (79.2%) | 26 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 62 | 0/62 (0.0%) | 52/62 (83.9%) | 33/47 (70.2%) | 24/36 (66.7%) | 37 / 28 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 66 | 0/66 (0.0%) | 56/66 (84.8%) | 0/48 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 65 | 9/65 (13.8%) | 62/65 (95.4%) | 32/52 (61.5%) | 26/32 (81.2%) | 32 / 0 |
| hermes | glm-5.2 | sail_v3 | 62 | 1/62 (1.6%) | 52/62 (83.9%) | 36/49 (73.5%) | 25/37 (67.6%) | 38 / 35 |
| hermes | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 52/62 (83.9%) | 0/49 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 66 | 7/66 (10.6%) | 57/66 (86.4%) | 20/50 (40.0%) | 18/20 (90.0%) | 20 / 0 |
| hermes | qwen3.7-max | sail_v3 | 62 | 2/62 (3.2%) | 47/62 (75.8%) | 26/46 (56.5%) | 17/28 (60.7%) | 19 / 12 |
| hermes | qwen3.7-max | sail_v3_no_human | 68 | 0/68 (0.0%) | 51/68 (75.0%) | 0/51 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
