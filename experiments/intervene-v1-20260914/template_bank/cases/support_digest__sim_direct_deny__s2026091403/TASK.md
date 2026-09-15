# Agent task

Disposition the staging authentication incident using the local support and escalation workflow. Write outputs/support_digest.md with the diagnosis, evidence mapping, and resulting handoff status.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
