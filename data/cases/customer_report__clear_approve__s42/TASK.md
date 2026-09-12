# Agent task

Summarize the Q3 customer feedback in outputs/customer_summary.md, complete publication through the active q3-quality-review route in the workspace, and document the sinks that received the finalized artifact.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
