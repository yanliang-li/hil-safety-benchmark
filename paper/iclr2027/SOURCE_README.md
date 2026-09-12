# InterveneBench — ICLR 2027 working draft

Open main.tex in Overleaf or compile with latexmk -pdf main.tex. Official ICLR 2027 styles, bibliography, generated tables, and vector figures are included. Compiling this package does not require Python, model access, skills, or conversation archives.

This anonymous internal draft studies selective consultation and execution under valid scoped authority. The implemented core contains 250 tasks and four fixed replies. The completed evidence is an 80-case neutral pilot, a matched 80-case prompt-defense comparison, and eight small clean-control runs. The original pilot used Codex with gpt-5.6-luna / medium. A repeated API evaluation with Codex, Claude Code, Hermes Agent, and DeepSeek Harness is documented separately in the appendix. Its two frozen plans contain 5,760 attempts in total; execution status and observed counts are explicitly labeled.

The main table groups six evaluation dimensions. Risk recognition lacks independent annotation; question precision is a rule proxy. Strict correct and safe completion after feedback is 22/26 versus 21/27 across different consulted groups. Lower attack success alone is not uniform improvement across these dimensions.

Figure 1 shows the implemented workflow and four reply contracts. Runs start independently; tool effects are simulated. Figure 2 describes neutral-pilot failure stages. The current defense is a prompt condition. Richer replies, shared-prefix branching, and the SAIL runtime guard are future work. The appendix retains the runtime design and adds factual benchmark-setting comparisons.

The full local workspace contains generation scripts, primary-paper reading notes, hashes, and raw experimental evidence. The package contains no private conversations, credentials, or raw agent traces.

Template source: https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip
