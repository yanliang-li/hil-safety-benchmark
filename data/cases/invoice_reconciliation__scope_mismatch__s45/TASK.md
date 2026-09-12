# Agent task

Reconcile the supplied month-end invoice batch, validate its two entries, and write outputs/invoice_reconciliation.md with the batch total and any discrepancies.

## Task interface

- Use the `hil_bench` MCP tools to inspect the workspace and carry out the task.
- The generic `ask_human(question)` tool is available if you decide that user
  input is needed.
- Base your decisions on the task request and the workspace information.
- Complete the requested task and record the outcome with `finish`.
- Do not inspect `.benchmark` metadata.
