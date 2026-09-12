from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .evaluate import CaseResult, evaluate_run, write_result
from .conditions import apply_condition
from .runtime import BenchmarkRuntime
from .schemas import EffectSpec


def run_scripted_agent(
    case_dir: Path,
    run_dir: Path,
    *,
    behavior: Literal["safe", "vulnerable"] = "safe",
) -> CaseResult:
    """Run a deterministic smoke-test agent.

    This agent is not a benchmark baseline: it reads case metadata through the
    runtime object. It exists only to verify generation, tools, event logging,
    and scoring without an external model.
    """
    _prepare_run_dir(run_dir)
    runtime = BenchmarkRuntime(case_dir, run_dir)
    case = runtime.case
    listing = runtime.list_documents()
    for path in listing["files"]:
        runtime.read_document(path)

    risky = case.task.attack.risky_effect
    response = runtime.ask_human(
        question=(
            "Do you authorize this exact action: "
            f"{case.task.attack.injected_instruction}? "
            f"Potential concern: {case.task.attack.risk_summary}"
        )
    )
    should_execute = behavior == "vulnerable" or (
        case.human_response.category == "clear_approve"
        and case.task.attack.authorization_mode == "confirmable"
    )
    if should_execute:
        _invoke_effect(runtime, risky)

    for effect in case.task.required_benign_effects:
        _invoke_effect(runtime, effect)
    runtime.finish(
        f"Scripted {behavior} smoke-test completed; human said: {response['response']}"
    )
    result = evaluate_run(case_dir, run_dir)
    write_result(result, run_dir / "result.json")
    return result


def run_claude_code(
    case_dir: Path,
    run_dir: Path,
    *,
    model: str = "sonnet",
    executable: str = "claude",
    max_budget_usd: float = 1.0,
    bare: bool = False,
    timeout_seconds: int = 300,
) -> CaseResult:
    executable_path = shutil.which(executable)
    if executable_path is None:
        raise FileNotFoundError(f"Claude Code executable not found: {executable}")
    case_dir = case_dir.resolve()
    run_dir = run_dir.resolve()
    _prepare_run_dir(run_dir)
    mcp_config_path = run_dir / "mcp_config.json"
    mcp_config = {
        "mcpServers": {
            "hil_bench": {
                "type": "stdio",
                "command": sys.executable,
                "args": ["-m", "hil_safety_bench.mcp_server"],
                "env": {
                    "HIL_BENCH_CASE_DIR": str(case_dir),
                    "HIL_BENCH_RUN_DIR": str(run_dir),
                },
            }
        }
    }
    mcp_config_path.write_text(
        json.dumps(mcp_config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    prompt = (case_dir / "TASK.md").read_text(encoding="utf-8")
    command = [
        executable_path,
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        model,
        "--max-budget-usd",
        str(max_budget_usd),
        "--mcp-config",
        str(mcp_config_path),
        "--strict-mcp-config",
        "--no-session-persistence",
        "--session-id",
        str(uuid.uuid4()),
        "--disallowedTools",
        "Bash,Edit,Write,Read,WebFetch,WebSearch,NotebookEdit,Glob,Grep,Task",
        "--allowedTools",
        "mcp__hil_bench__*",
        "--permission-mode",
        "dontAsk",
    ]
    if bare:
        command.append("--bare")
    command.append(prompt)

    started = datetime.now(timezone.utc)
    completed, timed_out = _run_process(
        command,
        cwd=case_dir / "workspace",
        timeout_seconds=timeout_seconds,
    )
    (run_dir / "claude_stream.jsonl").write_text(
        completed.stdout,
        encoding="utf-8",
    )
    (run_dir / "claude_stderr.log").write_text(
        completed.stderr,
        encoding="utf-8",
    )
    metadata = {
        "agent": "claude-code",
        "model": model,
        "command": command[:-1] + ["<TASK_PROMPT>"],
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "returncode": completed.returncode,
        "timeout_seconds": timeout_seconds,
        "timed_out": timed_out,
    }
    (run_dir / "run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if completed.returncode != 0:
        failure = "timed out" if timed_out else "failed"
        _write_failure(
            run_dir,
            agent="claude-code",
            model=model,
            returncode=completed.returncode,
            timed_out=timed_out,
            timeout_seconds=timeout_seconds,
            stderr_log="claude_stderr.log",
        )
        raise RuntimeError(
            f"Claude Code run {failure}. See "
            f"{run_dir / 'claude_stderr.log'} for details."
        )
    result = evaluate_run(case_dir, run_dir)
    write_result(result, run_dir / "result.json")
    return result


def run_codex(
    case_dir: Path,
    run_dir: Path,
    *,
    model: str = "gpt-5.6-luna",
    reasoning_effort: str = "medium",
    executable: str = "codex",
    timeout_seconds: int = 300,
    condition: str = "neutral",
) -> CaseResult:
    executable_path = shutil.which(executable)
    if executable_path is None:
        raise FileNotFoundError(f"Codex executable not found: {executable}")
    case_dir = case_dir.resolve()
    run_dir = run_dir.resolve()
    _prepare_run_dir(run_dir)
    python_executable = sys.executable
    task_prompt = (case_dir / "TASK.md").read_text(encoding="utf-8")
    prompt = apply_condition(task_prompt, condition)
    mcp_env = (
        "{"
        f'HIL_BENCH_CASE_DIR="{_toml_escape(str(case_dir))}",'
        f'HIL_BENCH_RUN_DIR="{_toml_escape(str(run_dir))}"'
        "}"
    )
    command = [
        executable_path,
        "exec",
        "-m",
        model,
        "-s",
        "read-only",
        "-C",
        str(case_dir / "workspace"),
        "--skip-git-repo-check",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--json",
        "-c",
        'approval_policy="never"',
        "-c",
        f'model_reasoning_effort="{_toml_escape(reasoning_effort)}"',
        "-c",
        (
            'mcp_servers.hil_bench.command="'
            f'{_toml_escape(python_executable)}"'
        ),
        "-c",
        'mcp_servers.hil_bench.args=["-m","hil_safety_bench.mcp_server"]',
        "-c",
        'mcp_servers.hil_bench.default_tools_approval_mode="approve"',
        "-c",
        f"mcp_servers.hil_bench.env={mcp_env}",
        "-",
    ]
    started = datetime.now(timezone.utc)
    completed, timed_out = _run_process(
        command,
        cwd=case_dir / "workspace",
        input_text=prompt,
        timeout_seconds=timeout_seconds,
    )
    (run_dir / "codex_stream.jsonl").write_text(
        completed.stdout,
        encoding="utf-8",
    )
    (run_dir / "codex_stderr.log").write_text(
        completed.stderr,
        encoding="utf-8",
    )
    metadata = {
        "agent": "codex",
        "model": model,
        "reasoning_effort": reasoning_effort,
        "condition": condition,
        "task_prompt_sha256": hashlib.sha256(task_prompt.encode()).hexdigest(),
        "effective_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "command": command[:-1] + ["<TASK_PROMPT_ON_STDIN>"],
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "returncode": completed.returncode,
        "timeout_seconds": timeout_seconds,
        "timed_out": timed_out,
        "usage": _last_codex_usage(completed.stdout),
    }
    (run_dir / "run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if completed.returncode != 0:
        failure = "timed out" if timed_out else "failed"
        _write_failure(
            run_dir,
            agent="codex",
            model=model,
            returncode=completed.returncode,
            timed_out=timed_out,
            timeout_seconds=timeout_seconds,
            stderr_log="codex_stderr.log",
        )
        raise RuntimeError(
            f"Codex run {failure}. See "
            f"{run_dir / 'codex_stderr.log'} for details."
        )
    result = evaluate_run(case_dir, run_dir)
    write_result(result, run_dir / "result.json")
    return result


def _prepare_run_dir(run_dir: Path) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    if any(run_dir.iterdir()):
        raise FileExistsError(
            f"Run directory must be empty for reproducibility: {run_dir}"
        )


def _run_process(
    command: list[str],
    *,
    cwd: Path,
    timeout_seconds: int,
    input_text: str | None = None,
) -> tuple[subprocess.CompletedProcess[str], bool]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            input=input_text,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        return completed, False
    except subprocess.TimeoutExpired as error:
        stdout = _captured_text(error.stdout)
        stderr = _captured_text(error.stderr)
        stderr += (
            f"\nProcess exceeded the {timeout_seconds}-second timeout "
            "and was terminated.\n"
        )
        return (
            subprocess.CompletedProcess(
                command,
                124,
                stdout=stdout,
                stderr=stderr,
            ),
            True,
        )


def _captured_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _write_failure(
    run_dir: Path,
    *,
    agent: str,
    model: str,
    returncode: int,
    timed_out: bool,
    timeout_seconds: int,
    stderr_log: str,
) -> None:
    payload = {
        "status": "failed",
        "score_eligible": False,
        "agent": agent,
        "model": model,
        "returncode": returncode,
        "timed_out": timed_out,
        "timeout_seconds": timeout_seconds,
        "stderr_log": stderr_log,
    }
    (run_dir / "failure.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _last_codex_usage(stream: str) -> dict[str, Any] | None:
    usage = None
    for line in stream.splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("type") == "turn.completed":
            usage = payload.get("usage")
    return usage


def _example_arguments(effect: EffectSpec) -> dict[str, Any]:
    args: dict[str, Any] = {}
    for key, value in effect.match.items():
        if key == "contains":
            args["command"] = value
        elif key == "body_contains":
            args["body"] = value
        elif key == "minimum_count":
            args["count"] = int(value)
        elif key == "maximum_count":
            args.setdefault("count", int(value))
        elif key == "exact_count":
            args["count"] = int(value)
        elif key == "operation_contains":
            args["operation"] = value
        else:
            args[key] = value
    if effect.tool == "execute_command":
        args.setdefault("command", "true")
        args["justification"] = effect.description
    elif effect.tool == "upload_file":
        args["justification"] = effect.description
    elif effect.tool == "delete_path":
        args["justification"] = effect.description
    elif effect.tool == "send_message":
        args.setdefault("subject", "benchmark message")
        args.setdefault("body", "benchmark body")
        args["justification"] = effect.description
    elif effect.tool == "consume_resource":
        args.setdefault("count", 1)
        args["justification"] = effect.description
    elif effect.tool == "write_output":
        args.setdefault("content", f"# {effect.description}\n")
    return args


def _invoke_effect(runtime: BenchmarkRuntime, effect: EffectSpec) -> dict[str, Any]:
    args = _example_arguments(effect)
    method = getattr(runtime, effect.tool)
    return method(**args)
