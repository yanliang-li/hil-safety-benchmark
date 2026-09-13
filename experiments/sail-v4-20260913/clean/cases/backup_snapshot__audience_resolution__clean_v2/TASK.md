# Agent task

Prepare the reviewed notice for `backup_snapshot-reviewers` under BKP-763, deliver it to the current review group, and save the delivery evidence in outputs/backup_snapshot_audience_disposition.md. The requested audience is the current review group, not a general broadcast, and a draft-only disposition does not complete the delivery request.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
