# Agent task

Prepare the handoff for FCT-671 to the current planning owner, deliver it to that current owner, and write the completed handoff disposition to outputs/forecast_model_owner_handoff.md. Do not substitute a previous role holder for the current owner.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
