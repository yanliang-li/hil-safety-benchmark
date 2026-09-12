# InterveneBench — ICLR 2027 working draft

Compile main.tex with latexmk -pdf or upload this ZIP to Overleaf. The official anonymous ICLR 2027 styles, bibliography, tables, and vector figures are included. No Python, model access, skill installation, private conversations, or credentials are needed to compile.

The paper evaluates human intervention under indirect workflow attacks. Its executable core contains 250 tasks and four fixed replies each. The completed prompt study contains 5,760 attempts across four native frameworks and three requested model routes, with 5,551 valid results. Earlier GPT pilot results remain separate in the appendix.

SAIL checks initial task authority, asks a scoped question when permission is missing, verifies the actual reply, and binds permission to one reviewed call. A separately frozen comparison tests SAIL against a fresh prompt control and a no-human ablation. The manuscript explicitly marks whether that comparison has finished; only completed main results enter its result section. All engineering preflights remain separate.

The six evaluation dimensions include two unresolved semantic annotation needs: autonomous risk recognition and semantic question correctness. Rule matching is only a proxy. Human replies are synthetic fixtures, task effects are simulated, and the 80-case evaluation reuses development tasks. Richer feedback and held-out validation remain necessary.

Template source: https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip
