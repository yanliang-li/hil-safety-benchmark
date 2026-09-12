# Hermes extension

Status: **provisional_incomplete**. 546 valid runs, 10 failed attempts, 884 pending out of 1440 planned.

| Harness | Requested model | Condition | Valid n | Unsafe ASR | Benign completion | HIL recall | Strict after reply |
|---|---|---|---:|---:|---:|---:|---:|
| hermes | deepseek-v4-flash | neutral | 96 | 30/96 (31.2%) | 84/96 (87.5%) | 37/70 (52.9%) | 26/37 (70.3%) |
| hermes | deepseek-v4-flash | prompt_guard_v1 | 91 | 15/91 (16.5%) | 81/91 (89.0%) | 32/67 (47.8%) | 24/33 (72.7%) |
| hermes | glm-5.2 | neutral | 86 | 21/86 (24.4%) | 78/86 (90.7%) | 31/65 (47.7%) | 25/31 (80.6%) |
| hermes | glm-5.2 | prompt_guard_v1 | 88 | 12/88 (13.6%) | 84/88 (95.5%) | 36/66 (54.5%) | 30/36 (83.3%) |
| hermes | qwen3.7-max | neutral | 92 | 22/92 (23.9%) | 83/92 (90.2%) | 18/71 (25.4%) | 13/18 (72.2%) |
| hermes | qwen3.7-max | prompt_guard_v1 | 93 | 11/93 (11.8%) | 86/93 (92.5%) | 28/71 (39.4%) | 21/28 (75.0%) |

ARIR and semantic question precision remain unavailable. Question precision is a rule-based proxy. API failures, timeouts, and OOM kills are excluded from valid-run safety rates and reported separately. Finished no-tool answers remain valid outcomes. The 20 task clusters were used during prompt development; this is not an untouched test set.

The full manifest, per-case rows, repeat-level counts, paired task-cluster intervals, and score-replay hashes are retained beside this report. Do not treat pending work as completed evidence.
