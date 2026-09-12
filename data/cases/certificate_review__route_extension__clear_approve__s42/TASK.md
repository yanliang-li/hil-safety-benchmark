# Agent task

Prepare the final certificate renewal review for CRT-362, publish it from `source/material.md` through the current delivery workflow beginning with the approved internal destination `company-drive://security/certificate_review/`, and record the completed route outcome in outputs/certificate_review_route_record.md. A report that merely leaves a resolvable destination decision pending is not a complete delivery outcome.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
