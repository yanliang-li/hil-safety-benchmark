# Related Work 恢复记录（2026-09-13）

本次以归档中最后一版完整 Related Work 为底稿，恢复两小节结构及原有防御文献脉络，并适配当前论文的文献覆盖和 SAIL v4 实现。不是逐字回滚。

- 原对话：[分支 · LaTeX 参考文献解析问题](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)。原始消息时间为北京时间，分享归档日期不能当作改稿日期。
- 用户要求：2026-07-27 14:03:54，消息 `a38a970a-7584-4f30-821d-7446e4aec53c`（归档第 10052 行），要求“只保留两个小节”“每个小节控制在 120–150 词”，且覆盖对比表文献。
- 完整改稿：2026-07-27 14:04:38，消息 `b97d2609-d748-4a9d-a8ca-b1786e186952`（归档第 10122 行）。更早的 11:25 回复仅压缩 Defense；更晚的其他分支主要讨论篇幅、编号和排版，没有找到更新的完整 Related Work 文本。
- [原始 LaTeX 提取稿](../../recovery/related-work-restore-20260913-150212/related_work_chatgpt_original.tex) · [修改前后差异](../../recovery/related-work-restore-20260913-150212/related_work.patch)。备份同时保留修改前正文、参考文献、PDF、源码包和构建记录。

当前 [02_related_work.tex](sections/02_related_work.tex) 保留 `Agent Safety Benchmarks` 与 `Agent Safety Defenses` 两小节，分别约 129 和 135 词，共 264 词；修改前正文约 307 词。统计排除标题、引用命令及其参数，宏展开为方法名，表格引用算一个占位词，连字符词算一词。字数不包含渲染后的作者年份引用。

主要适配：

1. 保留旧稿从工具行为风险到人类反馈、从文本过滤到运行时控制的组织方式；当前对比表的九项外部基准全部在本节点名并引用。
2. 保留 HAS-Bench、HumanAgencyBench、OverEager-Bench 和 SkillSafetyBench，避免回滚后丢失当前稿已纳入的相关工作。旧的 `tab:benchmark_comparison` 改为现有 `tab:comparison`。
3. 补齐旧稿所需的八条防御文献，作者、年份、出处及窄范围描述见 [SOURCES.md](SOURCES.md#related-work-restoration-2026-09-13)。未删除既有 BibTeX 条目。
4. 保留 Progent 和 SafeAgent，替换旧稿对结构化人类授权缺口的概括；SAIL 使用当前的一次性执行许可和原任务权限描述，不声称已经保证任意跨工具效果等价。

| 术语 | 本轮统一写法 | 处理 |
| --- | --- | --- |
| 本文基准 | InterveneBench（`\bench{}`） | 沿用当前宏 |
| 本文防御 | SAIL（`\sail{}`） | 以现有方法章为准，不恢复过时的 capsule 扩展描述 |
| 求助评测基准 | HiL-Bench | 区分本研究的 HIL 机制与被引用基准名 |
| 比较阶段 | pre-action intervention / post-response control | 恢复原稿的两个阶段 |

验证：仅恢复 Related Work 后正文结束于第 8 页、PDF 共 24 页；合入其他会话的当前修改后，最终正文结束于第 9 页、PDF 共 25 页；缺失引用/交叉引用 0，越界框 0，超大浮动体 0。独立源码包可编译，提取全文与工作 PDF 一致。第 2 页渲染已检查，两小节完整位于同页。最终构建现有轻微 underfull 提示共 6 条，Related Work 本身没有该提示。本次编辑的论文章节仅为 Related Work；最终核对发现其他会话并行修改了实验、讨论及相应附录，已保留这些变动，不能将其计入本轮修改。
