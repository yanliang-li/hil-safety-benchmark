"""Probe all text candidates with bounded concurrency; not benchmark scoring."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from remote_setup import ROOT, LABEL, NETWORK, GATEWAY, IMAGE


def run_model(model):
    run_id = "probe_" + hashlib.sha256(model.encode()).hexdigest()[:14]
    directory = ROOT / "runs/probes" / run_id
    directory.mkdir(parents=True, exist_ok=True)
    (ROOT / "registry" / f"{run_id}.json").write_text(json.dumps({"model": model, "purpose": "tool_compatibility", "max_requests": 2}))
    command = ["docker", "run", "--name", run_id, "--label", LABEL,
        "--network", NETWORK, "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--memory", "256m", "--memory-swap", "256m", "--cpus", "0.5", "--pids-limit", "64",
        "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,nosuid,nodev,size=32m",
        "--mount", f"type=bind,src={directory},dst=/run-output",
        "--mount", f"type=bind,src={ROOT/'scripts/api_experiment'},dst=/opt/api-experiment,readonly",
        "--workdir", "/tmp", "--entrypoint", "python", IMAGE, "/opt/api-experiment/probe.py",
        "--model", model, "--base-url", f"http://{GATEWAY}:8080/r/{run_id}/v1", "--output", "/run-output/probe.json"]
    try:
        process = subprocess.run(command, text=True, capture_output=True, timeout=410)
        (directory / "container_stdout.log").write_text(process.stdout)
        (directory / "container_stderr.log").write_text(process.stderr)
        result = json.loads((directory / "probe.json").read_text()) if (directory / "probe.json").exists() else {"requested_model": model, "failure": "container_error"}
    except subprocess.TimeoutExpired:
        result = {"requested_model": model, "failure": "container_timeout"}
    finally:
        subprocess.run(["docker", "rm", "-f", run_id], capture_output=True, timeout=20)
    return {k: v for k, v in result.items() if k != "requests"}


def main():
    catalog = json.loads((ROOT / "endpoint_catalog.json").read_text())
    ids = [m["id"] for m in catalog["models"]]
    excluded = [m for m in ids if any(w in m.lower() for w in ["embedding", "seedance", "seedream", "qwen-image"])]
    models = sorted(set(ids) - set(excluded))
    output = {"started_unix": time.time(), "purpose": "compatibility only, not safety evaluation",
              "candidates": models, "excluded_non_text": excluded, "concurrency": 4, "results": []}
    dest = ROOT / "reports/compatibility.json"
    dest.write_text(json.dumps(output, indent=2) + "\n")
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(run_model, model) for model in models]
        for future in as_completed(jobs):
            result = future.result()
            output["results"].append(result)
            dest.write_text(json.dumps(output, indent=2) + "\n")
            print(json.dumps(result), flush=True)
    output["finished_unix"] = time.time()
    dest.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
