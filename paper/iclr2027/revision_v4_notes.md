# Third-round manuscript contract

Target: anonymous ICLR 2027 benchmark + method paper. Use simple English and the official ICLR format. This revision is an internal draft until the frozen third-round results and author review are complete.

Argument: InterveneBench measures whether an agent asks about an authority gap, uses the actual reply within scope, and completes the original task safely. The first two rounds expose missing consultation, reply misuse, and lost authorized work. The third round tests whether preserving original task authority and recovering unfinished work improves both safety and utility against a fresh prompt baseline. The final clause remains a hypothesis until the experiment is complete.

Terminology: InterveneBench (benchmark); SAIL (method); Prompt (prompt_guard_v1); SAIL v3 (second-round controller); SAIL v4 (third-round controller); BCR (legacy benign completion rate); ASR (unsafe attack success rate); HIL recall (system consultation, with actor/controller attribution); PostSuccess (strict safe completion after matched consultation). Model route names never identify verified underlying model weights. A framework is not a model.

Evidence order and paragraph jobs:

1. Introduction: why human control can fail during tool use; indirect attacks and reply scope; the question and benchmark; the benchmark-to-method test route.
2. Related work: tool behavior and injection; human interaction and authority; task alignment, privilege control and recovery defenses. Credit prior work without claiming the first HIL or recovery mechanism.
3. Benchmark: threat model, confirmable versus prohibited effects, fixed replies, observable metrics and missing semantic labels.
4. Construction: attack surface, systematic family coverage, task variants and split provenance.
5. Method: task contract; original and extended authority; one-use reply permits; cumulative execution history; recovery and completion checks.
6. Experiments: first-round intervention failures; second-round safety/utility tradeoff and diagnosis; third-round equal-scale comparison with a fresh Prompt baseline and corresponding no-human ablation; failures and cost.
7. Discussion: what the combined evidence supports, what independent audit disagreements change, and which claims need real human replies and stronger semantic evaluation.

Main text keeps the central ASR/BCR comparison, primary paired task interval, the second-round utility loss, and any third-round failure that changes the conclusion. All 12 configurations, family-cluster sensitivity, request/token coverage, engineering revisions and detailed audit flags go in the appendix. Do not move contradictory evidence out of the main text.

Known evidence: round one has 5,760 attempts (5,551 valid); round two has 6,720 attempts (6,019 valid). Second-round matched BCR loses 251 pairs and gains 81, net loss 170; invoice and budget tasks account for 169 of that net loss. This is development diagnosis, not validation of the new method.

Third round, corrected by the user before formal start: 6,720 attempts, preserving the exact second-round cases, configurations, repeat allocation and ordered jobs. Prompt 2,880; SAIL v4 2,880; SAIL v4 no-human 960. Already-running engineering r1 remains separate; the r2 check uses only the three active conditions on eight cases (288 attempts). Expanded new-task, clean, fresh-v3 and no-recovery arms are cancelled for this round. Formal outcomes are pending. No result, confidence interval, improvement claim or completion timestamp may be invented.

Figure contract: Python, vector PDF/SVG with editable text and a PNG preview. The method diagram shows the original-authority path, the scoped human decision, and the return to authorized work. It is an explanatory schematic, not outcome evidence. Quantitative figures must show matched ASR/BCR differences, include all specified configurations, identify task-cluster intervals, and separate the three rounds and clean controls. Run source, glyph-size, alignment and collision checks, followed by visual inspection.

Writing references: Agent-SafetyBench connects tool effects to benchmark construction and evaluation. SkillHarm motivates systematic coverage from a concrete attack surface. Unsafer in Many Turns moves from benchmark failure to a defense and ablations. HiL-Bench, HAS-Bench and HumanAgencyBench motivate asking, feedback use and retained human control. These are structural references, not prose templates to copy.

Revision discipline: preserve the previous compiled draft until the integrated revision builds successfully. Replace overlapping explanations rather than continually appending them. Write the abstract last from final observed counts and uncertainty. Retain simulated-effect and synthetic-reply disclosures.

Layout and compression checkpoint: construction is reduced from 503 to 315 whitespace-delimited words, keeping the attack-to-task mechanism, fixed-reply design and semantic-validation limits. Detailed future response tracks and diagnostic traces remain in their existing appendices. The earlier source is preserved privately. Historical inventory is explicitly labeled through round two; third-round status has its own appendix. The corrected result exporter retains a 36-row matrix for the three active conditions across twelve configurations. Packaging rejects oversized floats as well as overfull boxes and undefined references. No official font or margin has been changed.

Scope correction: the third round is a replacement-defense replication of round two. Historical v3 and new v4 are not concurrent arms; each has its own same-round Prompt comparison. New tasks and clean counterparts are prepared future work, not evaluated evidence. No-recovery is an implemented but unused condition in this round. The superseded manuscript and orchestration are preserved privately.
