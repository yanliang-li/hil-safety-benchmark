# Human Response Simulator v2.2 freeze report

Freeze date: 2026-09-14 (Asia/Shanghai)

## Frozen artifact

- Suite: `intervenebench_simulator_v2_2`
- Scale: 20 tasks × 6 stateful policies = 120 cases, containing 200 reply turns.
- Cases SHA-256: `1c77bed9dc899683841dd4d37a58a581fd3a951afd73eac52d7848172e2a3a6e`.
- Suite-manifest SHA-256: `2604894b76a34e944ff959176d1b9fd1f75d09824c7578483f7fdb0f680c566b`.
- Construction-audit SHA-256: `8dd3d97bdcb9e9d74d6c6be67b152cbf66bb1a3557277362eefb0de90492fa4f`.
- Simulator-audit SHA-256: `c7a018792147689e907035eb730e4bcd776f48d2e44f6357afd44636a29c5db2`.

The deterministic audits pass all task/policy invariants. The bank contains one
case per task-policy pair, no degenerate reply, no construction-contract
violation, 98.5% unique reply strings, Distinct-1 of 0.171, and Distinct-2 of
0.482. These lexical checks do not establish realism.

## Blind model audit

The final audit uses the separately registered `glm-5.2` route and rubric
`blind-semantics-v3`. The judge sees the original task, proposed action, and
reply text, but not construction labels. It covers all 120 cases and 200 turns:

| Measure | Result |
|---|---:|
| Decision accuracy | 98.5% |
| Strict scope accuracy | 95.5% |
| Strict decision-and-scope fidelity | 95.5% |
| Authorization-equivalent fidelity | 98.5% |
| All-turn sequence fidelity | 92.5% |
| Sequence coherence (100% coverage) | 100.0% |
| Context consistency | 100.0% |
| Label-leak rate | 0.0% |
| Mean naturalness | 4.235 / 5 |

Authorization-equivalent fidelity treats `invalid/nearby` and `invalid/none`
as equivalent only when both encode an answer about another action and neither
authorizes the target. Strict scope fidelity remains reported. The summary
SHA-256 is `1549e4a2eb7ed3bad50d4334ca5fa97390be037f6004d697373aba73a36d88c9`.

## Immutable repair history

The original contextual v2 bank was generated once per retained case. A frozen
rubric selected 16 cases for v2.1 repair; an additional seven cases were selected
for v2.2 before the final bank was frozen. Each repair was generated into a new
directory and merged by task-policy identity. No prior bank was overwritten.

The v2 formal route records 114 complete calls after a six-case pilot. The v2.1
repair route records 17 complete calls: 16 retained replies and one response
excluded because a container UID error prevented it from being cached. The v2.2
repair route records seven complete retained calls. Earlier judge rubrics and
their outputs remain preserved as development evidence; only rubric v3 is used
for the formal experiment gate.

## Evidence boundary

The results above are independent-model proxy judgments, not human ratings. A
balanced blinded file with ten dialogues per policy is ready for at least two
human annotators under `docs/HUMAN_SIMULATOR_ANNOTATION_PROTOCOL.md`. Until that
annotation is completed, the defensible claim is that the simulator provides
controlled, stateful, context-grounded reply variation—not that it represents a
population distribution of real users.
