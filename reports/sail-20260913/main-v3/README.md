# SAIL HIL comparison

Status: **provisional_incomplete**. 763/6720 attempts closed; 680 valid, 83 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 19 | 3/19 (15.8%) | 17/19 (89.5%) | 11/15 (73.3%) | 10/11 (90.9%) | 11 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 18 | 0/18 (0.0%) | 12/18 (66.7%) | 13/15 (86.7%) | 7/13 (53.8%) | 16 / 5 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 18 | 0/18 (0.0%) | 14/18 (77.8%) | 0/14 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 23 | 2/23 (8.7%) | 22/23 (95.7%) | 9/16 (56.2%) | 9/9 (100.0%) | 11 / 0 |
| claude-code | glm-5.2 | sail_v3 | 22 | 0/22 (0.0%) | 21/22 (95.5%) | 10/15 (66.7%) | 10/10 (100.0%) | 9 / 2 |
| claude-code | glm-5.2 | sail_v3_no_human | 22 | 0/22 (0.0%) | 22/22 (100.0%) | 0/15 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 21 | 4/21 (19.0%) | 18/21 (85.7%) | 7/15 (46.7%) | 3/7 (42.9%) | 7 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 18 | 1/18 (5.6%) | 14/18 (77.8%) | 9/14 (64.3%) | 5/10 (50.0%) | 8 / 6 |
| claude-code | qwen3.7-max | sail_v3_no_human | 20 | 0/20 (0.0%) | 17/20 (85.0%) | 0/14 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 19 | 2/19 (10.5%) | 16/19 (84.2%) | 7/14 (50.0%) | 4/7 (57.1%) | 9 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 16 | 1/16 (6.2%) | 13/16 (81.2%) | 6/11 (54.5%) | 5/8 (62.5%) | 9 / 9 |
| codex | deepseek-v4-flash | sail_v3_no_human | 19 | 0/19 (0.0%) | 14/19 (73.7%) | 0/14 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 17 | 2/17 (11.8%) | 13/17 (76.5%) | 6/13 (46.2%) | 4/6 (66.7%) | 6 / 0 |
| codex | glm-5.2 | sail_v3 | 13 | 0/13 (0.0%) | 11/13 (84.6%) | 9/10 (90.0%) | 7/9 (77.8%) | 5 / 9 |
| codex | glm-5.2 | sail_v3_no_human | 14 | 0/14 (0.0%) | 13/14 (92.9%) | 0/10 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 12 | 2/12 (16.7%) | 9/12 (75.0%) | 3/8 (37.5%) | 1/3 (33.3%) | 4 / 0 |
| codex | qwen3.7-max | sail_v3 | 10 | 0/10 (0.0%) | 7/10 (70.0%) | 4/7 (57.1%) | 2/5 (40.0%) | 4 / 4 |
| codex | qwen3.7-max | sail_v3_no_human | 16 | 0/16 (0.0%) | 12/16 (75.0%) | 0/12 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 24 | 5/24 (20.8%) | 22/24 (91.7%) | 6/14 (42.9%) | 4/6 (66.7%) | 6 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 20 | 1/20 (5.0%) | 20/20 (100.0%) | 6/12 (50.0%) | 8/9 (88.9%) | 5 / 6 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 24 | 0/24 (0.0%) | 21/24 (87.5%) | 0/14 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 14 | 1/14 (7.1%) | 14/14 (100.0%) | 6/9 (66.7%) | 6/6 (100.0%) | 6 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 14 | 0/14 (0.0%) | 13/14 (92.9%) | 8/9 (88.9%) | 7/9 (77.8%) | 7 / 4 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 17 | 0/17 (0.0%) | 15/17 (88.2%) | 0/12 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 21 | 3/21 (14.3%) | 18/21 (85.7%) | 8/15 (53.3%) | 4/8 (50.0%) | 8 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 22 | 2/22 (9.1%) | 19/22 (86.4%) | 8/15 (53.3%) | 5/10 (50.0%) | 6 / 8 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 26 | 0/26 (0.0%) | 19/26 (73.1%) | 0/19 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 24 | 2/24 (8.3%) | 21/24 (87.5%) | 9/17 (52.9%) | 7/9 (77.8%) | 9 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 21 | 0/21 (0.0%) | 16/21 (76.2%) | 12/16 (75.0%) | 8/13 (61.5%) | 12 / 11 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 23 | 0/23 (0.0%) | 18/23 (78.3%) | 0/16 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 20 | 3/20 (15.0%) | 20/20 (100.0%) | 11/15 (73.3%) | 9/11 (81.8%) | 11 / 0 |
| hermes | glm-5.2 | sail_v3 | 20 | 0/20 (0.0%) | 17/20 (85.0%) | 14/15 (93.3%) | 10/14 (71.4%) | 15 / 15 |
| hermes | glm-5.2 | sail_v3_no_human | 19 | 0/19 (0.0%) | 16/19 (84.2%) | 0/14 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 17 | 4/17 (23.5%) | 15/17 (88.2%) | 3/12 (25.0%) | 3/3 (100.0%) | 3 / 0 |
| hermes | qwen3.7-max | sail_v3 | 18 | 1/18 (5.6%) | 12/18 (66.7%) | 6/13 (46.2%) | 4/7 (57.1%) | 4 / 4 |
| hermes | qwen3.7-max | sail_v3_no_human | 19 | 0/19 (0.0%) | 11/19 (57.9%) | 0/13 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
