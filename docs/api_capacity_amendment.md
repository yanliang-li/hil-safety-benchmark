# API experiment capacity amendment

The owner has subsequently authorized a [staged 96/128-agent ramp](capacity_ramp.md). The earlier capacity procedure below remains part of the execution history.

Current execution is governed by the later [64-agent amendment](capacity64.md). This document retains the preceding capacity history.

The original 4,320-attempt manifest freezes eight concurrent agents. The owner subsequently requested more parallel agents after inspecting available server memory. `capacity-amendment-v1.json` records this operational change separately; the original manifest and its source hashes remain intact.

`scripts/schedule_api_capacity.py` uses the original, hash-verified `run_one` implementation. It resumes the same attempt IDs and preserves both successful and failed attempts. A registered attempt without a final status prevents restart until it is inspected. The original controller must be drained before replacement. The new scheduler acquires the same process lock, preventing two controllers from submitting the same jobs.

The initial evaluation stages are 16 and 32 agents. Each agent retains its 1 CPU, 1,536 MiB memory limit, 900-second timeout, 48-request limit, image, MCP tools, task prompt, and defense condition. The relay allows 40 in-flight upstream requests and has a 1 GiB memory limit and 2 CPU limit. Its capacity wrapper loads the original gateway only after checking its SHA-256; request bodies, streaming responses, authorization, and evidence capture use the original implementation.

Before new launches, the capacity scheduler requires at least 64 GiB available host memory, 30 GiB free disk space, and one-minute host load below 75% of the logical CPU count. `STOP_NEW_RUNS` still pauses future launches. Reducing the target allows active attempts to finish; it does not kill them.

The live target is an atomic JSON file at `reports/capacity-control.json`. This target covers the original three-framework pool. While the [Hermes extension](hermes_extension.md) has eight workers, keep this target at **24** so the aggregate limit remains 32. The following example selects 32 original-pool workers only when no Hermes workers are active:

```python
import json
from pathlib import Path

path = Path("reports/capacity-control.json")
control = json.loads(path.read_text())
control.update(agent_concurrency=32, epoch="capacity-32")
temporary = path.with_suffix(".tmp")
temporary.write_text(json.dumps(control, indent=2) + "\n")
temporary.replace(path)
```

Keep the relay name and its declared 40-request capacity unchanged while attempts are running. The scheduler accepts at most 48 agents; this is a software bound, not a measured recommendation. Extra agents beyond the relay's capacity can queue and may reduce useful throughput.

`reports/capacity-history.json` records effective times and closed-attempt counts. Each new attempt stores its capacity epoch and target. `scripts/report_api_capacity.py` reports completed and valid attempts per hour, failures, API status codes, and API latency. `all_attempts.csv` retains the epoch for later stratification. Throughput windows have different task/model mixes and startup effects; a short-window ratio is an operational estimate, not a controlled performance comparison. Capacity can affect provider behavior, so the change must also be disclosed with the safety results.

A later [four-framework capacity amendment](../experiments/api-multimodel-20260912/four-framework-capacity-amendment-v1.json) permits a 40-agent trial after the initial 32-agent observation: 32 original-pool workers and eight Hermes workers, coordinated by the amended Hermes scheduler. The earlier frozen Hermes launcher must first drain and stop; it is not compatible with that allocation.

The 40-agent trial was subsequently ended after a burst of upstream connection failures. Execution resumed at **32 aggregate agents (24 original + eight Hermes)** after connectivity checks. See the [follow-up record](../reports/api-multimodel-20260912/four-frameworks/capacity40-followup.json); the early throughput checkpoint is not evidence of stable acceleration.
