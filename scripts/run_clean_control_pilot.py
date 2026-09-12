#!/usr/bin/env python3
"""Run the four existing clean-control drafts in separate Docker conditions.

Uses the existing authorized Codex login. The legacy compatibility scores are
preserved but must never enter the attack-suite HIL/ASR aggregate.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SPLIT = ROOT / "experiments/clean-controls-v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=["neutral", "prompt_guard_v1"], required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--image", default="hil-safety-bench:latest")
    parser.add_argument("--proxy-url")
    parser.add_argument("--jobs", type=int, choices=[1, 2, 3, 4], default=4)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((SPLIT / "manifest.json").read_text())
    main_manifest = json.loads((ROOT / "experiments/gpt-luna-pilot-80-v1.json").read_text())
    if manifest["legacy_aggregate_eligible"] is not False or manifest["case_count"] != 4:
        raise ValueError("Expected the frozen four-case draft control split")
    for case in manifest["cases"]:
        base = SPLIT / "cases" / case["case_id"]
        actual = {str(p.relative_to(base)): sha(p) for p in sorted(base.rglob("*")) if p.is_file()}
        if actual != case["files"]:
            raise ValueError(f"Control data drift: {case['case_id']}")
    source = ROOT / "src/hil_safety_bench"
    current = {str(p.relative_to(source)): sha(p) for p in sorted(source.rglob("*.py"))}
    if current != main_manifest["source_files"]:
        raise ValueError("Source differs from the main pilot")
    if args.check_only:
        print("Four clean fixtures and benchmark source hashes verified; no model calls.")
        return
    run_root = args.run_root.resolve()
    if run_root.exists():
        raise FileExistsError("Use a fresh run root; this eight-run diagnostic has no automatic retries")
    auth = Path.home() / ".codex/auth.json"
    if not auth.is_file():
        raise FileNotFoundError("Previously authorized Codex login is missing")
    image = subprocess.check_output(
        ["docker", "image", "inspect", args.image, "--format", "{{.Id}}"], text=True
    ).strip()
    if image != "sha256:b4f7053768e6c9781a549866d4498b9d45570af8255294c3a9c1c3c513c68022":
        raise ValueError("Use the same frozen image as the main pilot")
    run_root.mkdir(parents=True)
    (run_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    experiment = {
        "model": main_manifest["model"], "reasoning_effort": main_manifest["reasoning_effort"],
        "condition": args.condition, "image_id": image, "case_count": 4,
        "split": manifest["split"], "legacy_aggregate_eligible": False,
        "runner_sha256": sha(Path(__file__)),
        "manifest_sha256": sha(SPLIT / "manifest.json"),
        "evaluation_plan_sha256": sha(SPLIT / "evaluation_plan_20260912.json"),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source_files": current,
        "auth_mode": "existing_chatgpt_login",
        "protocol": "per-case read-only Docker, /case and /run-output; same core runner as attack pilot",
    }
    (run_root / "experiment.json").write_text(json.dumps(experiment, indent=2) + "\n")
    driver = run_root / "_driver"
    driver.mkdir()

    def run_case(case):
        case_id = case["case_id"]
        output = run_root / case_id
        output.mkdir()
        command = [
            "docker", "run", "--rm", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--network", "host",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m",
            "--user", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp",
            "-e", "PYTHONPATH=/experiment-src",
            "--mount", f"type=bind,src={auth},dst=/run/secrets/codex-auth.json,readonly",
            "--mount", f"type=bind,src={ROOT / 'src'},dst=/experiment-src,readonly",
            "--mount", f"type=bind,src={SPLIT / 'cases' / case_id},dst=/case,readonly",
            "--mount", f"type=bind,src={output},dst=/run-output",
        ]
        if args.proxy_url:
            for key in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
                command += ["-e", f"{key}={args.proxy_url}"]
            command += ["-e", "NO_PROXY=localhost,127.0.0.1"]
        command += [
            image, "run-codex", "/case", "--run-dir", "/run-output",
            "--model", main_manifest["model"], "--reasoning-effort", main_manifest["reasoning_effort"],
            "--timeout-seconds", "300", "--condition", args.condition,
        ]
        print(f"START {case_id} {args.condition}", flush=True)
        with (driver / f"{case_id}.log").open("w") as log:
            code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT).returncode
        if code == 0 and not (output / "result.json").is_file():
            code = 1
        (driver / f"{case_id}.status.json").write_text(json.dumps({"returncode": code}) + "\n")
        print(f"END {case_id} exit={code}", flush=True)
        return code

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for offset in range(0, len(manifest["cases"]), args.jobs):
            codes = list(pool.map(run_case, manifest["cases"][offset:offset + args.jobs]))
            if any(codes):
                raise SystemExit("Infrastructure failure; preserve these attempts and inspect logs")
    print("Four control runs completed. Score clean utility separately from the attack benchmark.", flush=True)


if __name__ == "__main__":
    main()
