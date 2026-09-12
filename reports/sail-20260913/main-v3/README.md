# SAIL HIL comparison

Status: **provisional_incomplete**. 1497/6720 attempts closed; 1337 valid, 160 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 43 | 9/43 (20.9%) | 37/43 (86.0%) | 21/32 (65.6%) | 17/22 (77.3%) | 22 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 42 | 1/42 (2.4%) | 31/42 (73.8%) | 23/32 (71.9%) | 14/26 (53.8%) | 32 / 15 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 42 | 0/42 (0.0%) | 34/42 (81.0%) | 0/31 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 41 | 3/41 (7.3%) | 38/41 (92.7%) | 19/30 (63.3%) | 15/19 (78.9%) | 21 / 0 |
| claude-code | glm-5.2 | sail_v3 | 39 | 0/39 (0.0%) | 34/39 (87.2%) | 20/29 (69.0%) | 16/20 (80.0%) | 17 / 6 |
| claude-code | glm-5.2 | sail_v3_no_human | 40 | 0/40 (0.0%) | 36/40 (90.0%) | 0/29 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 32 | 7/32 (21.9%) | 28/32 (87.5%) | 12/24 (50.0%) | 7/12 (58.3%) | 13 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 28 | 1/28 (3.6%) | 21/28 (75.0%) | 17/23 (73.9%) | 10/19 (52.6%) | 14 / 11 |
| claude-code | qwen3.7-max | sail_v3_no_human | 29 | 0/29 (0.0%) | 24/29 (82.8%) | 0/20 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 43 | 5/43 (11.6%) | 37/43 (86.0%) | 16/31 (51.6%) | 11/16 (68.8%) | 19 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 38 | 1/38 (2.6%) | 28/38 (73.7%) | 17/26 (65.4%) | 12/22 (54.5%) | 22 / 22 |
| codex | deepseek-v4-flash | sail_v3_no_human | 42 | 0/42 (0.0%) | 30/42 (71.4%) | 0/30 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 40 | 5/40 (12.5%) | 34/40 (85.0%) | 12/29 (41.4%) | 8/12 (66.7%) | 12 / 0 |
| codex | glm-5.2 | sail_v3 | 35 | 0/35 (0.0%) | 30/35 (85.7%) | 16/25 (64.0%) | 12/18 (66.7%) | 10 / 15 |
| codex | glm-5.2 | sail_v3_no_human | 35 | 0/35 (0.0%) | 31/35 (88.6%) | 0/23 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 28 | 4/28 (14.3%) | 25/28 (89.3%) | 8/19 (42.1%) | 6/8 (75.0%) | 13 / 0 |
| codex | qwen3.7-max | sail_v3 | 24 | 0/24 (0.0%) | 19/24 (79.2%) | 9/17 (52.9%) | 7/10 (70.0%) | 12 / 5 |
| codex | qwen3.7-max | sail_v3_no_human | 33 | 1/33 (3.0%) | 26/33 (78.8%) | 0/23 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 41 | 6/41 (14.6%) | 36/41 (87.8%) | 14/28 (50.0%) | 9/14 (64.3%) | 14 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 36 | 1/36 (2.8%) | 31/36 (86.1%) | 16/25 (64.0%) | 14/20 (70.0%) | 14 / 11 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 40 | 0/40 (0.0%) | 33/40 (82.5%) | 0/27 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 35 | 5/35 (14.3%) | 33/35 (94.3%) | 12/24 (50.0%) | 12/12 (100.0%) | 12 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 32 | 1/32 (3.1%) | 29/32 (90.6%) | 13/21 (61.9%) | 12/15 (80.0%) | 12 / 7 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 38 | 0/38 (0.0%) | 32/38 (84.2%) | 0/27 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 37 | 4/37 (10.8%) | 32/37 (86.5%) | 12/28 (42.9%) | 8/12 (66.7%) | 13 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 38 | 2/38 (5.3%) | 35/38 (92.1%) | 12/27 (44.4%) | 9/14 (64.3%) | 9 / 10 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 39 | 0/39 (0.0%) | 31/39 (79.5%) | 0/29 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 40 | 6/40 (15.0%) | 37/40 (92.5%) | 18/32 (56.2%) | 15/18 (83.3%) | 20 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 36 | 0/36 (0.0%) | 30/36 (83.3%) | 25/30 (83.3%) | 20/26 (76.9%) | 27 / 18 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 39 | 0/39 (0.0%) | 33/39 (84.6%) | 0/31 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 40 | 7/40 (17.5%) | 39/40 (97.5%) | 21/30 (70.0%) | 18/21 (85.7%) | 21 / 0 |
| hermes | glm-5.2 | sail_v3 | 39 | 1/39 (2.6%) | 34/39 (87.2%) | 25/29 (86.2%) | 19/26 (73.1%) | 27 / 23 |
| hermes | glm-5.2 | sail_v3_no_human | 38 | 0/38 (0.0%) | 34/38 (89.5%) | 0/28 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 38 | 4/38 (10.5%) | 31/38 (81.6%) | 12/28 (42.9%) | 11/12 (91.7%) | 12 / 0 |
| hermes | qwen3.7-max | sail_v3 | 37 | 2/37 (5.4%) | 27/37 (73.0%) | 15/27 (55.6%) | 10/16 (62.5%) | 12 / 6 |
| hermes | qwen3.7-max | sail_v3_no_human | 40 | 0/40 (0.0%) | 29/40 (72.5%) | 0/29 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
