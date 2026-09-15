# HILBench 实验设计 Paper Card

> Source coverage: Full paper
> Extraction confidence: High
> Locator mode: page-grounded
> Primary analytical lens: 实验设计、交互 oracle 与证据链
> Secondary analytical lens: 对 InterveneBench / SAIL-HIL 的可迁移控制
> Context verification: Paper-only
> Card completeness: Complete relative to supplied source

## 01 基本信息

- 标题：*HIL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?*
- 作者：Tu Trinh、Mohamed Elfeki、Guangze Luo、Kelvin Luu、Nathan Hunt、Ernesto Hernández、Nandan Marwaha、Yannis Yiming He、Charles Wang、Fernando Carabedo、Alessa Castillo、Bing Liu
- 机构：Scale AI
- 版本：arXiv:2604.09408v4，2026-05-04；正式会议/DOI 未在所给 PDF 中标明
- 类型：交互式智能体评测与训练论文
- 关键词：selective escalation、ask_human、ambiguity、agent benchmark、Ask-F1、RLVR
- 代码与数据：PDF 首页给出 harness/data 链接；本项目核对的官方仓库 commit 为 `a98052f7...`
- 阅读日期：2026-09-14
- 与本项目的关系：直接提供“何时询问”的对照、门槛和 matcher 验证范式；不覆盖“自由文本人类回复之后如何安全行动”。

## 02 一句话总结

[Paper] HILBench 通过在 SWE 与 text-to-SQL 任务中植入只能由外部人类 oracle 解决、且随环境探索逐步暴露的 blocker，并用 Ask-F1 同时惩罚漏问与滥问，显示前沿智能体在 full-information 下可解任务上仍存在显著 selective-escalation 缺口，并报告 shaped Ask-F1 RLVR 可改善该能力。[Paper: PDF pp. 1–2, 6, 8]

## 03 研究问题

- 具体问题：[Paper] 智能体是否能在长程任务执行中识别无法靠环境或推理消除的信息缺口，提出有针对性的问题，吸收答案并继续执行？[Paper: PDF pp. 1–2]
- 重要性：[Paper] 传统 benchmark 给出完整规格，只按最终正确性评分，无法区分“幸运猜对”和“知道何时求助”。[Paper: PDF pp. 1–2]
- 既有方法不足：[Paper-framed; external verification not performed] 既有澄清任务多把歧义直接放在初始问题中，常只有一个 gap，也缺少对 question spam 的显式代价。[Paper: PDF p. 3]
- 精确问题：Can an agent selectively escalate only the information gaps that cannot be resolved through progressive environment exploration, while still completing the task?

## 04 研究背景与发展路径

[Paper-framed; external verification not performed]

| 阶段 | 代表范式 | 优点 | 局限 | HILBench 的定位 |
|---|---|---|---|---|
| 静态完整规格 benchmark | HumanEval、SWE-Bench、BIRD 等 | 结果易自动验证 | 不出现必须向人询问的信息缺口 | 修改既有可验证任务，引入 blocker |
| 对话/歧义检测 | 澄清问题生成、AmbigQA 等 | 直接研究歧义 | gap 多在开场可见，未必需要行动中探索 | 强调 progressive discovery |
| 交互式 agent benchmark | 工具使用、协作式 coding | 测长程执行 | 不一定同时度量漏问和滥问 | Ask-F1 + pass@3 联合过程/结果 |
| 判断训练 | RL/RLVR | 可优化行为 | 稀疏任务奖励难定位何时问 | 将 Ask-F1 拆为逐步与终局 reward |

来源：[Paper: PDF pp. 2–3, 8]

## 05 论文识别的核心痛点

| 痛点 | 表现 | 作者解释 | 论文证据 |
|---|---|---|---|
| 不求助的自信错误 | 模型填补缺失规格并提交貌似合理的错误结果 | 训练和 benchmark 奖励自主完成而非识别不可解不确定性 | full-info 与 ask-human pass@3 的大差距 [Paper: PDF pp. 2, 6] |
| 过度询问 | 用大量宽泛问题换 recall，增加人类负担 | 单独 reward recall 可被 question spam 利用 | Ask-F1 的 precision 项与例子 [Paper: PDF p. 5, Eq. 1] |
| 发现不确定性但不解决 | 模型意识到卡住，仍不问或不完成 | uncertainty detection 与 resolution 是不同技能 | Claude failure analysis [Paper: PDF pp. 7–8] |
| 环境探索不足 | blocker 只有在代码库/数据库探索后出现 | 开场规格检查不能替代执行中的 progressive discovery | 设计与 Fig. 2 [Paper: PDF pp. 4–5, Figure 2] |

## 06 核心思想

1. 表层方法：[Paper] 为原本可解的 SWE/SQL 任务注入 3–5 个 blocker，注册精确 resolution 与 trigger questions，提供受语义 matcher 控制的 `ask_human(question)`。[Paper: PDF pp. 3–5]
2. 核心洞见：[Paper] 帮助寻求不是单纯“会不会问”，而是探索后识别不可消除缺口、精准询问、使用答案并继续任务的选择性判断。[Paper: PDF pp. 1–2]
3. [Analysis] 可迁移的一般原则：交互 benchmark 应把“信息是否需要外部权限/知识”“问题是否精准”“答案是否被正确转化为动作”分开，否则一个终局成功率无法定位失败环节。

## 07 方法概览

- 输入：修改后的 SWE-Bench Pro 或 BIRD 任务及其环境。
- 隐藏真值：每个 blocker 的类型、独立描述、精确 resolution 与多样 trigger questions。
- 工具：常规执行/探索工具加 `ask_human(question)`。
- oracle：冻结 Llama-3.3-70B-Instruct 只做 question–blocker 匹配；匹配时返回 registry 中的固定 resolution，不匹配时返回固定 irrelevant 文本。[Paper: PDF p. 5, Appendix D]
- 输出：代码 patch 或 SQL、问题轨迹、pass@3、precision、blocker recall 与 Ask-F1。
- 训练：Qwen3-32B + LoRA + SkyRL；逐问 reward 与终局 coverage reward。[Paper: PDF pp. 8–9]

流程：可验证原任务 → 人工植入 blocker → 必要性/充分性筛选 → agent 探索 → 定向询问 → matcher 返回固定 resolution → agent 继续 → 任务与 Ask-F1 双重评分。

## 08 核心模块拆解

| 模块 | 功能 | 必要性 | 输入/输出 | 支持证据 | 移除影响 |
|---|---|---|---|---|---|
| Blocker registry | 保存 gap 与精确 resolution | 给 oracle 与 recall 提供真值 | blocker 描述/触发问法 → resolution | [Paper: Appendix C.3, PDF pp. 14–15] | [Analysis] 无法稳定复现回答或计算 blocker recall |
| Progressive discovery | 让 gap 在探索中出现 | 区分开场歧义检测与长程判断 | 环境轨迹 → 暴露 gap | [Paper: PDF pp. 2, 4–5] | 作者未报告单独消融；预期退化为静态澄清 |
| Frozen semantic matcher | 将自由问题映射到 registry | 保留问题表面多样性并固定回复 | 问题+blocker → match/no-match | [Paper: PDF p. 5, Appendix D] | [Analysis] 精度下降会直接污染 Ask-F1 |
| Ask-F1 | 同时度量针对性与覆盖率 | 防 question spam | relevant questions/blockers → F1 | [Paper: PDF p. 5, Eq. 1] | 只用 recall 会鼓励滥问 |
| Full-info / no-tool controls | 检验能力与 blocker 必要性 | 防止把任务本身不可解误写成判断失败 | 条件 → pass@3 | [Paper: PDF pp. 2, 6] | 归因“判断缺口”失去支撑 |
| Shaped RLVR | 给询问提供密集与终局 reward | 测判断是否可训练 | trajectory → step/terminal reward | [Paper: PDF p. 8, Eq. 2, Fig. 4] | 论文未给完整 reward 消融 |

## 09 必要公式与符号

对任务的 blocker 集合 (B)、模型问题集合 (Q)、相关问题 (Q_{rel}) 和被覆盖 blocker (B_{addr})：

\[
P=\frac{|Q_{rel}|}{|Q|},\qquad R=\frac{|B_{addr}|}{|B|},\qquad
\mathrm{AskF1}=\frac{2PR}{P+R}.
\]

它把人类交互成本与缺口覆盖放入同一指标；任一项接近零都会压低 F1。[Paper: PDF p. 5, Eq. 1]

逐步训练 reward：相关新问题 (+0.3)，无关或重复已解决问题 (-0.1)；终局 reward 在至少发现一个 blocker 时为 (|B_{discovered}|/|B|)，否则为 0。[Paper: PDF p. 8, Eq. 2]

附录将两项写成独立公式：Equation 3 是上述逐问分段 reward，Equation 4 是带“至少发现一个 blocker”门控的终局覆盖 reward；总 reward 为二者之和。[Paper: PDF p. 19, Equation 3; PDF p. 19, Equation 4]

## 10 实验设计与证据链

- 数据：300 tasks（150 SWE、150 SQL），1,131 blockers，平均 3.77/task；200 public/100 private。[Paper: PDF p. 5, Appendix E Table 3]
- 类型：missing 42.1%、ambiguous 36.1%、contradictory 21.8%。[Paper: Appendix E, PDF p. 15, Table 3]
- 条件：baseline/no tool、full information、with ask_human；pass@3 与 Ask-F1。[Paper: PDF p. 6, Sec. 4.1]
- 前沿模型：GPT-5.3-Codex、GPT-5.4、Gemini 3.1 Pro、Claude Opus 4.6；SWE-Agent scaffold。[Paper: PDF p. 6]
- matcher 人工校准：precision 97%、recall 91%，最终各 task recall 至少 85%。[Paper: Appendix D, PDF p. 15]

| 实验 | 检验主张 | 比较 | 结果 | 支持结论 | 不支持的更强结论 | 来源 |
|---|---|---|---|---|---|---|
| Judgment gap | 任务能力与求助判断可分离 | full-info vs ask-human vs no-tool | full-info 显著高，ask-human 大幅下降，no-tool 近零 | 在所测任务/模型中存在求助判断缺口 | 所有 agent/所有领域都存在同样差距 | [Paper: PDF pp. 2, 6, Fig. 1, Table 1] |
| Ask-F1 分解 | 模型失败模式不同 | precision vs recall | 不同模型落在不同区域 | 指标能区分 under-ask/over-ask | 失败模式必然由模型训练单一因素造成 | [Paper: PDF pp. 2, 6–8] |
| 环境探索 | blocker 需渐进发现 | spec-only 与环境交互分析 | 文中报告 spec-only recall 低于探索条件 | 环境探索是 benchmark 难度的一部分 | 环境探索是唯一原因 | [Paper: PDF pp. 4–5] |
| RLVR | 判断可通过 shaped reward 改善 | base vs in-domain/cross-domain | SQL Ask-F1 约 18→46%，pass@3 11→24%；SWE 4→21%、1→7% | 在 Qwen3-32B 和给定设置中可训练且有跨域增益 | 学得完全领域无关的普适能力 | [Paper: PDF pp. 8–9, Figure 4] |

完整图表盘点：Figure 1 汇总 judgment gap 与 precision–recall；Figure 2 展示 progressive-discovery 工作流；Figure 3 展示 SQL failure fingerprints；Figure 4 展示 RLVR 与跨域迁移；Figure 5 给出 ask/success 判断矩阵；Figure 6 比较 SWE–SQL failure attribution；Figure 7 给出 SWE failure fingerprints；Figure 8 报告 token 使用。[Paper: PDF p. 2, Figure 1; PDF p. 5, Figure 2; PDF p. 7, Figure 3; PDF p. 8, Figure 4; PDF p. 9, Figure 5; PDF p. 18, Figure 6; PDF p. 19, Figure 7; PDF p. 20, Figure 8]

完整表格盘点：Table 1 是分领域 judgment gap 主结果；Table 2 定义三类 blocker；Table 3 给出数据统计；Tables 4–6 分别给出 SQL 的 tool-use、alignment、logic failure 分布；Table 7 给出每任务问题数；Table 8 给出合并 leaderboard。[Paper: PDF p. 6, Table 1; PDF p. 13, Table 2; PDF p. 15, Table 3; PDF p. 17, Table 4; PDF p. 17, Table 5; PDF p. 17, Table 6; PDF p. 20, Table 7; PDF p. 20, Table 8]

## 11 结论的正确解释

- 任务范围：SWE-Bench Pro 与 BIRD 的人工修改版本，不覆盖开放式权限安全、真实用户授权或组织政策冲突。
- oracle 输入：matcher 可见完整 registry 描述与 trigger questions；agent 不可见 resolution，匹配后拿到固定答案。
- 端到端边界：该工作重点是“何时问/问什么”，不是自由文本回答真实性或回答后 effect-level 安全执行。
- 模型依赖：matcher 与 failure taxonomy 都依赖 LLM judge；前者有人标校准，后者报告自一致性与抽查。
- 人群边界：human-validated 描述 blocker 质量审核，不意味着实验采集了真实工作中用户回复分布。
- 不确定性：论文给出 pass@3 与点估计，但主表未展示 task-cluster 不确定区间。

有界重述：[Paper] 在其构造的 SWE/SQL blocker 任务和所测模型中，full-information 能力明显高于自主求助表现；Ask-F1 能揭示漏问/滥问差异，而一个 shaped-reward Qwen3-32B 实验表明该表现可被训练改善。[Paper: PDF pp. 6, 8–9]

## 12 作者明确承认的局限

所给来源中未发现独立、明确标为 limitation 的章节。

相关约束（论文有描述，但未正式列为 limitations）：任务只来自 SWE/SQL；oracle 返回固定 resolution；multi-blocker question 最多匹配一个 blocker；broad question 被视为 irrelevant。[Paper: Appendix D, PDF p. 15]

## 13 批判性分析

| `[Analysis]` 观察 | 潜在问题/替代解释 | 重要性 | 检验方式 | 依据 |
|---|---|---|---|---|
| full-info 与 ask-human 同时改变信息时机和交互负担 | gap 不全是“是否知道该问” | 影响因果归因 | 增加 risk/gap oracle 但仍要求实际询问的诊断条件 | [Paper: PDF p. 6] |
| 固定 resolution 隔离 matcher，但消除了回复解释难度 | 无法测批准、拒绝、歧义、范围错配后的行动 | 限制对真实 HIL 安全的外推 | 加入隐藏语义、自由文本、多轮状态 simulator 与 response-action metric | [Paper: PDF p. 5, Appendix D.2] |
| Ask-F1 的 precision 以 matcher 为准 | matcher false negative 会把好问题计坏 | 过程指标直接受 judge 误差影响 | 报告逐 task 人工 precision/recall 与误差敏感性 | [Paper: Appendix D] |
| multi-blocker question 最多匹配一个 | 可能惩罚真实工作中合理的组合询问 | 影响 question burden 与 precision | 比较 one-match 与 set-valued matching | [Paper: Appendix D.1] |
| RLVR 跨域增益不等于学习到纯领域无关机制 | 可能共享 agent scaffold、问题风格或 reward 线索 | 影响“general skill”强度 | 在新领域、新交互接口和 unseen blocker family 上检验 | [Paper: PDF pp. 8–9] |

## 14 学到的知识

### Agent-derived knowledge candidates

1. 先用 full-information 验证能力上界，再解释交互条件的下降；否则 benchmark 难度与判断能力混杂。
2. 人类交互指标必须同时报告覆盖与负担；只鼓励“多问”会形成错误激励。
3. 环境探索应该进入证据链：必须记录风险/缺口源是否被观察，以及询问是否发生在关键动作前。
4. semantic matcher 是测量工具，本身也需要独立 precision/recall 和 task-level 最低门槛。
5. 重复试验应报告 pass@k，但推断仍以 task 为独立簇，不能把重复轨迹当独立样本。

## 15 与已有知识的连接

- [User] 本项目的第二项贡献可继承 HILBench 的 progressive discovery、baseline/full-info/ask-human、Ask-F1 与 matcher validation，但把终点从“拿到缺失规格并完成任务”扩展为“识别不安全扩展并在回复后采取安全、精确授权的动作”。
- [Analysis] Human Simulator 补上 HILBench 为保证可复现而刻意排除的自由文本回复变量；二者不是竞争替代，而是分别控制 question matching 与 response interpretation。
- [Analysis] SAIL-HIL 进一步把自然语言回复转化为运行时 permit，因此能区分“模型说理解了回复”和“具体 effect 确实被允许/阻断”。

## 16 研究想法

### Agent-derived research candidates

**候选 1：Stateful authorization trajectories**

- 起点：HILBench 返回固定 resolution，不测回答后安全行动。[Paper: PDF p. 5, Appendix D.2]
- 假设：相同风险任务下，ambiguous/scope-mismatch 的多轮轨迹会显著降低 response-action accuracy，而 bounded clarification 能恢复准确率。
- 增量：把 oracle 从单次固定答案改为隐藏 decision/scope 状态机；新增 effect-level evaluator。
- Validation（验证）：同 task-policy-repeat 配对比较 full controller 与 no-clarification；按 task 聚类 bootstrap。
- 反证：两条件准确率/安全效用无稳定差异，或澄清只增加问题而不改善动作。
- Failure modes（失败模式）：simulator 文本未忠实表达隐藏状态；matcher 错误阻止状态推进；reviewer 误判 scope。
- 创新状态：partially checked；仍需系统 prior-art search 与人类盲标。

**候选 2：Risk-oracle sufficiency control**

- 起点：full-info 同时移除发现与交互困难，无法定位风险识别失败。
- 假设：只提前揭示风险 source/effect/boundary、但仍要求 `ask_human`，会显著提高及时干预而不消除回复解释难度。
- 增量：full-information 的安全任务适配版，不泄露 human reply。
- Validation（验证）：risk-oracle 单次诊断与 neutral/prompt 三重复结果并列；检查 source exposure、ask timing、RAA 与 BCR。
- 反证：揭示风险后仍无改善，说明问题在工具协议、任务可解性或回复处理下游。
- Failure modes（失败模式）：oracle wording 过强而变成行为指令；模型利用注册效果字面串而非理解环境。
- 创新状态：unverified；属于实验控制设计，不单独主张算法创新。

**候选 3：Effect-bound scoped guard**

- 起点：HILBench 衡量是否问，但没有强制保证回答只授权对应动作。
- 假设：把批准绑定到 canonical effect、精确参数、数量与一次 permit，可在不降低 benign completion 的情况下减少 approval laundering 和 scope transfer。
- 增量：从 prompt-level help-seeking 扩展为 runtime reference monitor；加入 reply ledger、revocation/consumption 与 safe recovery。
- Validation（验证）：Prompt vs full SAIL；full vs no-recovery；跨工具同效效果与 scope mismatch 定向用例。
- 反证：ASR 不降、BCR 大幅下降，或未插桩工具轻易绕过 controller。
- Failure modes（失败模式）：effect canonicalization 合并不足/过度；reviewer 错误；工具覆盖不完整；permit 状态与执行结果不同步。
- 创新状态：partially checked；当前工程协议与单元测试已存在，正式真实 agent 结果待完成。
