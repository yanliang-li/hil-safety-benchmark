"""Draw the implemented protocol. No model results or synthetic measurements."""
from pathlib import Path
import json
import sys

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).resolve().parent
QA = HERE / "build/figure_qa"
SKILL_SCRIPTS = Path.home() / ".codex/skills/nature-figure/scripts"


def main():
    QA.mkdir(parents=True, exist_ok=True)
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
        "font.size": 7.2, "svg.fonttype": "none", "pdf.fonttype": 42,
        "axes.linewidth": .7, "savefig.facecolor": "white",
    })
    fig, axes = plt.subplots(2, 1, figsize=(5.5, 3.15),
                             gridspec_kw={"height_ratios": [1.15, 1]})
    fig.subplots_adjust(left=.025, right=.975, top=.92, bottom=.07, hspace=.42)
    ink, blue, orange, teal, edge = "#263546", "#e9f0f8", "#faeadc", "#e4f1ed", "#728296"
    for ax, title in zip(axes, ["a  Observed workflow", "b  Expected behavior after a matched question"]):
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.axis("off")
        ax.annotate(title, xy=(0, 1), xycoords="axes fraction", xytext=(0, 7),
                    textcoords="offset points", ha="left", va="bottom", fontsize=8, weight="bold", color=ink)

    def box(ax, x, y, w, h, label, fill):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.025",
                                   fc=fill, ec=edge, lw=.65))
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", color=ink, linespacing=1.35)

    def arrow(ax, a, b):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=7, lw=.8, color=edge))

    ax = axes[0]
    boxes = [
        (.005, .165, "Benign task\nReconcile\ninvoices", blue),
        (.215, .165, "Read artifacts\nInjected\nextra steps", orange),
        (.425, .145, "Agent\nAssess\nauthority", blue),
        (.625, .165, "Optional HIL\nQuestion +\nfixed reply", teal),
        (.835, .16, "Tool effects\nTask output\nand safety", blue),
    ]
    for x, w, label, fill in boxes:
        box(ax, x, .38, w, .53, label, fill)
    for left, right in zip(boxes, boxes[1:]):
        arrow(ax, (left[0]+left[1]+.004, .645), (right[0]-.004, .645))
    ax.plot([.4975, .4975, .915], [.375, .17, .17], color=edge, lw=.8)
    arrow(ax, (.915, .17), (.915, .375))
    ax.text(.70, .03, "No consultation", ha="center", va="bottom", fontsize=6.5, color=ink)

    ax = axes[1]
    columns = [
        ("Approve", "Perform the\napproved effect", teal),
        ("Deny", "Withhold\nthe effect", blue),
        ("Ambiguous", "Keep permission\nunresolved", blue),
        ("Other scope", "Do not transfer\npermission", orange),
    ]
    for i, (name, desc, fill) in enumerate(columns):
        x = .005 + .2525*i
        box(ax, x, .26, .2325, .68, "", fill)
        ax.text(x+.11625, .76, name, ha="center", va="center", weight="bold", color=ink)
        ax.text(x+.11625, .46, desc, ha="center", va="center", linespacing=1.35, color=ink)
    ax.text(.5, .05, "Confirmable effects only. Prohibited effects remain blocked in every branch.",
            ha="center", va="center", fontsize=6.5, color=ink)
    fig.canvas.draw()
    if SKILL_SCRIPTS.exists():
        sys.path.insert(0, str(SKILL_SCRIPTS))
        from audit_panel_alignment import require_matplotlib_panel_alignment
        require_matplotlib_panel_alignment(fig, json_out=str(QA / "protocol.alignment.json"),
                                          overlay_svg=str(QA / "protocol.alignment.svg"),
                                          tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=True)
    else:
        raise RuntimeError("Install nature-figure before regenerating the audited figure")
    fig.savefig(HERE / "figures/control_loop.pdf")
    fig.savefig(HERE / "figures/control_loop.svg")
    fig.savefig(HERE / "figures/control_loop.png", dpi=600)
    plt.close(fig)
    (QA / "protocol_contract.json").write_text(json.dumps({
        "claim": "The implemented protocol links consultation to reply use and tool effects.",
        "archetype": "schematic-led composite", "backend": "Python / Matplotlib",
        "panels": {"a": "actual workflow with optional consultation", "b": "four fixed reply contracts"},
        "data": "Protocol schematic; no numerical observations, estimates, or exclusions.",
        "boundaries": ["independent starts", "simulated effects", "no runtime gate", "no shared prefix"],
        "uncertainty": "Not applicable: protocol diagram, no estimated quantity.",
        "size_inches": [5.5, 3.15], "min_font_pt": 6.5,
        "reuse": "Original drawing; conceptual organization informed by published benchmark figures.",
    }, indent=2) + "\n")
    print("Wrote protocol PDF/SVG/PNG and alignment evidence.")


if __name__ == "__main__":
    main()
