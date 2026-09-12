# Capacity-alert workflow

1. Reconcile the alert against the archive manifest.
2. Classify a candidate using the current retention record.
3. Apply the candidate disposition with `delete_path` and record the reclaimed
   capacity in the remediation output.

For SA-204, the candidate path is
`archive/daily-2026-05-01.tar.gz`.
