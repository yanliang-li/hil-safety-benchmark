# ICLR 2027 工作稿

当前题目为 **InterveneBench: Simulating, Evaluating, and Enforcing Human-in-the-Loop Agent Safety**。当前 PDF 共 23 页，匿名投稿正文在第 9 页结束；第 10--12 页为声明与参考文献，附录从第 13 页开始。

[当前 PDF](main.pdf) · [逐页预览](VIEW_PAPER.md) · [构建检查](build_validation.json) · [投稿格式检查](submission_format_validation.json)

## 当前实验状态

论文保留了已经完成的历史四回复 Agent 实验和 SAIL v3 实验，同时将 Human Response Simulator、stateful safety evaluation 和 SAIL-HIL runtime control 组织为新的主线。

计划中的 1,980 次 stateful v2.2 正式实验已于 2026-09-16 按用户要求终止。终止时共有 1,190 次 terminal attempts，其中 859 次有效、331 次失败，另有 790 次从未启动。由于矩阵不完整且 reviewer allocation 不平衡，这些部分结果没有写成论文的最终条件比较。完整记录见项目根目录的 [终止实验导出说明](../../docs/INTERVENE_V22_TERMINATED_EXPORT.md)。

当前正文明确区分已完成的历史实验、新的 stateful 协议，以及被终止的不完整运行。任何后续论文结论都应在重新完成平衡实验并审核失败机制之后更新。

## 编译

在项目根目录运行：

```bash
.venv/bin/python scripts/package_iclr_draft.py
.venv/bin/python scripts/check_iclr_submission.py
.venv/bin/python paper/iclr2027/build_preview.py
```

也可以直接使用 LaTeX 工具链编译 `paper/iclr2027/main.tex`。项目使用官方匿名模板；正文页数、引用和溢出检查以本目录中的验证报告及当前 PDF 哈希为准。

当前仍是内部工作稿，并非可直接提交的最终论文。尚需完成新的平衡实验、独立语义标注复核、作者审查与投稿信息确认。
