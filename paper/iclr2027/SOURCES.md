# Reference and evidence checks

Checked on 2026-09-12. The manuscript uses primary paper pages to verify titles, author lists, and the specific scope claims below. It avoids an unchecked yes/no coverage matrix and does not claim to have exhaustively ruled out all prior work on authorization-aware human feedback.

| BibTeX key | Primary source | Scope used in the manuscript |
| --- | --- | --- |
| ruan2024toolemu | [ToolEmu](https://arxiv.org/abs/2309.15817) | Agent risk evaluation with an emulated sandbox |
| yuan2024rjudge | [R-Judge](https://aclanthology.org/2024.findings-emnlp.79/) | Risk-awareness evaluation from interaction records |
| zhang2024agentsafetybench | [Agent-SafetyBench](https://arxiv.org/abs/2412.14470) | Broad agent safety and interactive environments |
| andriushchenko2025agentharm | [AgentHarm](https://arxiv.org/abs/2410.09024) | Explicitly malicious requests and agent capabilities; author list updated from the primary page |
| zhan2024injecagent | [InjecAgent](https://aclanthology.org/2024.findings-acl.624/) | Indirect prompt injection through external content |
| debenedetti2024agentdojo | [AgentDojo](https://arxiv.org/abs/2406.13352) | Interactive tasks, attacks, defenses, and extensible evaluation |
| li2026unsafer | [Unsafer in Many Turns](https://arxiv.org/abs/2602.13379) | Multi-turn tool-use risks and ToolShield |
| ning2026skillharm | [SkillHarm](https://arxiv.org/abs/2606.02540) | Skill poisoning across the skill-use lifecycle |
| trinh2026hilbench | [HiL-Bench](https://arxiv.org/abs/2604.09408) | Selective help-seeking and question precision / blocker recall |
| debenedetti2025camel | [CaMeL](https://arxiv.org/abs/2503.18813) | Trusted control flow, untrusted data, and capability-based restrictions |
| wu2026hasbench | [HAS-Bench v1](https://arxiv.org/abs/2607.04329v1) | Configurable human participation, feedback use, control, and approval safety; five agent backends |
| sturgeon2025humanagencybench | [HumanAgencyBench v1](https://arxiv.org/abs/2509.08494v1) | Six agency dimensions; 3,000 queries and twenty assistant models |
| qu2026overeager | [Overeager Coding Agents v1](https://arxiv.org/abs/2605.18583v1) | Benign-task scope violations; four frameworks, six models, fifteen configurations |
| jin2026skillsafetybench | [SkillSafetyBench v3](https://arxiv.org/abs/2605.12015v3) | Skill-facing attacks; 155 attacks, four frameworks, seven models, nine configurations |

The old related-work text included additional defenses and a comparison matrix with unsupported coverage checks. This initial draft narrows the references to claims verified above. It does not claim that HiL-Bench has no response diversity, that InterveneBench includes direct malicious-user attacks, or that the proposed taxonomy is a complete taxonomy of agent attacks.

## Local empirical evidence

- [80-case prompt comparison and eight draft clean-control runs](../../reports/defense-comparison-20260912/README_ZH.md), [paired evidence](../../reports/defense-comparison-20260912/comparison.json), and [manuscript table provenance](defense_results_evidence.json).
- [80-case pilot report](../../reports/gpt_luna_pilot_20260912.md), [raw case results](../../runs/gpt-luna-neutral-80-20260912/), and [audit](../../runs/gpt-luna-neutral-80-20260912/trajectory_audit.json).
- [130-case historical import and verification](../../history/imports/hil-20260912/README.md).
- [Regeneration comparison](../../recovery/generation_comparison.json).
- [Intervention-label and task-contract review](../../docs/intervention_label_review_2026-09-12.md).
- [Clean-control drafts](../../experiments/clean-controls-v1/README.md).

The manuscript restores the original research scope documented in user messages dated 2026-07-25 20:53 and 21:45, and 2026-07-26 10:25. The user clarified on 2026-09-12 that the later rejection/deferral-only design was a deadline compromise and should not define the current work. The [conversation review](REVIEW_ZH.md) records the correction and exact message IDs. The V4 four-response core is implemented; the original aspirations for objectively erroneous advice, partial authorization, shared-prefix branching, and an effect-bound defense are distinguished from completed evidence.

The expanded [12-paper review](../../references/benchmark_review_20260912.md) records construction, main versus ablation counts, and introduction/related-work logic. HiL-Bench counts use v4; HAS-Bench uses v1. The separately reviewed arXiv:2606.08531v3 changed title to ForesightSafety-SAGE; it is not silently cited under its earlier VESTA title.
