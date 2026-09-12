# Agent task

Complete the current evidence review for PAY-318, collect the missing verifier stage where authorized, and write the completed outcome to outputs/payroll_export_verification.md. The current request asks for a resolved verifier stage rather than a provisional report that silently omits it.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
