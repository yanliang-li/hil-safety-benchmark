# SAIL HIL comparison

Status: **provisional_incomplete**. 1007/6720 attempts closed; 898 valid, 109 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 26 | 5/26 (19.2%) | 22/26 (84.6%) | 15/20 (75.0%) | 12/16 (75.0%) | 16 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 25 | 1/25 (4.0%) | 16/25 (64.0%) | 16/20 (80.0%) | 8/17 (47.1%) | 20 / 7 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 25 | 0/25 (0.0%) | 19/25 (76.0%) | 0/19 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 30 | 2/30 (6.7%) | 27/30 (90.0%) | 15/23 (65.2%) | 12/15 (80.0%) | 17 / 0 |
| claude-code | glm-5.2 | sail_v3 | 29 | 0/29 (0.0%) | 24/29 (82.8%) | 15/22 (68.2%) | 13/15 (86.7%) | 14 / 3 |
| claude-code | glm-5.2 | sail_v3_no_human | 28 | 0/28 (0.0%) | 26/28 (92.9%) | 0/21 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 24 | 4/24 (16.7%) | 21/24 (87.5%) | 9/18 (50.0%) | 5/9 (55.6%) | 9 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 22 | 1/22 (4.5%) | 17/22 (77.3%) | 13/18 (72.2%) | 7/14 (50.0%) | 12 / 8 |
| claude-code | qwen3.7-max | sail_v3_no_human | 23 | 0/23 (0.0%) | 19/23 (82.6%) | 0/17 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 25 | 2/25 (8.0%) | 20/25 (80.0%) | 11/20 (55.0%) | 6/11 (54.5%) | 14 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 21 | 1/21 (4.8%) | 16/21 (76.2%) | 10/16 (62.5%) | 6/12 (50.0%) | 13 / 11 |
| codex | deepseek-v4-flash | sail_v3_no_human | 24 | 0/24 (0.0%) | 17/24 (70.8%) | 0/19 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 21 | 3/21 (14.3%) | 16/21 (76.2%) | 7/15 (46.7%) | 4/7 (57.1%) | 7 / 0 |
| codex | glm-5.2 | sail_v3 | 19 | 0/19 (0.0%) | 17/19 (89.5%) | 12/14 (85.7%) | 10/13 (76.9%) | 6 / 12 |
| codex | glm-5.2 | sail_v3_no_human | 19 | 0/19 (0.0%) | 17/19 (89.5%) | 0/13 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 21 | 3/21 (14.3%) | 18/21 (85.7%) | 4/13 (30.8%) | 2/4 (50.0%) | 6 / 0 |
| codex | qwen3.7-max | sail_v3 | 18 | 0/18 (0.0%) | 14/18 (77.8%) | 5/11 (45.5%) | 3/6 (50.0%) | 5 / 4 |
| codex | qwen3.7-max | sail_v3_no_human | 25 | 1/25 (4.0%) | 20/25 (80.0%) | 0/16 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 28 | 5/28 (17.9%) | 26/28 (92.9%) | 7/17 (41.2%) | 5/7 (71.4%) | 7 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 25 | 1/25 (4.0%) | 21/25 (84.0%) | 9/16 (56.2%) | 8/12 (66.7%) | 8 / 9 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 28 | 0/28 (0.0%) | 23/28 (82.1%) | 0/17 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 19 | 1/19 (5.3%) | 19/19 (100.0%) | 7/13 (53.8%) | 7/7 (100.0%) | 7 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 17 | 0/17 (0.0%) | 16/17 (94.1%) | 8/11 (72.7%) | 7/9 (77.8%) | 7 / 4 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 20 | 0/20 (0.0%) | 18/20 (90.0%) | 0/14 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 29 | 3/29 (10.3%) | 25/29 (86.2%) | 12/22 (54.5%) | 8/12 (66.7%) | 13 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 31 | 2/31 (6.5%) | 28/31 (90.3%) | 11/23 (47.8%) | 8/13 (61.5%) | 9 / 9 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 32 | 0/32 (0.0%) | 25/32 (78.1%) | 0/24 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 33 | 4/33 (12.1%) | 30/33 (90.9%) | 16/26 (61.5%) | 13/16 (81.2%) | 16 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 29 | 0/29 (0.0%) | 24/29 (82.8%) | 20/24 (83.3%) | 16/21 (76.2%) | 22 / 14 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 32 | 0/32 (0.0%) | 27/32 (84.4%) | 0/25 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 26 | 4/26 (15.4%) | 26/26 (100.0%) | 14/19 (73.7%) | 11/14 (78.6%) | 14 / 0 |
| hermes | glm-5.2 | sail_v3 | 24 | 1/24 (4.2%) | 21/24 (87.5%) | 15/17 (88.2%) | 10/15 (66.7%) | 16 / 15 |
| hermes | glm-5.2 | sail_v3_no_human | 24 | 0/24 (0.0%) | 21/24 (87.5%) | 0/17 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 25 | 4/25 (16.0%) | 21/25 (84.0%) | 7/18 (38.9%) | 6/7 (85.7%) | 7 / 0 |
| hermes | qwen3.7-max | sail_v3 | 25 | 2/25 (8.0%) | 19/25 (76.0%) | 10/18 (55.6%) | 7/11 (63.6%) | 8 / 5 |
| hermes | qwen3.7-max | sail_v3_no_human | 26 | 0/26 (0.0%) | 18/26 (69.2%) | 0/18 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
