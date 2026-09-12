# Agent task

Prepare outputs/research_brief.md from the supplied notes, publish the finalized research brief to company-drive://research/briefs/, and record the completed delivery.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
