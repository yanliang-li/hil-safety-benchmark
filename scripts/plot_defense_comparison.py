#!/usr/bin/env python3
"""Export rates and task-cluster uncertainty from a completed comparison."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comparison", type=Path)
    args = parser.parse_args()
    data = json.loads(args.comparison.read_text())
    keys = [
        "unsafe_asr", "hil_recall", "direct_block", "response_accuracy",
        "benign_completion", "joint_utility", "paired_boundary",
    ]
    labels = [
        "Unsafe ASR (lower is better)", "HIL recall on confirmable cases",
        "Direct block on prohibited cases", "Correct action after a matched ask",
        "Benign task completion", "Joint safe utility", "Four-response boundary (tasks)",
    ]
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.6), sharey=True,
                             gridspec_kw={"width_ratios": [1.05, 1]})
    y = np.arange(len(keys))
    for condition, offset, color, label in [
        ("baseline", -.17, "#647f9e", "Neutral"),
        ("defense", .17, "#2c8f87", "Authorization prompt"),
    ]:
        pairs = [data["metrics"][key][condition] for key in keys]
        values = [100 * n / d if d else np.nan for n, d in pairs]
        bars = axes[0].barh(y + offset, values, height=.30, color=color, label=label)
        axes[0].bar_label(bars, [f"{n}/{d}" if d else "N/A" for n, d in pairs],
                         padding=3, fontsize=8)
    axes[0].set_xlim(0, 119)
    axes[0].set_yticks(y, labels)
    axes[0].invert_yaxis()
    axes[0].set_xlabel("Eligible cases or tasks (%)")
    axes[0].legend(loc="upper center", bbox_to_anchor=(.55, 1.12), ncol=2,
                   frameon=False, fontsize=8)
    axes[1].axvline(0, color="#85919b", linewidth=1)
    for i, key in enumerate(keys):
        metric = data["metrics"][key]
        delta = metric["delta"]
        interval = metric["paired_task_bootstrap"]["interval_95"]
        if delta is None or interval is None:
            axes[1].text(0, i, "N/A", va="center")
            continue
        direction = -1 if metric["preferred_direction"] == "lower" else 1
        color = "#287c62" if delta * direction > 0 else "#a6643d" if delta else "#697682"
        lower, upper = [100 * v for v in interval]
        axes[1].plot([lower, upper], [i, i], color=color, linewidth=2)
        axes[1].plot([lower, lower], [i-.08, i+.08], color=color)
        axes[1].plot([upper, upper], [i-.08, i+.08], color=color)
        axes[1].plot(delta * 100, i, "o", color=color, markersize=5)
        axes[1].annotate(f"{delta * 100:+.1f}", (delta * 100, i),
                         xytext=(0, -13), textcoords="offset points", ha="center",
                         fontsize=8, color=color)
    axes[1].set_xlabel("Guard minus neutral (percentage points)")
    axes[1].set_title("Paired task-cluster 95% intervals", fontsize=10, pad=15)
    for ax in axes:
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", alpha=.13)
        ax.set_axisbelow(True)
    fig.suptitle(f"Codex + {data['model']} / {data['reasoning_effort']}: "
                 f"{data['case_count']} matched cases", fontsize=12, y=.97)
    fig.text(.02, .045,
             f"{data['task_count']} task clusters; four replies each; "
             f"{data['bootstrap']['draws']:,} paired bootstrap draws. "
             "Conditional denominators differ between runs.", fontsize=8)
    fig.text(.02, .017,
             "Exploratory comparison with an earlier baseline; no shared pre-response state or runtime enforcement.",
             fontsize=8, color="#53606a")
    fig.subplots_adjust(left=.26, right=.98, top=.81, bottom=.16, wspace=.20)
    for ext in ["pdf", "svg", "png"]:
        path = args.comparison.parent / f"defense_comparison.{ext}"
        fig.savefig(path, dpi=200)
        print(path)
    plt.close(fig)


if __name__ == "__main__":
    main()
