#!/usr/bin/env python3
"""Export descriptive pilot figures; response branches are task-paired."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    rows = [json.loads(p.read_text()) for p in sorted(args.run_root.glob("*/result.json"))]
    manifest = json.loads((args.run_root / "manifest.json").read_text())
    experiment = json.loads((args.run_root / "experiment.json").read_text())
    if len(rows) != manifest["case_count"]:
        raise ValueError("Finish the planned pilot before generating the final figure")
    categories = ["clear_approve", "clear_deny", "ambiguous", "scope_mismatch"]
    labels = ["Clear approval", "Clear denial", "Ambiguous", "Scope mismatch"]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.3, 1]})
    x = np.arange(4)
    for i, (field, label, color) in enumerate([
        ("asked_human", "Matched ask before effect", "#356db4"),
        ("unsafe_attack_success", "Unsafe effect", "#ca593f"),
        ("benign_task_complete", "Legacy benign completion", "#5f9865"),
    ]):
        values = []
        counts = []
        for category in categories:
            subset = [r for r in rows if r["response_category"] == category]
            numerator = sum(bool(r[field]) for r in subset)
            values.append(100 * numerator / len(subset))
            counts.append(f"{numerator}/{len(subset)}")
        bars = axes[0].bar(x + (i - 1) * .25, values, width=.23, color=color, label=label)
        axes[0].bar_label(bars, counts, padding=3, fontsize=8)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("Cases (%)")
    axes[0].set_ylim(0, 113)
    axes[0].legend(loc="upper center", bbox_to_anchor=(.5, -.17), ncol=1, frameon=False)
    axes[0].set_title("Behavior by response fixture")
    ask = [r for r in rows if r["authorization_mode"] == "confirmable"]
    block = [r for r in rows if r["authorization_mode"] == "prohibited"]
    post = [r for r in rows if r["response_action_correct"] is not None]
    metrics = [
        ("HIL recall\n(should ask)", sum(r["asked_human"] for r in ask), len(ask)),
        ("Direct block\n(should block)", sum(r["initial_decision_correct"] for r in block), len(block)),
        ("Correct action\n(after matched ask)", sum(r["response_action_correct"] for r in post), len(post)),
    ]
    values = [100 * n / d if d else 0 for _, n, d in metrics]
    bars = axes[1].bar(np.arange(3), values, color=["#356db4", "#5f9865", "#7e68a1"], width=.58)
    axes[1].bar_label(bars, [f"{n}/{d}" if d else "N/A" for _, n, d in metrics], padding=5)
    axes[1].set_xticks(np.arange(3), [m[0] for m in metrics])
    axes[1].set_ylim(0, 113)
    axes[1].set_ylabel("Eligible cases (%)")
    axes[1].set_title("Separate stages and denominators")
    fig.suptitle(f"Codex + {manifest['model']} / {manifest['reasoning_effort']} — "
                 f"{len(rows)}-case {experiment['condition']} pilot", fontsize=14)
    fig.text(.02, .015,
        f"{manifest['task_count']} task clusters; one task per attack family; four replies per task. "
        "Descriptive pilot rates, not full-suite estimates.", fontsize=9, color="#444444")
    fig.subplots_adjust(top=.83, bottom=.29, left=.065, right=.985, wspace=.3)
    for extension in ("png", "pdf", "svg"):
        output = args.run_root / f"pilot_overview.{extension}"
        fig.savefig(output, dpi=180)
        print(output)
    plt.close(fig)


if __name__ == "__main__":
    main()
