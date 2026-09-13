# Engineering revision 3: clarify the existing review schema

Before formal execution, revision 2 could not satisfy the predeclared configuration-coverage gate: Codex/deepseek-v4-flash/full and DeepSeek Harness/glm-5.2/full each closed all eight engineering attempts without a valid episode. At the 247-closed diagnostic snapshot, 136 review responses failed consequential_effect_tool, 24 failed constraint_not_in_task, and 13 failed reviewer_incomplete_output across stages. These are protocol/runtime findings, not ASR/BCR selection.

The existing contract validator permits only consequential tools in effects. The reviewer frequently added local write_output there instead of only in obligations. Revision 3 states the exact permitted tool list, supplies a local-report obligation example, explains the existing literal-string rule for exact_arguments, and includes these schema reminders in the already-bounded one-correction feedback. Validation, authorization decisions, cumulative budgets, human replies, scoring, data, model routes and actor limits are unchanged. The previous sources and all attempts remain archived.

Several DeepSeek Harness/glm-5.2 failures spent their full 4,096 output-token allowance in reasoning before emitting a useful next action. The allowance is preserved to match the second round; such failures remain failures. This separate model/route behavior is not claimed to be fixed by schema clarification.

The final bounded engineering revision repeats the same eight development cases, twelve framework/model combinations and three conditions once, for 288 new engineering attempts with distinct IDs. All are excluded from formal rates. The unchanged gate requires complete accounting, valid input provenance and at least one valid episode per configuration/condition, never a success-rate threshold. No fourth engineering revision is scheduled automatically. Formal scope remains 5,760 main attempts followed by 960 no-human ablation attempts.

The user-requested scheduling amendment starts r3 and formal execution at 96 concurrent episodes and conditionally trials 128. Capacity changes never relax the engineering gate or replace failed attempts.
