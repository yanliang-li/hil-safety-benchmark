# InterveneBench v2.2 terminated-run export

The stateful InterveneBench formal run was stopped at the user's request on
2026-09-16. This export preserves the partial experiment without treating it as
a completed matrix.

## Terminal state

| Quantity | Count |
|---|---:|
| Planned attempts | 1,980 |
| Finished attempts | 1,190 |
| Valid runs | 859 |
| Failed runs | 331 |
| Never started | 790 |

The actor-only shard completed all 840 planned attempts (656 valid and 184
failed). The reviewer shard stopped after 350/1,140 terminal attempts (203 valid
and 147 failed); its other 790 run IDs were never registered or executed. At
termination, both launchers were stopped, no experiment container remained,
and every registered run ID had a terminal status file. No terminal attempt was
retried or replaced.

These partial outcomes are not a balanced realization of the frozen 1,980-run
matrix. The included analysis therefore has status `incomplete`. It must not be
used as the paper's final condition comparison without explicitly accounting
for the incomplete reviewer allocation and the high, condition-dependent
failure rate.

## Files

- `experiments/intervene-v1-20260914/`: frozen response banks, simulator
  validation, preflight evidence, formal parent plan, scheduler shards, and
  launch records.
- `reports/intervene-v22-terminated/`: partial summary, per-case rows, all
  planned attempt statuses, final shard progress, and the termination audit.
- `artifacts/intervene-v22-server-snapshot-terminated-20260916-public.tar.gz`: public
  server-side code, experiment inputs, reports, snapshots, and raw run folders
  at termination.

Server snapshot SHA-256:

```text
51c3e5b85a36dc8648ea3aeca38c584de39481aafbe36d62f3dc75719829345f
```

The compressed archive is 25,676,013 bytes. After cloning the repository,
extract it into a new directory rather than over an existing checkout:

```bash
mkdir intervene-v22-server-snapshot
tar -xzf artifacts/intervene-v22-server-snapshot-terminated-20260916-public.tar.gz \
  -C intervene-v22-server-snapshot
```

## Public-export boundary

The GitHub repository is public. The export excludes API and SSH credentials,
private conversation archives, gateway credential evidence, and blinded human
annotation answer keys. Runtime containers received no real API credential;
their raw folders record the benchmark interaction and simulated effects.
