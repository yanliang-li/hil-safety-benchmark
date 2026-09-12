# Scoped HIL method experiments

Three 72-attempt development preflights test native-framework wiring and controller behavior. They are not pooled with the main comparison. Their condition-specific case sets differ.

- `sail-preflight-v1.json`: reviewer exposed to workflow observations.
- `sail-preflight-v2.json`: task-only initial authority and isolated proposal inputs.
- `sail-preflight-v3.json`: distinguish missing authority from a supported hard block, and allow a new actual reply to reopen deferred permission.
- `sail-main-v2.json`: frozen but **never launched**; superseded before execution. See `sail-main-v2-superseded.json`.
- `sail-main-v3.json`: active main plan, 6,720 attempts, four frameworks and three actor model routes. Prompt and full SAIL each have three repeats; no-human SAIL has one. No automatic retries.

The method is described in [docs/sail_method.md](../../docs/sail_method.md). Immutable source and fixture hashes are in each plan. The main launch waits for all preflights to close, verifies replay and reviewer wire inputs, and checks that preflight containers have drained. The gate does not set a safety-performance threshold.

Run `scripts/analyze_sail_v3.py` against the corresponding plan and raw private evidence. Run `scripts/audit_sail_inputs.py` for versions 2 and 3. Public reports retain per-case outcomes, failed-attempt counts, usage, and replay hashes; raw model streams and reviewer request bodies are excluded from publication.

The wrapped native runner's final `run_metadata.json`, immutable `job.json`, and `attempt_status.json` carry the actual method condition. A legacy `failure.json` produced before wrapper finalization can retain the base runner's parser condition name. Analyses use the final metadata and frozen plan, never that legacy condition field.

All runs use the same reused 80 development cases. These plans do not create held-out evidence or validate the entire 1,000-case corpus.
