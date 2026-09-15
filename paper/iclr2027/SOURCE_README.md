# InterveneBench — ICLR 2027 working draft

Compile `main.tex` with a standard LaTeX toolchain. The repository contains the official anonymous style, bibliography, active tables, vector figures, and manuscript sections; compilation requires no model access.

The manuscript studies human-in-the-loop safety for tool-using agents through three connected components: a stateful Human Response Simulator, an agent-safety benchmark spanning consultation and post-response execution, and the SAIL-HIL runtime controller. Conceptual figures illustrate task authority and the consultation-to-execution protocol; they are not measured trajectories.

The paper reports completed historical agent studies separately from the new stateful protocol. The planned 1,980-attempt v2.2 formal run was terminated on 2026-09-16 after 1,190 terminal attempts (859 valid and 331 failed), leaving 790 attempts unstarted. Because this realization is incomplete and unbalanced, its partial outcomes are archived for diagnosis and continuation but are not presented as the final condition comparison.

The manuscript reports safety and utility, consultation and reply use, failures, and overhead. Semantic risk recognition and question correctness still require independent annotation; rule matching remains a proxy. AI assistance is disclosed in the manuscript.

This repository excludes private conversations, credentials, gateway evidence, and blinded human-annotation answer keys. See `../../docs/INTERVENE_V22_TERMINATED_EXPORT.md` for the public server snapshot and exact termination counts.
