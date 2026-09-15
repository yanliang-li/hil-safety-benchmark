"""Launch a frozen InterveneBench plan in isolated native-agent containers."""
from __future__ import annotations

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = Path("/home/root123/hil-api-experiments-20260912")
REGISTRY = LEGACY_ROOT / "registry"
GATEWAY = "hil-api-gateway-capacity-ramp-20260912"
NETWORK = "hil-api-internal-20260912"
DIRECT_CONDITIONS = {"neutral", "prompt_guard_v1", "risk_oracle"}


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def ready() -> bool:
    available_kib = int(
        next(
            line.split()[1]
            for line in Path("/proc/meminfo").read_text().splitlines()
            if line.startswith("MemAvailable:")
        )
    )
    return (
        available_kib / 1024**2 >= 48
        and shutil.disk_usage(ROOT).free >= 80 * 1024**3
        and os.getloadavg()[0] < 0.9 * os.cpu_count()
        and not (ROOT / "STOP_INTERVENE").exists()
    )


def snapshot(plan_path: Path, plan: dict) -> Path:
    digest = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    destination = ROOT / "snapshots" / digest
    if destination.exists():
        return destination
    (destination / "method").mkdir(parents=True)
    for package in ("hil_guard_v3", "hil_guard_v4", "hil_guard_hil"):
        shutil.copytree(
            ROOT / "scripts" / package,
            destination / "method" / package,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    shutil.copytree(
        ROOT / "src/hil_safety_bench",
        destination / "intervene-src/hil_safety_bench",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    (destination / "frozen-runners").mkdir()
    shutil.copy2(
        ROOT / "scripts/api_experiment/run_case.py",
        destination / "frozen-runners/run_case.py",
    )
    shutil.copy2(
        ROOT / "scripts/hermes_experiment/run_case.py",
        destination / "frozen-runners/hermes_run_case.py",
    )
    save(
        destination / "snapshot.json",
        {
            "plan_sha256": digest,
            "created_unix": time.time(),
            "source_sha256": plan["source_sha256"],
        },
    )
    return destination


def run_one(job: dict, frozen: Path) -> dict:
    folder = ROOT / "runs" / job["stage"] / job["run_id"]
    status = folder / "attempt_status.json"
    if status.exists():
        return json.loads(status.read_text())
    folder.mkdir(parents=True, exist_ok=True)
    registration = REGISTRY / f"{job['run_id']}.json"
    if registration.exists():
        raise RuntimeError("Registered unfinished attempt cannot be retried")
    save(
        registration,
        {
            "model": job["model"],
            "max_requests": 48,
            "purpose": "intervenebench-formal",
            "agent": job["agent"],
        },
    )
    if job["condition"] not in DIRECT_CONDITIONS:
        save(
            REGISTRY / f"{job['run_id']}_guard.json",
            {
                "model": "deepseek-v4-flash",
                "max_requests": 24,
                "purpose": "intervenebench-sail-reviewer",
                "agent": "sail-reviewer",
            },
        )
    save(folder / "job.json", job)
    result = dict(job, started_unix=time.time(), completed=False)
    command = [
        "docker",
        "run",
        "--name",
        job["run_id"],
        "--label",
        "org.hilbench.experiment=intervene-v1-20260914",
        "--network",
        NETWORK,
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--memory",
        "1536m",
        "--memory-swap",
        "1536m",
        "--cpus",
        "1",
        "--pids-limit",
        "160",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--tmpfs",
        "/tmp:rw,nosuid,nodev,size=512m",
        "--tmpfs",
        f"/home/benchmark:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}",
        "--tmpfs",
        f"/home/node:rw,nosuid,nodev,size=128m,uid={os.getuid()},gid={os.getgid()}",
        "--mount",
        f"type=bind,src={ROOT / job['case_root'] / job['case_id']},dst=/case,readonly",
        "--mount",
        f"type=bind,src={folder},dst=/run-output",
        "--mount",
        f"type=bind,src={frozen / 'method'},dst=/opt/hil-method,readonly",
        "--mount",
        f"type=bind,src={frozen / 'intervene-src'},dst=/opt/intervene-src,readonly",
        "--mount",
        f"type=bind,src={frozen / 'frozen-runners'},dst=/opt/frozen-runners,readonly",
        "--env",
        "PYTHONPATH=/opt/intervene-src:/opt/hil-method:/opt/hilbench-src/src",
        "--entrypoint",
        "/opt/hilbench-venv/bin/python",
        job["image_id"],
        "-m",
        "hil_guard_hil.run_case",
        "--agent",
        job["agent"],
        "--model",
        job["model"],
        "--condition",
        job["condition"],
        "--run-id",
        job["run_id"],
        "--repeat",
        str(job["repeat"]),
        "--timeout",
        str(job["timeout"]),
        "--base-url",
        f"http://{GATEWAY}:8080/r/{job['run_id']}/v1",
    ]
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=job["timeout"] + 90,
        )
        (folder / "container_stdout.log").write_text(process.stdout)
        (folder / "container_stderr.log").write_text(process.stderr)
        result["container_returncode"] = process.returncode
        metadata = folder / "run_metadata.json"
        if metadata.exists():
            meta = json.loads(metadata.read_text())
            result.update(
                completed=meta.get("scorable", False) and process.returncode == 0,
                guard_invalid=meta.get("guard_invalid", False),
                event_count=meta.get("benchmark_event_count", 0),
            )
        state = subprocess.run(
            ["docker", "inspect", job["run_id"], "--format", "{{json .State}}"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if state.returncode == 0:
            docker = json.loads(state.stdout)
            save(folder / "docker_state.json", docker)
            result["oom_killed"] = docker.get("OOMKilled", False)
            if result["oom_killed"]:
                result["completed"] = False
    except Exception as error:
        result["scheduler_failure"] = type(error).__name__
    finally:
        try:
            subprocess.run(
                ["docker", "rm", "-f", job["run_id"]],
                capture_output=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            result["container_cleanup_timeout"] = True
    result["finished_unix"] = time.time()
    save(status, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--concurrency", type=int, default=32)
    args = parser.parse_args()
    if not 1 <= args.concurrency <= 64:
        raise ValueError("concurrency must be between 1 and 64")
    plan = json.loads(args.plan.read_text())
    for relative, expected in plan["source_sha256"].items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError("Frozen source mismatch: " + relative)
    for case in plan["cases"]:
        for relative, expected in case["files"].items():
            path = ROOT / case["case_root"] / case["case_id"] / relative
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError("Frozen case mismatch: " + case["case_id"])
    if len({job["run_id"] for job in plan["jobs"]}) != len(plan["jobs"]):
        raise ValueError("Duplicate run IDs")
    frozen = snapshot(args.plan, plan)
    reports_root = ROOT / "reports"
    reports_root.mkdir(parents=True, exist_ok=True)
    lock = (reports_root / (args.plan.stem + ".lock")).open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    results, queue = [], []
    for job in plan["jobs"]:
        status = ROOT / "runs" / job["stage"] / job["run_id"] / "attempt_status.json"
        if status.exists():
            results.append(json.loads(status.read_text()))
        elif (REGISTRY / f"{job['run_id']}.json").exists():
            raise RuntimeError("Refusing automatic retry of registered attempt")
        else:
            queue.append(job)
    progress = reports_root / (args.plan.stem + "_progress.json")
    report = {
        "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        "started_unix": time.time(),
        "planned": len(plan["jobs"]),
        "results": results,
        "active": 0,
        "queued": len(queue),
        "concurrency": args.concurrency,
    }
    pool = ThreadPoolExecutor(max_workers=args.concurrency)
    active = {}
    while queue or active:
        can_launch = ready()
        while can_launch and queue and len(active) < args.concurrency:
            job = queue.pop(0)
            active[pool.submit(run_one, job, frozen)] = job
        done, _ = (
            wait(active, timeout=3, return_when=FIRST_COMPLETED)
            if active
            else (set(), set())
        )
        for future in done:
            job = active.pop(future)
            try:
                item = future.result()
            except Exception as error:
                item = dict(
                    job,
                    completed=False,
                    finished_unix=time.time(),
                    scheduler_failure=type(error).__name__,
                )
                save(
                    ROOT / "runs" / job["stage"] / job["run_id"] / "attempt_status.json",
                    item,
                )
            results.append(item)
        report.update(
            active=len(active),
            queued=len(queue),
            finished_attempts=len(results),
            valid_runs=sum(item.get("completed", False) for item in results),
            checked_unix=time.time(),
            resource_pause=not can_launch,
        )
        save(progress, report)
        if done:
            print(
                json.dumps(
                    {key: value for key, value in report.items() if key != "results"}
                ),
                flush=True,
            )
        if not active and queue:
            time.sleep(3)
    pool.shutdown()
    report["finished_unix"] = time.time()
    save(progress, report)


if __name__ == "__main__":
    main()
