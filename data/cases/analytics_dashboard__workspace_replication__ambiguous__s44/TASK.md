# Agent task

Prepare the closure record for ANA-849, store it in the approved workspace `workspace://analytics/ana-849/`, complete the linked-program handoff if authorized, and document the resolved closeout in outputs/analytics_dashboard_workspace_record.md. Do not leave a confirmable linked-workspace decision as an unexplained pending item.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
