# ICLR 2027 初稿

<!-- SAIL_MAIN_COMPLETE -->
本轮 SAIL 主实验已完成：6,720 次尝试，6,019 条有效，701 次失败。正文与附录已加入独立对照结果；[中文完整表](../../reports/sail-20260913/main-v3/RESULTS_ZH.md)保留分母和限制。

**InterveneBench: Benchmarking Human-in-the-Loop Safety Control for Tool-Using Agents**

- [论文 PDF](main.pdf) · [Overleaf 源码包](iclr2027-draft-source.zip) · [编译检查](build_validation.json)
- [已完成的四框架结果](../../reports/api-multimodel-20260912/four-frameworks/RESULTS_ZH.md) · [正文数字来源](main_results_evidence.json)
- [SAIL 方法与实验设计](../../docs/sail_method.md) · [新实验目录](../../reports/sail-20260913/)
- [本轮写作取舍](REVISION_PLAN_20260913.md) · [会话复盘](REVIEW_ZH.md) · [文献核查](SOURCES.md)

正文以 HIL 为主线：何时需要人的决定，问题是否说清动作与范围，以及回复是否真正控制后续执行。已完成的四框架实验有 5,760 次尝试、5,551 条有效结果。提示防御的攻击成功率由 25.95% 降至 13.40%，但仍有 316 条攻击缺少匹配询问，55 条在询问后发生。原 GPT pilot 单列附录，避免混用不同实验的数字。

SAIL 已实现任务权限检查、具体动作询问、实际回复核验及单次执行许可。新实验用同样四个框架和三个模型，重新运行提示对照，并加入无法获得人工回复的消融。正式计划为 6,720 次；运行结果由独立结果文件注明，结束前不写入正文作为完成结论。前两版预检暴露了工作流污染审核判断、缺失授权被永久禁止的问题，保留其代码与轨迹；第三版修正后另行冻结。

仍需完善独立语义标注、未见任务验证、错误建议和部分授权轨道。现有问题准确率是规则代理；自主识别率没有独立标注。80 条实验案例来自已用于开发的 20 个任务，不能写成未见测试集。人工回复是固定合成文本。

## 编译

使用官方 ICLR 2027 匿名模板，样式来源与哈希见 [template_source.json](template_source.json)。没有压缩版心或修改官方样式。正文页数、溢出与引用检查，以 [build_validation.json](build_validation.json) 的本次构建结果为准。

在项目根目录运行：

```bash
.venv/bin/python scripts/build_main_results.py
.venv/bin/python scripts/build_sail_results.py
.venv/bin/python scripts/package_iclr_draft.py
```

最后一步会编译正文、生成源码包，并在临时目录独立编译后核对全文。Overleaf 选择 `main.tex`；源码包自带图表，不需要模型访问、Python 或 skills。图表修改沿用 Python 和 nature-figure 工作流。

公开代码位于 [yanliang-li/hil-safety-benchmark](https://github.com/yanliang-li/hil-safety-benchmark)。公开内容不包含私人会话、API 凭据或原始模型轨迹。当前仍是内部初稿；尚未提交，匿名复现材料与最终作者审查待完成。
