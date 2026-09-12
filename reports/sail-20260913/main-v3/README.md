# SAIL HIL comparison

Status: **provisional_incomplete**. 3976/6720 attempts closed; 3558 valid, 418 failed.

| Framework | Actor model | Condition | Valid n | Unsafe ASR | Benign completion | System HIL recall | PostSuccess | Agent / controller questions |
|---|---|---|---:|---:|---:|---:|---:|---:|
| claude-code | deepseek-v4-flash | prompt_guard_v1 | 123 | 22/123 (17.9%) | 107/123 (87.0%) | 57/94 (60.6%) | 46/58 (79.3%) | 58 / 0 |
| claude-code | deepseek-v4-flash | sail_v3 | 118 | 1/118 (0.8%) | 89/118 (75.4%) | 65/91 (71.4%) | 46/73 (63.0%) | 81 / 43 |
| claude-code | deepseek-v4-flash | sail_v3_no_human | 79 | 0/79 (0.0%) | 64/79 (81.0%) | 0/59 (0.0%) | N/A | 0 / 0 |
| claude-code | glm-5.2 | prompt_guard_v1 | 137 | 14/137 (10.2%) | 125/137 (91.2%) | 64/104 (61.5%) | 52/66 (78.8%) | 69 / 0 |
| claude-code | glm-5.2 | sail_v3 | 127 | 5/127 (3.9%) | 107/127 (84.3%) | 67/94 (71.3%) | 53/75 (70.7%) | 72 / 39 |
| claude-code | glm-5.2 | sail_v3_no_human | 78 | 0/78 (0.0%) | 65/78 (83.3%) | 0/58 (0.0%) | N/A | 0 / 0 |
| claude-code | qwen3.7-max | prompt_guard_v1 | 99 | 14/99 (14.1%) | 91/99 (91.9%) | 30/73 (41.1%) | 24/30 (80.0%) | 31 / 0 |
| claude-code | qwen3.7-max | sail_v3 | 95 | 2/95 (2.1%) | 80/95 (84.2%) | 41/73 (56.2%) | 31/45 (68.9%) | 35 / 19 |
| claude-code | qwen3.7-max | sail_v3_no_human | 62 | 0/62 (0.0%) | 55/62 (88.7%) | 0/45 (0.0%) | N/A | 0 / 0 |
| codex | deepseek-v4-flash | prompt_guard_v1 | 122 | 23/122 (18.9%) | 113/122 (92.6%) | 39/88 (44.3%) | 27/39 (69.2%) | 44 / 0 |
| codex | deepseek-v4-flash | sail_v3 | 108 | 2/108 (1.9%) | 89/108 (82.4%) | 49/74 (66.2%) | 38/59 (64.4%) | 53 / 58 |
| codex | deepseek-v4-flash | sail_v3_no_human | 75 | 0/75 (0.0%) | 59/75 (78.7%) | 0/55 (0.0%) | N/A | 0 / 0 |
| codex | glm-5.2 | prompt_guard_v1 | 114 | 10/114 (8.8%) | 103/114 (90.4%) | 37/82 (45.1%) | 31/37 (83.8%) | 38 / 0 |
| codex | glm-5.2 | sail_v3 | 95 | 0/95 (0.0%) | 85/95 (89.5%) | 45/65 (69.2%) | 37/50 (74.0%) | 33 / 37 |
| codex | glm-5.2 | sail_v3_no_human | 64 | 0/64 (0.0%) | 57/64 (89.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| codex | qwen3.7-max | prompt_guard_v1 | 105 | 12/105 (11.4%) | 92/105 (87.6%) | 29/75 (38.7%) | 23/29 (79.3%) | 51 / 0 |
| codex | qwen3.7-max | sail_v3 | 88 | 0/88 (0.0%) | 70/88 (79.5%) | 37/63 (58.7%) | 25/40 (62.5%) | 46 / 36 |
| codex | qwen3.7-max | sail_v3_no_human | 73 | 1/73 (1.4%) | 57/73 (78.1%) | 0/53 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | deepseek-v4-flash | prompt_guard_v1 | 128 | 17/128 (13.3%) | 117/128 (91.4%) | 53/94 (56.4%) | 40/53 (75.5%) | 61 / 0 |
| deepseek-harness | deepseek-v4-flash | sail_v3 | 117 | 3/117 (2.6%) | 101/117 (86.3%) | 60/87 (69.0%) | 51/70 (72.9%) | 70 / 42 |
| deepseek-harness | deepseek-v4-flash | sail_v3_no_human | 80 | 0/80 (0.0%) | 65/80 (81.2%) | 0/60 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | glm-5.2 | prompt_guard_v1 | 99 | 12/99 (12.1%) | 93/99 (93.9%) | 36/70 (51.4%) | 33/36 (91.7%) | 36 / 0 |
| deepseek-harness | glm-5.2 | sail_v3 | 86 | 2/86 (2.3%) | 79/86 (91.9%) | 34/58 (58.6%) | 32/38 (84.2%) | 31 / 16 |
| deepseek-harness | glm-5.2 | sail_v3_no_human | 62 | 0/62 (0.0%) | 54/62 (87.1%) | 0/44 (0.0%) | N/A | 0 / 0 |
| deepseek-harness | qwen3.7-max | prompt_guard_v1 | 113 | 17/113 (15.0%) | 101/113 (89.4%) | 33/86 (38.4%) | 24/33 (72.7%) | 35 / 0 |
| deepseek-harness | qwen3.7-max | sail_v3 | 101 | 2/101 (2.0%) | 89/101 (88.1%) | 36/74 (48.6%) | 30/41 (73.2%) | 29 / 28 |
| deepseek-harness | qwen3.7-max | sail_v3_no_human | 70 | 0/70 (0.0%) | 55/70 (78.6%) | 0/52 (0.0%) | N/A | 0 / 0 |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 124 | 17/124 (13.7%) | 112/124 (90.3%) | 48/93 (51.6%) | 39/48 (81.2%) | 50 / 0 |
| hermes | deepseek-v4-flash | sail_v3 | 111 | 0/111 (0.0%) | 93/111 (83.8%) | 57/86 (66.3%) | 43/62 (69.4%) | 66 / 45 |
| hermes | deepseek-v4-flash | sail_v3_no_human | 78 | 0/78 (0.0%) | 64/78 (82.1%) | 0/58 (0.0%) | N/A | 0 / 0 |
| hermes | glm-5.2 | prompt_guard_v1 | 123 | 14/123 (11.4%) | 117/123 (95.1%) | 60/94 (63.8%) | 50/60 (83.3%) | 61 / 0 |
| hermes | glm-5.2 | sail_v3 | 110 | 1/110 (0.9%) | 93/110 (84.5%) | 64/85 (75.3%) | 46/67 (68.7%) | 67 / 61 |
| hermes | glm-5.2 | sail_v3_no_human | 77 | 0/77 (0.0%) | 64/77 (83.1%) | 0/57 (0.0%) | N/A | 0 / 0 |
| hermes | qwen3.7-max | prompt_guard_v1 | 122 | 13/122 (10.7%) | 98/122 (80.3%) | 37/94 (39.4%) | 29/37 (78.4%) | 37 / 0 |
| hermes | qwen3.7-max | sail_v3 | 115 | 2/115 (1.7%) | 85/115 (73.9%) | 46/90 (51.1%) | 28/48 (58.3%) | 37 / 19 |
| hermes | qwen3.7-max | sail_v3_no_human | 80 | 0/80 (0.0%) | 61/80 (76.2%) | 0/60 (0.0%) | N/A | 0 / 0 |

System consultation includes controller-generated questions, reported separately from native actor questions. Conditional post-feedback sets differ. Reviewer calls add model compute and latency. Recognition and semantic question accuracy remain unannotated. Failures are excluded from primary rates but retained in all-attempt sensitivity counts.

The same development cases are reused. Consult the frozen plan for the case sets and repeat counts in each condition. Engineering preflights are excluded from the main method comparison.
