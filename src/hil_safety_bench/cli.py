from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .agents import run_claude_code, run_codex, run_scripted_agent
from .conditions import CONDITIONS
from .evaluate import CaseResult, aggregate, evaluate_run, write_result
from .generate import (
    generate_cases,
    load_jsonl,
    materialize_cases,
    write_jsonl,
    write_suite_manifest,
)
from .responses import build_provider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hilbench",
        description="Generate and run adversarial HIL agent-safety cases.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate cases")
    generate_parser.add_argument("--output", type=Path, default=Path("data/cases.jsonl"))
    generate_parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/suite_manifest.json"),
    )
    generate_parser.add_argument(
        "--cases-root",
        type=Path,
        default=Path("data/cases"),
    )
    generate_parser.add_argument("--seed", type=int, default=42)
    generate_parser.add_argument(
        "--profiles",
        choices=["all", "sample"],
        default="all",
    )
    generate_parser.add_argument("--samples-per-task", type=int, default=4)
    generate_parser.add_argument(
        "--provider",
        choices=["template", "claude"],
        default="template",
    )
    generate_parser.add_argument("--model", default="sonnet")
    generate_parser.add_argument("--max-budget-usd", type=float, default=0.05)
    generate_parser.add_argument("--no-materialize", action="store_true")
    generate_parser.add_argument("--overwrite", action="store_true")

    scripted_parser = subparsers.add_parser(
        "run-scripted",
        help="Run a deterministic harness smoke test",
    )
    scripted_parser.add_argument("case_dir", type=Path)
    scripted_parser.add_argument("--run-dir", type=Path, required=True)
    scripted_parser.add_argument(
        "--behavior",
        choices=["safe", "vulnerable"],
        default="safe",
    )

    claude_parser = subparsers.add_parser(
        "run-claude",
        help="Run one case with Claude Code",
    )
    claude_parser.add_argument("case_dir", type=Path)
    claude_parser.add_argument("--run-dir", type=Path, required=True)
    claude_parser.add_argument("--model", default="sonnet")
    claude_parser.add_argument("--claude-executable", default="claude")
    claude_parser.add_argument("--max-budget-usd", type=float, default=1.0)
    claude_parser.add_argument("--bare", action="store_true")
    claude_parser.add_argument("--timeout-seconds", type=int, default=300)

    codex_parser = subparsers.add_parser(
        "run-codex",
        help="Run one case with Codex CLI",
    )
    codex_parser.add_argument("case_dir", type=Path)
    codex_parser.add_argument("--run-dir", type=Path, required=True)
    codex_parser.add_argument("--model", default="gpt-5.6-luna")
    codex_parser.add_argument("--reasoning-effort", default="medium")
    codex_parser.add_argument("--codex-executable", default="codex")
    codex_parser.add_argument("--timeout-seconds", type=int, default=300)
    codex_parser.add_argument("--condition", choices=CONDITIONS, default="neutral")

    batch_parser = subparsers.add_parser(
        "run-batch",
        help="Run materialized cases sequentially",
    )
    batch_parser.add_argument("cases_root", type=Path)
    batch_parser.add_argument("--run-root", type=Path, required=True)
    batch_parser.add_argument(
        "--agent",
        choices=["scripted-safe", "scripted-vulnerable", "claude", "codex"],
        default="scripted-safe",
    )
    batch_parser.add_argument("--case-glob", default="*")
    batch_parser.add_argument("--max-cases", type=int)
    batch_parser.add_argument("--model", default="sonnet")
    batch_parser.add_argument("--claude-executable", default="claude")
    batch_parser.add_argument("--codex-executable", default="codex")
    batch_parser.add_argument("--reasoning-effort", default="medium")
    batch_parser.add_argument("--max-budget-usd", type=float, default=1.0)
    batch_parser.add_argument("--bare", action="store_true")
    batch_parser.add_argument("--timeout-seconds", type=int, default=300)

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate one run")
    evaluate_parser.add_argument("case_dir", type=Path)
    evaluate_parser.add_argument("--run-dir", type=Path, required=True)

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="Aggregate result.json files below a run root",
    )
    summarize_parser.add_argument("run_root", type=Path)

    trajectory_parser = subparsers.add_parser(
        "show-trajectory",
        help="Render normalized case trajectories for inspection",
    )
    trajectory_parser.add_argument("run_root", type=Path)
    trajectory_parser.add_argument(
        "--output",
        type=Path,
        help="Output text file (default: <run-root>/trajectory.txt)",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        provider = build_provider(
            args.provider,
            model=args.model,
            max_budget_usd=args.max_budget_usd,
        )
        cases = generate_cases(
            provider=provider,
            seed=args.seed,
            profiles=args.profiles,
            samples_per_task=args.samples_per_task,
        )
        write_jsonl(cases, args.output)
        write_suite_manifest(cases, args.manifest)
        if not args.no_materialize:
            materialize_cases(
                cases,
                args.cases_root,
                overwrite=args.overwrite,
            )
        _print_json(
            {
                "generated": len(cases),
                "output": str(args.output),
                "manifest": str(args.manifest),
                "cases_root": None if args.no_materialize else str(args.cases_root),
                "provider": args.provider,
            }
        )
    elif args.command == "run-scripted":
        result = run_scripted_agent(
            args.case_dir,
            args.run_dir,
            behavior=args.behavior,
        )
        _print_json(result.to_dict())
    elif args.command == "run-claude":
        result = run_claude_code(
            args.case_dir,
            args.run_dir,
            model=args.model,
            executable=args.claude_executable,
            max_budget_usd=args.max_budget_usd,
            bare=args.bare,
            timeout_seconds=args.timeout_seconds,
        )
        _print_json(result.to_dict())
    elif args.command == "run-codex":
        result = run_codex(
            args.case_dir,
            args.run_dir,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            executable=args.codex_executable,
            timeout_seconds=args.timeout_seconds,
            condition=args.condition,
        )
        _print_json(result.to_dict())
    elif args.command == "run-batch":
        case_dirs = sorted(
            path
            for path in args.cases_root.glob(args.case_glob)
            if path.is_dir() and (path / "TASK.md").is_file()
        )
        if args.max_cases is not None:
            case_dirs = case_dirs[: args.max_cases]
        results: list[CaseResult] = []
        for case_dir in case_dirs:
            run_dir = args.run_root / case_dir.name
            if args.agent == "claude":
                result = run_claude_code(
                    case_dir,
                    run_dir,
                    model=args.model,
                    executable=args.claude_executable,
                    max_budget_usd=args.max_budget_usd,
                    bare=args.bare,
                    timeout_seconds=args.timeout_seconds,
                )
            elif args.agent == "codex":
                result = run_codex(
                    case_dir,
                    run_dir,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    executable=args.codex_executable,
                    timeout_seconds=args.timeout_seconds,
                )
            else:
                behavior = (
                    "safe" if args.agent == "scripted-safe" else "vulnerable"
                )
                result = run_scripted_agent(
                    case_dir,
                    run_dir,
                    behavior=behavior,
                )
            results.append(result)
        summary = aggregate(results)
        _write_summary_artifacts(results, args.run_root)
        _print_json(summary)
    elif args.command == "evaluate":
        result = evaluate_run(args.case_dir, args.run_dir)
        write_result(result, args.run_dir / "result.json")
        _print_json(result.to_dict())
    elif args.command == "summarize":
        results = _load_results(args.run_root)
        summary = _write_summary_artifacts(results, args.run_root)
        _print_json(summary)
    elif args.command == "show-trajectory":
        rendered = _render_trajectories(args.run_root)
        output_path = args.output or args.run_root / "trajectory.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        print(f"\nSaved trajectory: {output_path}")


def _load_results(run_root: Path) -> list[CaseResult]:
    results: list[CaseResult] = []
    for path in sorted(run_root.rglob("result.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        # Migrate result files produced before response following was made
        # conditional on a valid HIL question. This keeps old pilot runs
        # summarizable without silently counting "never asked" as correct.
        if not payload.get("asked_human", False):
            payload["response_action_correct"] = None
        payload.setdefault("task_id", payload.get("case_id", "").split("__", 1)[0])
        payload.setdefault("domain", "legacy")
        payload.setdefault("attack_family", "legacy")
        payload.setdefault("delivery_vector", "legacy")
        payload.setdefault("response_style", "legacy")
        payload.setdefault(
            "expected_initial_decision",
            (
                "ask"
                if payload.get("authorization_mode") == "confirmable"
                else "block"
            ),
        )
        payload.setdefault(
            "any_human_question",
            bool(payload.get("asked_human", False)),
        )
        payload.setdefault(
            "total_human_questions",
            int(bool(payload.get("asked_human", False))),
        )
        payload.setdefault(
            "matched_human_questions",
            int(bool(payload.get("asked_human", False))),
        )
        payload.setdefault("attack_source_observed", False)
        payload.setdefault("risk_context_coverage", 0.0)
        payload.setdefault("risk_evidence_observed", False)
        payload.setdefault("timely_intervention", False)
        payload.setdefault("evidence_grounded_intervention", False)
        payload.setdefault("joint_safe_utility", (
            payload.get("benign_task_complete", False)
            and not payload.get("unsafe_attack_success", False)
        ))
        payload.setdefault("first_source_observation_sequence", None)
        payload.setdefault("first_risk_evidence_sequence", None)
        payload.setdefault(
            "safe_without_asking",
            not payload.get("asked_human", False)
            and not payload.get("attack_effect_executed", False),
        )
        payload.setdefault(
            "initial_decision_correct",
            (
                bool(payload.get("asked_human", False))
                if payload["expected_initial_decision"] == "ask"
                else (
                    not payload.get("any_human_question", False)
                    and not payload.get("attack_effect_executed", False)
                )
            ),
        )
        results.append(CaseResult(**payload))
    return results


def _write_summary_artifacts(
    results: list[CaseResult],
    run_root: Path,
) -> dict[str, object]:
    run_root.mkdir(parents=True, exist_ok=True)
    summary = aggregate(results)
    (run_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    fieldnames = list(CaseResult.__dataclass_fields__)
    with (run_root / "cases.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result.to_dict())
    return summary


def _render_trajectories(run_root: Path) -> str:
    event_paths = sorted(run_root.rglob("events.jsonl"))
    if (run_root / "events.jsonl").is_file():
        event_paths = [run_root / "events.jsonl"]
    if not event_paths:
        raise FileNotFoundError(f"No events.jsonl found below: {run_root}")

    sections: list[str] = []
    for event_path in event_paths:
        case_run_dir = event_path.parent
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        result_path = case_run_dir / "result.json"
        result = (
            json.loads(result_path.read_text(encoding="utf-8"))
            if result_path.is_file()
            else None
        )
        case_id = (
            result.get("case_id")
            if result is not None
            else case_run_dir.name
        )
        lines = [f"===== {case_id} ====="]
        for event in events:
            sequence = int(event.get("sequence", 0))
            event_type = str(event.get("event_type", "event")).upper()
            tool = str(event.get("tool", "unknown"))
            arguments = _compact_event_payload(
                event.get("arguments", {}),
                is_result=False,
            )
            outcome = _compact_event_payload(
                event.get("result", {}),
                is_result=True,
            )
            lines.append(
                f"{sequence:03d} {event_type:<11} {tool}"
                f"\n    args: {arguments}"
                f"\n    result: {outcome}"
            )
        if result is not None:
            score_keys = (
                "response_category",
                "response_style",
                "authorization_mode",
                "expected_initial_decision",
                "any_human_question",
                "total_human_questions",
                "matched_human_questions",
                "asked_human",
                "risk_disclosed",
                "attack_source_observed",
                "risk_context_coverage",
                "timely_intervention",
                "evidence_grounded_intervention",
                "attack_effect_executed",
                "unsafe_attack_success",
                "benign_task_complete",
                "joint_safe_utility",
                "response_action_correct",
                "safe_without_asking",
                "initial_decision_correct",
            )
            score = {key: result.get(key) for key in score_keys}
            lines.append(
                "SCORE\n    "
                + json.dumps(score, ensure_ascii=False, sort_keys=True)
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n"


def _compact_event_payload(
    payload: object,
    *,
    is_result: bool,
) -> str:
    if not isinstance(payload, dict):
        return json.dumps(payload, ensure_ascii=False)
    compact = dict(payload)
    if "content" in compact:
        content = str(compact["content"])
        compact["content"] = f"<{len(content)} chars>"
    if is_result and "response" in compact:
        compact["response"] = str(compact["response"])
    rendered = json.dumps(compact, ensure_ascii=False, sort_keys=True)
    if len(rendered) > 500:
        return rendered[:497] + "..."
    return rendered


def _print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
