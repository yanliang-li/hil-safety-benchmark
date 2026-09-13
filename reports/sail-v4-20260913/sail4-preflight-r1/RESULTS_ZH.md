# 第三轮 SAIL 结果

状态：complete；480/480 次已关闭，289 次有效。

| 条件 | 有效数 | ASR | BCR | 失败数 |
|---|---:|---:|---:|---:|
| prompt_guard_v1 | 78 | 38/78 (48.72%) | 77/78 (98.72%) | 18 |
| sail_v3 | 62 | 3/62 (4.84%) | 6/62 (9.68%) | 34 |
| sail_v4 | 51 | 5/51 (9.80%) | 49/51 (96.08%) | 45 |
| sail_v4_no_recovery | 49 | 4/49 (8.16%) | 46/49 (93.88%) | 47 |
| sail_v4_no_human | 49 | 0/49 (0.00%) | 47/49 (95.92%) | 47 |

Engineering only: original invoice and resource-budget tasks, all four replies; excluded from formal evidence.

主比较为同配置、同样本、同重复编号且双方均有效的配对比较；置信区间按基础任务聚类，另报告攻击族聚类敏感性。保留所有失败和 API 用量。独立审计只标记冲突，不修改旧评分；原始 BCR 不是语义完成度。工程预检不进入正式结论。
