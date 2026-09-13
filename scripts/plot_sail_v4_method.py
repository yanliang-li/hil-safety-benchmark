"""Draw the implemented HIL authority/recovery loop; no quantitative outcomes."""
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
QA_TOOLS = Path.home() / '.codex/skills/nature-figure/scripts'
sys.path.insert(0, str(QA_TOOLS))
from audit_panel_alignment import require_matplotlib_panel_alignment


def main():
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
        'font.size': 8, 'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})
    fig, ax = plt.subplots(figsize=(6.6, 3.35))
    fig.subplots_adjust(left=.015, right=.985, top=.99, bottom=.02)
    ax.set(xlim=(0, 100), ylim=(0, 70))
    ax.axis('off')
    neutral, blue, orange, teal = '#F2F3F5', '#E5EDF7', '#F8EBDD', '#E2F0ED'
    def box(x, y, w, title, detail, color):
        ax.add_patch(FancyBboxPatch((x, y), w, 12, boxstyle='round,pad=0.35,rounding_size=1',
            linewidth=.75, edgecolor='#607080', facecolor=color))
        ax.text(x+w/2, y+8.5, title, ha='center', va='center', fontsize=8, weight='bold')
        ax.text(x+w/2, y+3.5, detail, ha='center', va='center', fontsize=7)
    def arrow(points, color='#536273', style='-'):
        for a, b in zip(points[:-2], points[1:-1]):
            ax.plot([a[0], b[0]], [a[1], b[1]], lw=.9, color=color, linestyle=style, zorder=1)
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>', mutation_scale=9,
            linewidth=.9, color=color, linestyle=style, shrinkA=0, shrinkB=2, zorder=1))
    box(2, 56, 23, 'Original task', 'User goal + tool definitions', neutral)
    box(36, 56, 25, 'Task contract', 'Effects, scope, obligations', blue)
    box(73, 56, 25, 'Persistent ledger', 'Replies, permits, total use', teal)
    box(2, 33, 23, 'Native actor', 'Propose an exact tool call', neutral)
    box(36, 33, 25, 'Authority check', 'Original scope + remaining use', blue)
    box(73, 33, 25, 'Tool dispatch', 'Reserve permit; record effect', teal)
    box(2, 10, 23, 'Human decision', 'Actual question and reply', orange)
    box(36, 10, 25, 'Reply scope', 'Effect, object, quantity', orange)
    box(73, 10, 25, 'Task recovery', 'Suggest work; check finish', blue)
    arrow([(25.5, 62), (35.5, 62)])
    arrow([(48.5, 55.5), (48.5, 45.5)])
    arrow([(85.5, 45.5), (85.5, 55.5)])
    arrow([(73, 59), (66, 59), (66, 49), (58, 45.5)])
    arrow([(25.5, 39), (35.5, 39)])
    arrow([(61.5, 39), (72.5, 39)])
    ax.text(67, 41.5, 'Authorized', ha='center', fontsize=6.5)
    arrow([(42, 32.5), (42, 27), (13.5, 27), (13.5, 22.5)])
    ax.text(27, 29, 'Missing authority', ha='center', fontsize=6.5)
    arrow([(25.5, 16), (35.5, 16)])
    arrow([(55, 22.5), (55, 32.5)])
    ax.text(57, 27, 'Scoped\napproval', ha='left', va='center', fontsize=6.5)
    arrow([(61.5, 16), (72.5, 16)])
    ax.text(67, 13, 'No permit', ha='center', fontsize=6.5)
    arrow([(61.5, 34), (68, 25), (72.5, 22)], color='#8A6346', style='--')
    ax.text(70, 29, 'Hard block', ha='left', fontsize=6.5, color='#8A6346')
    arrow([(85.5, 32.5), (85.5, 22.5)])
    ax.text(87, 27.5, 'Feedback', ha='left', fontsize=6.5)
    arrow([(85.5, 9.5), (85.5, 3.5), (1, 3.5), (1, 39), (1.7, 39)], color='#356F89', style='--')
    ax.text(47, 5, 'Resume authorized work through the same checks', ha='center', fontsize=7, color='#245B74')
    out = ROOT / 'paper/iclr2027/figures/sail_v4_method'
    qa = ROOT / 'paper/iclr2027/build/figure_qa'
    qa.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig, json_out=str(qa / 'sail_v4_method.alignment.json'), strict=True)
    fig.savefig(out.parent / 'sail_v4_method.pdf', facecolor='white')
    fig.savefig(out.parent / 'sail_v4_method.svg', facecolor='white')
    fig.savefig(out.parent / 'sail_v4_method.png', dpi=600, facecolor='white')
    plt.close(fig)
    (qa / 'sail_v4_method.contract.json').write_text(json.dumps({
        'claim': 'Denied extensions preserve original task authority; recovery proposals are rechecked before execution.',
        'role': 'Method explanation, not quantitative evidence.', 'backend': 'Python/matplotlib',
        'archetype': 'single-panel process schematic', 'final_size_inches': [6.6, 3.35],
        'data': 'Implemented controller logic; no synthetic quantitative values.',
        'uncertainty': 'Semantic scope/effect reviews are fallible; no formal safety guarantee.',
        'source': 'scripts/plot_sail_v4_method.py'}, indent=2) + '\n')


if __name__ == '__main__':
    main()
