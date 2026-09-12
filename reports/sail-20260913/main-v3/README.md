# SAIL HIL comparison

Status: **provisional_incomplete**. 2990/6720 attempts closed; 2710 valid, 280 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 82 | 17/82 (20.7%) | 73/82 (89.0%) | 40/62 (64.5%) | 33/41 (80.5%) | 41 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 78 | 1/78 (1.3%) | 61/78 (78.2%) | 43/59 (72.9%) | 30/48 (62.5%) | 54 / 24 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 88 | 10/88 (11.4%) | 80/88 (90.9%) | 42/66 (63.6%) | 34/42 (81.0%) | 45 / 0 |
| claude-code | glm-5.2 | sail_v3 | 81 | 3/81 (3.7%) | 69/81 (85.2%) | 41/60 (68.3%) | 33/46 (71.7%) | 43 / 21 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 66 | 10/66 (15.2%) | 61/66 (92.4%) | 19/50 (38.0%) | 14/19 (73.7%) | 20 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 63 | 1/63 (1.6%) | 54/63 (85.7%) | 27/49 (55.1%) | 20/30 (66.7%) | 23 / 15 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 85 | 16/85 (18.8%) | 78/85 (91.8%) | 27/62 (43.5%) | 20/27 (74.1%) | 32 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 78 | 2/78 (2.6%) | 64/78 (82.1%) | 37/55 (67.3%) | 29/45 (64.4%) | 41 / 38 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 77 | 7/77 (9.1%) | 68/77 (88.3%) | 26/56 (46.4%) | 22/26 (84.6%) | 27 / 0 |
| codex | glm-5.2 | sail_v3 | 64 | 0/64 (0.0%) | 56/64 (87.5%) | 29/44 (65.9%) | 23/32 (71.9%) | 20 / 25 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 75 | 11/75 (14.7%) | 70/75 (93.3%) | 22/53 (41.5%) | 18/22 (81.8%) | 40 / 0 |
| codex | qwen3.7-max | sail_v3 | 60 | 0/60 (0.0%) | 47/60 (78.3%) | 23/41 (56.1%) | 15/26 (57.7%) | 30 / 23 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 86 | 10/86 (11.6%) | 77/86 (89.5%) | 36/65 (55.4%) | 26/36 (72.2%) | 40 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 78 | 2/78 (2.6%) | 66/78 (84.6%) | 40/60 (66.7%) | 31/45 (68.9%) | 46 / 22 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 72 | 8/72 (11.1%) | 68/72 (94.4%) | 28/51 (54.9%) | 26/28 (92.9%) | 28 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 61 | 2/61 (3.3%) | 56/61 (91.8%) | 26/41 (63.4%) | 24/29 (82.8%) | 25 / 8 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 69 | 10/69 (14.5%) | 61/69 (88.4%) | 22/51 (43.1%) | 15/22 (68.2%) | 23 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 69 | 2/69 (2.9%) | 60/69 (87.0%) | 23/49 (46.9%) | 18/26 (69.2%) | 18 / 21 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 87 | 13/87 (14.9%) | 79/87 (90.8%) | 34/64 (53.1%) | 27/34 (79.4%) | 36 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 40/59 (67.8%) | 29/44 (65.9%) | 48 / 34 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 90 | 12/90 (13.3%) | 85/90 (94.4%) | 42/66 (63.6%) | 34/42 (81.0%) | 42 / 0 |
| hermes | glm-5.2 | sail_v3 | 82 | 1/82 (1.2%) | 70/82 (85.4%) | 45/61 (73.8%) | 33/47 (70.2%) | 48 / 48 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 84 | 10/84 (11.9%) | 72/84 (85.7%) | 25/64 (39.1%) | 20/25 (80.0%) | 25 / 0 |
| hermes | qwen3.7-max | sail_v3 | 79 | 2/79 (2.5%) | 60/79 (75.9%) | 33/60 (55.0%) | 19/35 (54.3%) | 25 / 14 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
