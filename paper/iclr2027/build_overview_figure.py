"""Draw the three-module InterveneBench protocol as native vector artwork."""

from pathlib import Path
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch, FancyArrowPatch, FancyBboxPatch


HERE = Path(__file__).resolve().parent
QA = HERE / "build/figure_qa"
OUT = HERE / "figures/benchmark_overview"
SKILL = Path.home() / ".codex/skills/nature-figure/scripts"
sys.path.insert(0, str(SKILL))
from audit_panel_alignment import require_matplotlib_panel_alignment


INK = "#20262E"
GRAY = "#66717D"
BORDER = "#B9C4D0"
BLUE = "#2F6FD6"
BLUE_DARK = "#174A8B"
BLUE_LIGHT = "#EEF5FF"
PURPLE = "#7656B5"
PURPLE_LIGHT = "#F4F0FA"
GREEN = "#4F8A3B"
GREEN_LIGHT = "#F0F7EC"
RED = "#C93B36"
RED_LIGHT = "#FFF1F0"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 8,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
})


def box(ax, xy, wh, text, edge=BORDER, face="white", *, weight="normal", size=8):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.025",
        transform=ax.transAxes, facecolor=face, edgecolor="none", linewidth=0,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, transform=ax.transAxes,
            ha="center", va="center", fontsize=size, color=INK,
            fontweight=weight, linespacing=1.15)
    return patch


def arrow(ax, start, end, color=GRAY, *, dashed=False):
    patch = FancyArrowPatch(start, end, transform=ax.transAxes, arrowstyle="-|>",
                            mutation_scale=8, linewidth=1.0, color=color,
                            linestyle=(0, (3, 2)) if dashed else "-",
                            shrinkA=0, shrinkB=0)
    ax.add_patch(patch)
    return patch


def robot(ax, x, y, color=BLUE_DARK):
    head = FancyBboxPatch((x - .035, y - .025), .07, .05,
                          boxstyle="round,pad=.01,rounding_size=.012",
                          transform=ax.transAxes, facecolor="white",
                          edgecolor=color, linewidth=1)
    ax.add_patch(head)
    ax.add_patch(Circle((x - .016, y), .006, transform=ax.transAxes, color=color))
    ax.add_patch(Circle((x + .016, y), .006, transform=ax.transAxes, color=color))
    ax.plot([x, x], [y + .035, y + .052], transform=ax.transAxes, color=color, lw=1)
    ax.add_patch(Circle((x, y + .057), .006, transform=ax.transAxes, color=color))


fig, axes = plt.subplots(1, 3, figsize=(5.5, 2.2), gridspec_kw={"wspace": .10})
fig.subplots_adjust(left=.012, right=.988, bottom=.055, top=.95)
titles = ["1  Case\nsetup", "2  Agent\ninteraction", "3  Execution\nand scoring"]
for ax, title in zip(axes, titles):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((.005, .01), .99, .98,
                 boxstyle="round,pad=.012,rounding_size=.025",
                 transform=ax.transAxes, facecolor="#FBFCFE",
                 edgecolor=BORDER, linewidth=1.0))
    ax.text(.5, .925, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=9, fontweight="bold", color=BLUE_DARK)

a, b, c = axes
box(a, (.12, .67), (.76, .13), "Trusted task\nand authority", BLUE, BLUE_LIGHT, weight="bold")
box(a, (.12, .48), (.76, .13), "Artifact adds\nan extra effect", RED, RED_LIGHT)
arrow(a, (.5, .65), (.5, .62), RED)
box(a, (.07, .08), (.86, .32), "Policy fixed before run\n6 reply policies\nOne or two turns\nIndependent starts", PURPLE, PURPLE_LIGHT)
arrow(a, (.5, .47), (.5, .405), GRAY)

robot(b, .17, .74)
box(b, (.31, .67), (.58, .13), "Agent proposes\nan action", BLUE, BLUE_LIGHT, weight="bold")
arrow(b, (.60, .66), (.60, .60))
box(b, (.07, .43), (.40, .15), "Matched\nask", PURPLE, PURPLE_LIGHT, weight="bold")
box(b, (.54, .43), (.39, .15), "No scoped\nask", BORDER, "white", weight="bold")
box(b, (.07, .22), (.40, .14), "Next policy\nreply", PURPLE, PURPLE_LIGHT)
box(b, (.54, .22), (.39, .14), "No reply\nexposed", BORDER, "white")
arrow(b, (.27, .42), (.27, .37), PURPLE)
arrow(b, (.735, .42), (.735, .37), GRAY)
arrow(b, (.27, .21), (.48, .12), PURPLE)
arrow(b, (.735, .21), (.52, .12), GRAY)
b.add_patch(Circle((.5, .105), .018, transform=b.transAxes, facecolor=BLUE_DARK, edgecolor="none"))

box(c, (.18, .66), (.64, .12), "Native / Prompt\ndispatch", BLUE, BLUE_LIGHT, weight="bold")
c.text(.10, .64, "OR", transform=c.transAxes, ha="center", va="center",
       fontsize=8, color=GRAY, fontweight="bold")
box(c, (.18, .43), (.64, .19), "SAIL-HIL control\nAssess authority\nClarify if needed", PURPLE, PURPLE_LIGHT, weight="bold")
box(c, (.20, .26), (.60, .12), "Outcome record", GREEN, GREEN_LIGHT, weight="bold")
c.plot([.82, .94, .94], [.72, .72, .38], transform=c.transAxes,
       color=BLUE, linewidth=1.0)
arrow(c, (.94, .38), (.81, .32), BLUE)
arrow(c, (.62, .425), (.62, .385), PURPLE)
box(c, (.12, .045), (.76, .19), "Safety · reply use\nTask completion\nFailures · cost", BORDER, "white")


# The three modules read left to right; both interaction outcomes continue.
fig.add_artist(ConnectionPatch(xyA=(.995, .50), coordsA=a.transAxes,
                               xyB=(.005, .50), coordsB=b.transAxes,
                               arrowstyle="-|>", mutation_scale=9,
                               linewidth=1.2, color=BLUE_DARK))
fig.add_artist(ConnectionPatch(xyA=(.52, .105), coordsA=b.transAxes,
                               xyB=(.02, .105), coordsB=c.transAxes,
                               arrowstyle="-", mutation_scale=9,
                               linewidth=1.2, color=BLUE_DARK))
arrow(c, (.02, .105), (.02, .60), BLUE_DARK)

QA.mkdir(parents=True, exist_ok=True)
require_matplotlib_panel_alignment(
    fig, json_out=str(QA / "overview.alignment.json"),
    overlay_svg=str(QA / "overview.alignment.svg"), tolerance_pt=1.5,
    gutter_tolerance_pt=1.5, strict=True,
)
fig.savefig(str(OUT) + ".pdf", facecolor="white", metadata={"Title": "InterveneBench protocol"})
fig.savefig(str(OUT) + ".svg", facecolor="white", metadata={"Title": "InterveneBench protocol"})
fig.savefig(str(OUT) + ".png", dpi=600, facecolor="white")
plt.close(fig)
