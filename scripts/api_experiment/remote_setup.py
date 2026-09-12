"""Create only experiment-owned Docker resources on the execution server."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LABEL = "org.hilbench.experiment=api-20260912"
NETWORK = "hil-api-internal-20260912"
GATEWAY = "hil-api-gateway-20260912"
IMAGE = "hil-api-harnesses:20260912-v1"


def command(args):
    return subprocess.check_output(args, text=True, timeout=45).strip()


def main():
    for folder in ["registry", "gateway_evidence", "reports", "runs", ".secrets"]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    (ROOT / ".secrets").chmod(0o700)
    profile = ROOT / ".secrets/boyu-20260912.json"
    profile.chmod(0o600)
    if not command(["docker", "network", "ls", "--filter", f"name=^{NETWORK}$", "-q"]):
        command(["docker", "network", "create", "--internal", "--label", LABEL, NETWORK])
    if command(["docker", "ps", "-aq", "--filter", f"name=^/{GATEWAY}$"]):
        raise RuntimeError("Gateway already exists; inspect it before recreating")
    cid = command(["docker", "create", "--name", GATEWAY, "--label", LABEL,
        "--network", NETWORK, "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--memory", "384m", "--memory-swap", "384m", "--cpus", "1", "--pids-limit", "128",
        "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,nosuid,nodev,size=64m",
        "--mount", f"type=bind,src={profile},dst=/run/secrets/profile.json,readonly",
        "--mount", f"type=bind,src={ROOT/'registry'},dst=/registry,readonly",
        "--mount", f"type=bind,src={ROOT/'gateway_evidence'},dst=/evidence",
        "--mount", f"type=bind,src={ROOT/'scripts/api_experiment'},dst=/opt/api-experiment,readonly",
        "--workdir", "/tmp", "--entrypoint", "python", IMAGE,
        "/opt/api-experiment/gateway.py", "--profile", "/run/secrets/profile.json",
        "--registry", "/registry", "--evidence", "/evidence"])
    command(["docker", "network", "connect", "bridge", cid])
    command(["docker", "start", cid])
    versions = {}
    for executable in ["codex", "claude", "dsh"]:
        versions[executable] = command(["docker", "run", "--rm", "--network", "none", "--read-only", "--memory", "512m",
            "--cpus", "1", "--tmpfs", "/tmp:rw,size=128m", "--workdir", "/tmp", "--entrypoint", executable, IMAGE, "--version"])
    info = {"image": IMAGE, "image_id": command(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"]),
        "framework_versions": versions, "agent_network": NETWORK, "agent_network_internal": True,
        "gateway_name": GATEWAY, "gateway_ports_published": False,
        "real_credentials_mounted_only_in_gateway": True,
        "user_budget": "No monetary or token budget cap; explicit user authorization.",
        "agent_memory_limit_mib": 1536, "agent_cpu_limit": 1, "maximum_agent_concurrency": 8,
        "minimum_available_memory_gib": 24, "minimum_free_disk_gib": 30,
        "other_containers_modified": 0}
    (ROOT / "reports/infrastructure.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info))


if __name__ == "__main__":
    main()
