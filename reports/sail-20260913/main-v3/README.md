# SAIL HIL comparison

Status: **provisional_incomplete**. 1250/6720 attempts closed; 1123 valid, 127 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 32 | 6/32 (18.8%) | 27/32 (84.4%) | 19/25 (76.0%) | 15/20 (75.0%) | 20 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 31 | 1/31 (3.2%) | 21/31 (67.7%) | 19/25 (76.0%) | 10/20 (50.0%) | 27 / 9 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 31 | 0/31 (0.0%) | 24/31 (77.4%) | 0/24 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 35 | 2/35 (5.7%) | 32/35 (91.4%) | 16/25 (64.0%) | 13/16 (81.2%) | 18 / 0 |
| claude-code | glm-5.2 | sail_v3 | 34 | 0/34 (0.0%) | 29/34 (85.3%) | 16/24 (66.7%) | 14/16 (87.5%) | 15 / 4 |
| claude-code | glm-5.2 | sail_v3_no_human | 33 | 0/33 (0.0%) | 30/33 (90.9%) | 0/24 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 25 | 4/25 (16.0%) | 22/25 (88.0%) | 9/19 (47.4%) | 5/9 (55.6%) | 10 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 23 | 1/23 (4.3%) | 17/23 (73.9%) | 13/18 (72.2%) | 7/15 (46.7%) | 12 / 9 |
| claude-code | qwen3.7-max | sail_v3_no_human | 23 | 0/23 (0.0%) | 19/23 (82.6%) | 0/17 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 36 | 5/36 (13.9%) | 31/36 (86.1%) | 15/25 (60.0%) | 10/15 (66.7%) | 18 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 31 | 1/31 (3.2%) | 22/31 (71.0%) | 14/21 (66.7%) | 9/18 (50.0%) | 18 / 19 |
| codex | deepseek-v4-flash | sail_v3_no_human | 35 | 0/35 (0.0%) | 25/35 (71.4%) | 0/25 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 28 | 3/28 (10.7%) | 23/28 (82.1%) | 10/22 (45.5%) | 6/10 (60.0%) | 10 / 0 |
| codex | glm-5.2 | sail_v3 | 25 | 0/25 (0.0%) | 22/25 (88.0%) | 14/20 (70.0%) | 11/15 (73.3%) | 8 / 12 |
| codex | glm-5.2 | sail_v3_no_human | 25 | 0/25 (0.0%) | 23/25 (92.0%) | 0/19 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 25 | 4/25 (16.0%) | 22/25 (88.0%) | 6/16 (37.5%) | 4/6 (66.7%) | 10 / 0 |
| codex | qwen3.7-max | sail_v3 | 22 | 0/22 (0.0%) | 17/22 (77.3%) | 8/15 (53.3%) | 6/9 (66.7%) | 10 / 5 |
| codex | qwen3.7-max | sail_v3_no_human | 29 | 1/29 (3.4%) | 23/29 (79.3%) | 0/19 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 37 | 6/37 (16.2%) | 33/37 (89.2%) | 11/24 (45.8%) | 7/11 (63.6%) | 11 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 33 | 1/33 (3.0%) | 28/33 (84.8%) | 14/22 (63.6%) | 12/18 (66.7%) | 12 / 11 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 37 | 0/37 (0.0%) | 30/37 (81.1%) | 0/24 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 31 | 4/31 (12.9%) | 30/31 (96.8%) | 10/21 (47.6%) | 10/10 (100.0%) | 10 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 29 | 1/29 (3.4%) | 27/29 (93.1%) | 11/19 (57.9%) | 10/13 (76.9%) | 10 / 6 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 35 | 0/35 (0.0%) | 31/35 (88.6%) | 0/25 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 33 | 3/33 (9.1%) | 28/33 (84.8%) | 12/25 (48.0%) | 8/12 (66.7%) | 13 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 34 | 2/34 (5.9%) | 31/34 (91.2%) | 11/25 (44.0%) | 8/13 (61.5%) | 9 / 9 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 36 | 0/36 (0.0%) | 28/36 (77.8%) | 0/27 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 36 | 5/36 (13.9%) | 33/36 (91.7%) | 17/29 (58.6%) | 14/17 (82.4%) | 18 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 32 | 0/32 (0.0%) | 26/32 (81.2%) | 22/27 (81.5%) | 17/23 (73.9%) | 25 / 16 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 35 | 0/35 (0.0%) | 29/35 (82.9%) | 0/28 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 36 | 6/36 (16.7%) | 35/36 (97.2%) | 19/27 (70.4%) | 16/19 (84.2%) | 19 / 0 |
| hermes | glm-5.2 | sail_v3 | 34 | 1/34 (2.9%) | 29/34 (85.3%) | 22/25 (88.0%) | 15/22 (68.2%) | 23 / 18 |
| hermes | glm-5.2 | sail_v3_no_human | 34 | 0/34 (0.0%) | 30/34 (88.2%) | 0/25 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 29 | 4/29 (13.8%) | 24/29 (82.8%) | 9/22 (40.9%) | 8/9 (88.9%) | 9 / 0 |
| hermes | qwen3.7-max | sail_v3 | 28 | 2/28 (7.1%) | 21/28 (75.0%) | 11/21 (52.4%) | 8/12 (66.7%) | 9 / 5 |
| hermes | qwen3.7-max | sail_v3_no_human | 31 | 0/31 (0.0%) | 22/31 (71.0%) | 0/23 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
