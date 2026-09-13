# ICLR 2027 初稿

本次附录精简合并为六节，保留完整结果分母、区间、失败记录、评分边界与复现协议，删去重复表格和工程流水账。[附录修改记录](REVISION_NOTES_APPENDIX_20260913.md)列出取舍及篇幅变化。正文实验结果与 agent 分析保留。

本次历史稿恢复后正文为 9 页：第 7 页为 12 组 agent 的结果矩阵，第 8 页为 SAIL v3 的安全、完成率和交互指标。已从原对话补回摘要与引言场景、任务定义、构造细节、方法组织、案例结构和分类表定义；[逐章回顾与来源](ARCHIVE_REVIEW_20260913.md)记录采用内容及证据边界。正文保留逐配置评价、回复误用、正常任务损失、无人工回复消融以及失败和开销分析；此前的[结果正文修改记录](REVISION_NOTES_MAIN_TEXT_20260913.md)保留当时的内容分配和字数变化。

<!-- SAIL_MAIN_COMPLETE -->
本轮 SAIL 主实验已完成：6,720 次尝试，6,019 条有效，701 次失败。正文与附录已加入独立对照结果；[中文完整表](../../reports/sail-20260913/main-v3/RESULTS_ZH.md)保留分母和限制。

**InterveneBench: Benchmarking Human-in-the-Loop Safety Control for Tool-Using Agents**

- [论文 PDF](main.pdf) · [Overleaf 源码包](iclr2027-draft-source.zip) · [编译检查](build_validation.json)
- [已完成的四框架结果](../../reports/api-multimodel-20260912/four-frameworks/RESULTS_ZH.md) · [正文数字来源](main_results_evidence.json)
- [SAIL 方法与实验设计](../../docs/sail_method.md) · [新实验目录](../../reports/sail-20260913/)
- [本轮写作取舍](REVISION_PLAN_20260913.md) · [会话复盘](REVIEW_ZH.md) · [文献核查](SOURCES.md)

正文以 HIL 为主线：何时需要人的决定，问题是否说清动作与范围，以及回复是否真正控制后续执行。已完成的四框架实验有 5,760 次尝试、5,551 条有效结果。提示防御的攻击成功率由 25.95% 降至 13.40%，但仍有 316 条攻击缺少匹配询问，55 条在询问后发生。原 GPT pilot 单列附录，避免混用不同实验的数字。

SAIL v3 的独立 6,720 次比较已经完成，降低了有效运行的 ASR，但也损失正常任务完成，并增加失败和额外调用。SAIL v4 在此基础上实现原始权限保留和任务恢复；第三轮正式结果仍待完成，工程预检保持独立。

仍需完善独立语义标注、未见任务验证、错误建议和部分授权轨道。现有问题准确率是规则代理；自主识别率没有独立标注。80 条实验案例来自已用于开发的 20 个任务，不能写成未见测试集。人工回复是固定合成文本。

## 编译

使用官方 ICLR 2027 匿名模板，样式来源与哈希见 [template_source.json](template_source.json)。没有压缩版心或修改官方样式。正文页数、溢出与引用检查，以 [build_validation.json](build_validation.json) 的本次构建结果为准。

在项目根目录运行：

```bash
.venv/bin/python scripts/build_main_results.py
.venv/bin/python scripts/build_sail_results.py
.venv/bin/python scripts/package_iclr_v4_draft.py
```

最后一步会编译正文、生成源码包，并在临时目录独立编译后核对全文。Overleaf 选择 `main.tex`；源码包自带图表，不需要模型访问、Python 或 skills。图表修改沿用 Python 和 nature-figure 工作流。

两个结果构建脚本刷新派生数字、表格和证据文件；不会覆盖人工修改的正文、摘要或第三轮状态。打包检查要求两张核心结果表均位于正文，并只收录当前稿件实际引用的源文件；未使用的历史段落和旧图表保留在本地归档。

公开代码位于 [yanliang-li/hil-safety-benchmark](https://github.com/yanliang-li/hil-safety-benchmark)。公开内容不包含私人会话、API 凭据或原始模型轨迹。当前仍是内部初稿；尚未提交，匿名复现材料与最终作者审查待完成。
