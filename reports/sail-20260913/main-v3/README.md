# SAIL HIL comparison

Status: **provisional_incomplete**. 4228/6720 attempts closed; 3768 valid, 460 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 134 | 24/134 (17.9%) | 117/134 (87.3%) | 61/100 (61.0%) | 49/62 (79.0%) | 62 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 130 | 1/130 (0.8%) | 100/130 (76.9%) | 70/98 (71.4%) | 51/79 (64.6%) | 88 / 45 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 144 | 15/144 (10.4%) | 131/144 (91.0%) | 64/107 (59.8%) | 52/66 (78.8%) | 69 / 0 |
| claude-code | glm-5.2 | sail_v3 | 134 | 5/134 (3.7%) | 113/134 (84.3%) | 69/97 (71.1%) | 54/77 (70.1%) | 74 / 42 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 102 | 14/102 (13.7%) | 92/102 (90.2%) | 31/76 (40.8%) | 25/31 (80.6%) | 32 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 96 | 2/96 (2.1%) | 81/96 (84.4%) | 42/74 (56.8%) | 32/46 (69.6%) | 36 / 19 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 132 | 23/132 (17.4%) | 123/132 (93.2%) | 42/96 (43.8%) | 30/42 (71.4%) | 48 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 118 | 2/118 (1.7%) | 99/118 (83.9%) | 52/82 (63.4%) | 41/63 (65.1%) | 56 / 63 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 122 | 12/122 (9.8%) | 110/122 (90.2%) | 38/88 (43.2%) | 32/38 (84.2%) | 39 / 0 |
| codex | glm-5.2 | sail_v3 | 100 | 0/100 (0.0%) | 90/100 (90.0%) | 47/70 (67.1%) | 39/52 (75.0%) | 35 / 37 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 112 | 12/112 (10.7%) | 96/112 (85.7%) | 30/80 (37.5%) | 24/30 (80.0%) | 52 / 0 |
| codex | qwen3.7-max | sail_v3 | 90 | 0/90 (0.0%) | 72/90 (80.0%) | 37/64 (57.8%) | 25/40 (62.5%) | 46 / 36 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 140 | 19/140 (13.6%) | 126/140 (90.0%) | 59/103 (57.3%) | 43/60 (71.7%) | 68 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 129 | 4/129 (3.1%) | 109/129 (84.5%) | 66/96 (68.8%) | 55/78 (70.5%) | 78 / 50 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 112 | 13/112 (11.6%) | 106/112 (94.6%) | 39/79 (49.4%) | 36/39 (92.3%) | 39 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 98 | 3/98 (3.1%) | 91/98 (92.9%) | 38/66 (57.6%) | 35/42 (83.3%) | 35 / 16 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 123 | 18/123 (14.6%) | 109/123 (88.6%) | 35/94 (37.2%) | 26/35 (74.3%) | 37 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 111 | 2/111 (1.8%) | 98/111 (88.3%) | 39/83 (47.0%) | 32/44 (72.7%) | 32 / 30 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 134 | 18/134 (13.4%) | 122/134 (91.0%) | 50/99 (50.5%) | 41/50 (82.0%) | 52 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 121 | 0/121 (0.0%) | 103/121 (85.1%) | 61/92 (66.3%) | 47/67 (70.1%) | 71 / 48 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 135 | 17/135 (12.6%) | 129/135 (95.6%) | 64/103 (62.1%) | 54/64 (84.4%) | 65 / 0 |
| hermes | glm-5.2 | sail_v3 | 121 | 1/121 (0.8%) | 102/121 (84.3%) | 72/93 (77.4%) | 53/76 (69.7%) | 75 / 66 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 129 | 13/129 (10.1%) | 100/129 (77.5%) | 38/99 (38.4%) | 29/38 (76.3%) | 38 / 0 |
| hermes | qwen3.7-max | sail_v3 | 123 | 2/123 (1.6%) | 91/123 (74.0%) | 48/96 (50.0%) | 29/50 (58.0%) | 38 / 21 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
