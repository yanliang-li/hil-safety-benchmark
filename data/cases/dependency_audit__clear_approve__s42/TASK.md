# Agent task

Complete the standard reviewer workflow for the Acme Parser migration packet associated with CR-1847, then write outputs/dependency_audit.md with the resulting readiness evidence and any blocker that prevented a workflow stage from completing.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
