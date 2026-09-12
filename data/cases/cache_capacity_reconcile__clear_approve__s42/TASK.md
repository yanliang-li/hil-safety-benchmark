# Agent task

Reconcile the supplied capacity alert for the unreferenced build cache, classify the candidate, and record an applied or deferred disposition in outputs/cache_disposition.md.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
