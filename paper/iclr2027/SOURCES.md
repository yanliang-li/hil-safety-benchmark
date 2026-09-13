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

## Related-work restoration, 2026-09-13

The two-subsection organization and defense literature were restored from the
2026-07-27 14:04 archived draft. [Restoration notes](RELATED_WORK_RESTORE_20260913.md)
identify the source messages and the adaptations to the current manuscript.
The following eight entries were checked against primary paper or proceedings
pages before being added to `references.bib`. This check covers identity,
author order, publication metadata used in the entry, and the narrow scope
description in Related Work; it is not a new systematic literature review.

| BibTeX key | Primary source | Scope used in the restored section |
| --- | --- | --- |
| inan2023llamaguard | [Llama Guard](https://arxiv.org/abs/2312.06674) | Classification of safety risks in prompts and responses |
| han2024wildguard | [WildGuard](https://arxiv.org/abs/2406.18495) | Prompt and response moderation; NeurIPS 2024 version |
| zeng2024shieldgemma | [ShieldGemma](https://arxiv.org/abs/2407.21772) | Content moderation for user inputs and generated outputs |
| chen2025struq | [StruQ, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/chen-sizhe) | Structured prompt/data separation and defensive training |
| chen2025secalign | [SecAlign](https://arxiv.org/abs/2410.05451) | Preference optimization for resistance to injected instructions; ACM CCS 2025 and proceedings DOI identified on the paper page |
| zhan2025adaptive | [Adaptive Attacks, NAACL Findings 2025](https://aclanthology.org/2025.findings-naacl.395/) | Testing prompt-injection defenses with adaptive attacks; not evidence that every later defense is broken |
| xiang2025guardagent | [GuardAgent, ICML 2025](https://proceedings.mlr.press/v267/xiang25a.html) | Translating guard requests into executable checks on agent behavior |
| toolsafe2026 | [ToolSafe](https://arxiv.org/abs/2601.10156) | Proactive detection and feedback for unsafe tool invocations |

The archived blanket gap statement about absent or unstructured human approval
was not restored. [Progent v3](https://arxiv.org/abs/2504.11703v3) explicitly requires
approval for privilege expansion. [SafeAgent](https://arxiv.org/abs/2604.17562v1)
already combines runtime control with recovery. These entries remain in the
section, and [HAS-Bench](https://arxiv.org/abs/2607.04329v1) remains credited for
feedback and human control. The SAIL description follows the current method:
reviewed extensions receive one-use permits; semantic review is fallible and
general cross-tool equivalence is not formally verified.
