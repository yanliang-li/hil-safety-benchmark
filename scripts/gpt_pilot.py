#!/usr/bin/env python3
"""Freeze a paired pilot and run it in isolated Docker containers.

Uses existing ChatGPT Codex authentication; no API keys or credentials enter
manifests. Failed attempts never count as safe outcomes. No automatic retries.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("clear_approve", "clear_deny", "ambiguous", "scope_mismatch")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(root, pattern="*"):
    return {str(p.relative_to(root)): sha256(p)
            for p in sorted(root.rglob(pattern)) if p.is_file()}


def save(path, payload):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)


def freeze(args):
    if args.output.exists():
        raise FileExistsError(args.output)
    families = defaultdict(dict)
    tasks = defaultdict(list)
    for p in sorted((ROOT / "data/cases").glob("*/.benchmark/case.json")):
        case = json.loads(p.read_text())
        task = case["task"]
        families[task["attack"]["attack_type"]][task["task_id"]] = task
        tasks[task["task_id"]].append((p.parents[1], case))
    selected = []
    for family, candidates in sorted(families.items()):
        task_id = min(candidates, key=lambda t: hashlib.sha256(
            f"{args.seed}:{t}".encode()).hexdigest())
        variants = tasks[task_id]
        if Counter(c["human_response"]["category"] for _, c in variants) != Counter(CATEGORIES):
            raise ValueError(f"Incomplete/duplicate response pairing: {task_id}")
        if len({json.dumps(c["task"], sort_keys=True) for _, c in variants}) != 1:
            raise ValueError(f"Task content changes across replies: {task_id}")
        for path, case in sorted(variants, key=lambda x: CATEGORIES.index(
                x[1]["human_response"]["category"])):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", case["case_id"]):
                raise ValueError("Unsafe case identifier")
            selected.append({
                "case_id": case["case_id"], "task_id": task_id,
                "attack_family": family, "domain": case["task"]["domain"],
                "authorization_mode": case["task"]["attack"]["authorization_mode"],
                "response_category": case["human_response"]["category"],
                "files": tree_hashes(path),
            })
    manifest = {
        "schema_version": 1, "suite": "hil_safety_1000_v4",
        "selection": "one task per attack family; minimum sha256(seed:task_id); all four replies",
        "seed": args.seed, "case_count": len(selected),
        "task_count": len(families), "model": args.model,
        "reasoning_effort": "medium", "timeout_seconds": 300,
        "conditions": ["neutral", "prompt_guard_v1"],
        "source_files": tree_hashes(ROOT / "src/hil_safety_bench", "*.py"),
        "runner_sha256": sha256(Path(__file__)),
        "cases": selected,
        "interpretation": "Family-balanced exploratory pilot, not an estimate on the full 1000-case distribution.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save(args.output, manifest)
    print(f"Frozen {len(selected)} cases / {len(families)} task clusters: {args.output}")


def validate(manifest):
    if tree_hashes(ROOT / "src/hil_safety_bench", "*.py") != manifest["source_files"]:
        raise ValueError("Source drift: freeze a new manifest for changed code")
    if sha256(Path(__file__)) != manifest["runner_sha256"]:
        raise ValueError("Runner drift: freeze a new manifest")
    for case in manifest["cases"]:
        case_id = case["case_id"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", case_id):
            raise ValueError("Unsafe case identifier")
        if tree_hashes(ROOT / "data/cases" / case_id) != case["files"]:
            raise ValueError(f"Data drift: {case_id}")


def run(args):
    manifest = json.loads(args.manifest.read_text())
    validate(manifest)
    if args.condition not in manifest["conditions"]:
        raise ValueError("Condition not declared in manifest")
    if args.jobs < 1 or args.jobs > 4:
        raise ValueError("Use 1 to 4 concurrent cases")
    auth = Path.home() / ".codex/auth.json"
    if not auth.is_file():
        raise FileNotFoundError("Existing Codex ChatGPT login required")
    image = subprocess.check_output([
        "docker", "image", "inspect", args.image, "--format", "{{.Id}}"
    ], text=True).strip()
    run_root = args.run_root.resolve()
    identity = {"manifest_sha256": sha256(args.manifest),
                "condition": args.condition, "image_id": image}
    experiment_path = run_root / "experiment.json"
    if run_root.exists():
        if not args.resume or not experiment_path.is_file():
            raise FileExistsError("Use a fresh run root, or --resume for this experiment")
        existing = json.loads(experiment_path.read_text())
        if any(existing.get(k) != v for k, v in identity.items()):
            raise ValueError("Cannot resume with a different manifest, condition, or image")
    else:
        run_root.mkdir(parents=True)
        save(experiment_path, dict(identity, model=manifest["model"],
             reasoning_effort=manifest["reasoning_effort"],
             started_at=datetime.now(timezone.utc).isoformat(),
             auth_mode="existing_chatgpt_login", jobs=args.jobs,
             proxy_used=bool(args.proxy_url),
             protocol="per-case read-only Docker, /case and /run-output; original CLI defaults",
             codex_cli=subprocess.check_output([
                 "docker", "run", "--rm", "--network", "none", "--entrypoint",
                 "codex", image, "--version"], text=True).strip()))
        shutil.copyfile(args.manifest, run_root / "manifest.json")
    driver = run_root / "_driver"
    driver.mkdir(exist_ok=True)
    pending = [c["case_id"] for c in manifest["cases"]
               if not (run_root / c["case_id"] / "result.json").is_file()]
    print(f"Pending {len(pending)}/{manifest['case_count']}; {args.condition}; {manifest['model']}", flush=True)

    def run_case(case_id):
        case_run = run_root / case_id
        if case_run.exists() and any(case_run.iterdir()):
            archive = driver / "retry_archive"
            archive.mkdir(exist_ok=True)
            case_run.rename(archive / f"{case_id}.{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}")
        case_run.mkdir(exist_ok=True)
        command = ["docker", "run", "--rm", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--network", "host",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m",
            "--user", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp",
            "-e", "PYTHONPATH=/experiment-src",
            "--mount", f"type=bind,src={auth},dst=/run/secrets/codex-auth.json,readonly",
            "--mount", f"type=bind,src={ROOT / 'src'},dst=/experiment-src,readonly",
            "--mount", f"type=bind,src={ROOT / 'data/cases' / case_id},dst=/case,readonly",
            "--mount", f"type=bind,src={case_run},dst=/run-output"]
        if args.proxy_url:
            for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
                command += ["-e", f"{key}={args.proxy_url}"]
            command += ["-e", "NO_PROXY=localhost,127.0.0.1"]
        command += [image, "run-codex", "/case", "--run-dir", "/run-output",
            "--model", manifest["model"], "--reasoning-effort", manifest["reasoning_effort"],
            "--timeout-seconds", str(manifest["timeout_seconds"]),
            "--condition", args.condition]
        print(f"START {case_id}", flush=True)
        with (driver / f"{case_id}.log").open("w") as log:
            code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT).returncode
        if code == 0 and not (case_run / "result.json").is_file():
            code = 1
        save(driver / f"{case_id}.status.json", {"returncode": code})
        print(f"END {case_id} exit={code}", flush=True)
        return code

    # Submit in bounded waves so an authentication/network failure cannot
    # consume the rest of the pilot. Explicit resume preserves failed attempts.
    failed = False
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for offset in range(0, len(pending), args.jobs):
            codes = list(pool.map(run_case, pending[offset:offset + args.jobs]))
            completed = sum((run_root / c["case_id"] / "result.json").is_file()
                            for c in manifest["cases"])
            save(run_root / "progress.json", {"planned": manifest["case_count"],
                 "completed": completed, "last_wave_failed": any(codes)})
            if any(codes):
                failed = True
                break
    if failed:
        raise SystemExit("Stopped after infrastructure failure; inspect _driver logs before --resume")
    print("All planned cases completed. Summarize and audit before interpreting results.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("freeze")
    prepare.add_argument("--output", type=Path, required=True)
    prepare.add_argument("--seed", type=int, default=42)
    prepare.add_argument("--model", default="gpt-5.6-luna")
    execute = sub.add_parser("run")
    execute.add_argument("manifest", type=Path)
    execute.add_argument("--run-root", type=Path, required=True)
    execute.add_argument("--condition", choices=["neutral", "prompt_guard_v1"], default="neutral")
    execute.add_argument("--jobs", type=int, default=2)
    execute.add_argument("--image", default="hil-safety-bench:latest")
    execute.add_argument("--proxy-url")
    execute.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    (freeze if args.command == "freeze" else run)(args)


if __name__ == "__main__":
    main()
