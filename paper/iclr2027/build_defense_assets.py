"""Generate a manuscript table only from the completed audited comparison."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    source = ROOT / "reports/defense-comparison-20260912/comparison.json"
    data = json.loads(source.read_text())
    audit = json.loads(
        (ROOT / "runs/gpt-luna-prompt-guard-80-20260912/trajectory_audit.json").read_text()
    )
    if data["case_count"] != 80 or not audit["all_planned_completed"]:
        raise ValueError("Complete the full paired comparison before generating this table")
    if audit["unresolved_issue_case_count"]:
        raise ValueError("Resolve trajectory audit findings before manuscript reporting")
    labels = [
        ("unsafe_asr", "Unsafe ASR"),
        ("hil_recall", "Matched HIL on confirmable cases"),
        ("direct_block", "Direct block on prohibited cases"),
        ("response_accuracy", "Response-conditioned action accuracy"),
        ("benign_completion", "Benign task completion"),
        ("joint_utility", "Joint safe utility"),
        ("paired_boundary", "Four-response boundary (tasks)"),
    ]
    lines = [
        r"\begin{table}[ht]", r"\centering\small",
        r"\caption{Exploratory comparison on the same 20 tasks and four reply conditions "
        r"(80 runs per condition). Prompt guard adds authorization-scope instructions; "
        r"the model, image, cases, and scorer are fixed. Conditional denominators "
        r"differ. This is a prompt defense, not runtime enforcement.}",
        r"\label{tab:defense}", r"\begin{tabular}{lrr}",
        r"\toprule", r"Metric & Neutral & Prompt guard\\", r"\midrule",
    ]
    for key, label in labels:
        row = [label]
        for condition in ["baseline", "defense"]:
            n, d = data["metrics"][key][condition]
            row.append(f"{n}/{d} ({100*n/d:.1f}\\%)" if d else "N/A")
        lines.append(" & ".join(row) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (HERE / "tables/defense_results.tex").write_text("\n".join(lines) + "\n")
    evidence = {
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "condition": "prompt_guard_v1",
        "metrics": data["metrics"],
        "checks": data["checks"],
        "runtime_guard_implemented": False,
        "audit_unresolved_issues": 0,
    }
    (HERE / "defense_results_evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print("Generated manuscript defense table from the completed comparison.")


if __name__ == "__main__":
    main()
