# 历史论文写作回顾与初稿合入（2026-09-13）

你之前确实已经写过大部分核心章节。当前稿存在两种情况：部分内容已被保留但压得过简，另一些细节只留在历史对话中。这轮按章节恢复可用内容，并用当前代码、案例和已核验结果限定旧稿中的断言。

## 回顾范围与版本选择

以 12 个课题相关会话建立去重索引，共 187 条用户消息和 715 条助手最终答复；从中定位 180 条含论文 LaTeX 或章节结构的候选消息。180 包括反复排版、公式和参考文献修复，不代表 180 段独立正文。先核对用户取舍，再精读各章最后一版完整稿及相关分支；同时对照已有 Codex 恢复说明、39 段历史表格和九张上传图的索引。未把贝叶斯推导、水工结构和 SLAM 旁支混入本课题。

不能仅按“时间最新”覆盖当前稿：7 月 27 日 22:17 后的拒绝／含糊两回复设计属于已被你在 9 月 12 日撤回的赶工方案。7 月 28 日对文风和真实性的纠正仍适用。你在 7 月 28 日 01:20 明确认可的摘要开头，可与原四回复方向合并；其助手续写的实验数字没有证据，不能一起恢复。

## 分章节对应表

| 部分 | 主要原稿位置（北京时间） | 本轮处理 | 采用与校准 | 当前落点 |
|---|---|---|---|---|
| 标题 | [07-28 01:43](../../history/chatgpt_shared/20260912/6aa4b8de-2f6c-83ee-9043-7cf57cc5fc3e.md)，第 4156 行 | 保留 | 现有标题与最后一次真实性纠正一致；不恢复未经验证的 Improving 等效果性措辞。 | [main.tex](main.tex) |
| 摘要 | [07-28 01:20](../../history/chatgpt_shared/20260912/6aa4b985-6b20-83e8-b9b7-44630a0bc2fc.md)，第 355 行 | 替换开头 | 吸收你认可的“读任务材料时被引入额外动作”场景；保留本轮真实数字和四回复协议。旧回复后半段的虚构规模与效果未采用。 | [00_abstract.tex](sections/00_abstract.tex) |
| 引言 | [07-27 21:44](../../history/chatgpt_shared/20260912/6aa4b9a9-c92c-83ee-ad4c-abfbecad2a6e.md)，第 3071 行 | 合并恢复 | 恢复正常报告交付、额外副本、批准范围与闭环衔接；合并重复论点，保留当前研究定位。 | [01_introduction.tex](sections/01_introduction.tex) |
| Related Work | [07-27 14:04](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)，第 10122 行 | 保留上一轮恢复 | 两小节已在上一轮恢复，本轮没有再改写。 | [02_related_work.tex](sections/02_related_work.tex) |
| Benchmark Overview | [07-27 14:26](../../history/chatgpt_shared/20260912/6aa4b911-0940-83ee-aa70-df992f525c60.md)，第 13939 行 | 合并恢复 | 补回任务六元组和询问前／回复后决策关系；沿用当前评分定义，不恢复旧 50-task 规模。 | [03_benchmark.tex](sections/03_benchmark.tex) |
| Benchmark Construction | [07-27 14:27](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)，第 10848 行 | 扩充并重组 | 恢复构造标准、50+200 任务来源、冻结回复匹配、执行与验证三个小节；原文“全部严格验证”的断言改为实际机械检查与语义边界。 | [04_construction.tex](sections/04_construction.tex) |
| Case Schema | [07-26 21:06](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)，第 7973 行 | 恢复至附录 | 新增五组件表：任务、工作区、回复、运行时、评测器；补充回复暴露、读到攻击与处理攻击的区别，以及事件评分。 | [08_appendix.tex](sections/08_appendix.tex) |
| 指标 | [07-26 21:03](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)，第 7636 行 | 核对后保留现行定义 | 旧稿包含多套 SafetyAskF1、RespAcc、UASR/BCR/JSU；当前六指标及 RCAA、PSER、PostSuccess 的不同分母已明确，未用旧名覆盖现行评分。 | [03_benchmark.tex](sections/03_benchmark.tex) |
| SAIL 方法 | [07-27 14:29](../../history/chatgpt_shared/20260912/6aa4b911-0940-83ee-aa70-df992f525c60.md)，第 14161 行 | 恢复组织与扩展合同 | 主文恢复效果授权与运行时执行两块结构，保留 v4 权限保存和任务恢复；四元效果签名与等价关系放入附录扩展设计。 | [06_method_v4.tex](sections/06_method_v4.tex) |
| 八域二十类 taxonomy | [07-27 20:49](../../history/chatgpt_shared/20260912/6aa4b9bf-74fc-83ee-9af2-99d3c57f3ae8.md)，第 18872 行 | 恢复完整定义 | 恢复最后一版全部二十个名称与 Definition、组内横线及居中；继续标记为设计 taxonomy，不等同于实现覆盖。 | [taxonomy.tex](tables/taxonomy.tex) |
| 图示与排版说明 | [07-27 14:21](../../history/chatgpt_shared/20260912/6aa4b85b-f70c-83ee-9d81-746fa58f4938.md)，第 10690 行 | 核对后沿用当前图 | 旧图与批注已归档；现有流程图和方法图更符合实际四回复及 v4 实现。修正方法图提前浮到 Construction 的位置，分类表与标题保持同页。 | [06_method_v4.tex](sections/06_method_v4.tex) |
| 实验与结论 | [07-28 01:43](../../history/chatgpt_shared/20260912/6aa4b8de-2f6c-83ee-9043-7cf57cc5fc3e.md)，第 4156 行 | 保留可核验结果 | 历史稿多次给出后来明确否认的预填实验数字；当前两轮实验及其负面结果不回滚，第三轮仍标记 pending。 | [05_experiments.tex](sections/05_experiments.tex) |

精确消息 ID、时间、行号和处理决定见 [机器可读来源表](archive_review_sources.json)。[完整候选索引](../../recovery/manuscript-archive-review-20260913-151700/manuscript_candidates.json)、[本轮差异](../../recovery/manuscript-archive-review-20260913-151700/restoration.patch)和[文件哈希记录](../../recovery/manuscript-archive-review-20260913-151700/change_manifest.json)保留在本地恢复目录。原始对话保持不变。

## 哪些旧内容不能写成已完成

- **旧数字**：3,000 cases、八组 agent–model、74.6%、SAIL 22.0%→8.5% 等缺乏匹配运行证据。保留当前两轮真实结果及安全／效用取舍。
- **因果分叉**：四类案例的任务组成相同，不等于同一个询问前状态。checkpoint/resume 尚未实现；保留为扩展比较。
- **回复维度**：scope mismatch 不等于客观错误，也不等于真正的部分授权。后两类仍需事实来源、许可子集和独立效果谓词。
- **效果等价**：旧稿的 sigma 四元组可作为接口与归一化目标，但不是已验证的跨工具等价证明。现有方法仍是具体调用许可与模型参与的效果关联。
- **覆盖与验证**：八域二十类是设计分类；实现的二十 attack families 不能自动证明其完整覆盖。“全部语义验证通过”不成立。
- **已确定的方向**：HIL 前的风险发现与选择性询问、HIL 后的正确使用回复、良性任务完成均保留。没有采用危险动作一律禁止的简化。

## 本轮新增内容的本地证据

- `src/hil_safety_bench/schemas.py`：任务、攻击、效果、回复与案例结构；`runtime.py:58`：只有匹配问题暴露冻结回复，公开结果只含回复文本，重复匹配不改变回复。
- `task_catalog.py`、`expanded_tasks.py`、`scaled_tasks.py`：50 个原任务模板和 200 个扩展任务；代码中的总量为 250、195 confirmable / 55 prohibited、24 application domains、20 implementation families。
- 逐组检查 `data/cases.jsonl` 的全部 1,000 条案例：250 组均包含四类回复，同组任务字段完全一致。检查记录见 [case_structure_check.json](../../recovery/manuscript-archive-review-20260913-151700/case_structure_check.json)。这验证结构一致性，不证明语义等价或因果控制。
- `scripts/hil_guard_v4/protocol.py` 与 `core.py`：原任务引用、具体参数约束、回复证据、累计数量和执行许可；一般归一化仍按扩展设计表述。

## 写作与证据分配

| 内容 | 功能 | 放置及取舍 |
|---|---|---|
| 正常交付场景、两阶段决策 | 定义研究问题 | 替换摘要／引言开头，Overview 补回短任务表示 |
| 构造标准、50+200 来源、回复暴露 | 可复现性必要信息 | 合并为 Construction 三小节 |
| 五组件 schema、重复询问策略 | 实现溯源细节 | 新增附录 B，主文一处指向 |
| 一般效果签名与工具等价 | 扩展设计边界 | 附录 H，不增加已完成主张 |
| 全部 taxonomy 定义 | 构造目标细节 | 附录 K；标题与完整表同页，保留组内横线 |
| 两轮 ASR/BCR、主要配对区间、效用损失 | 核心证据与限制 | 沿用主文实验，不重算或选择性摘录 |
| 全配置、分母、成本与运行失败 | 支撑与可复现性 | 沿用当前主表／附录／结果来源文件 |

主线按“场景与问题 → 可观察协议 → 案例构造 → 权限与执行 → 真实实验 → 边界”展开。原有正文的重复解释优先替换，长 schema 与未实现的通用合同放附录。结果和讨论不重复新增旧稿中的提升结论。

| 术语 | 本轮固定含义 |
|---|---|
| InterveneBench | 当前四回复 benchmark |
| SAIL v3 / SAIL v4 | 第二轮已完成控制器 / 第三轮实现与待完成评估 |
| confirmable / prohibited | 授权模式；不自动等同于必须询问／无需询问标签 |
| response profile / wording style | 授权语义类别 / 表面表达方式 |
| RCAA / PSER / PostSuccess | 回复动作正确 / 安全良性完成 / 正确回复使用且安全完成，不能互换 |
| application domain / implementation family / risk domain | 业务领域 / 代码机制标签 / 被保护的边界 |

## 字数与构建检查

| 部分 | 修改前 | 修改后 |
|---|---:|---:|
| 00_abstract | 196 | 183 |
| 01_introduction | 284 | 311 |
| 03_benchmark | 469 | 492 |
| 04_construction | 261 | 359 |
| 06_method_v4 | 406 | 429 |
| 08_appendix | 1792 | 2004 |

上述为统一脚本计算的近似正文词数：排除注释、标题、引用参数和显示公式／图表；保留行内数学，宏展开为名称。长表另按完整二十条定义检查。摘要中的所有数字 token 与修改前逐项一致。

最终 PDF 正文结束于第 9 页，共 25 页；源码包独立编译后的提取全文与工作 PDF 一致。缺失引用／交叉引用 0，越界框 0，超大浮动体 0。已检查整稿缩略图与新增内容放大图，修正方法图跨章节前浮和 taxonomy 标题脱离表格的问题。保留四条轻微 underfull 提示，未改官方字体、版心或模板样式。最终哈希见 [build_validation.json](build_validation.json)。
