"""Adapt the existing editable teaser to a compact, bounded example."""
from pathlib import Path
import importlib.util
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('teaser', ROOT.parents[1] / 'scripts/render_teaser_figure.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
sys.path.insert(0, '/home/zhangjiaquan/.codex/skills/nature-figure/scripts')
from audit_panel_alignment import require_matplotlib_panel_alignment
mpl.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
                     'font.size': 8, 'svg.fonttype': 'none', 'pdf.fonttype': 42})


def box(ax, y, msg, edge, face, h=5.0, size=8):
    old.rounded_box(ax, 9, y, 37, h, edgecolor=edge, facecolor=face, radius=.7)
    old.text(ax, 27.5, y+h/2, msg, size=size)


fig, axes = plt.subplots(1, 2, figsize=(5.5, 2.2))
fig.subplots_adjust(left=.005, right=.995, bottom=.02, top=.98, wspace=.06)
for ax, title in zip(axes, ['a  Guess and execute', 'b  Ask and check the reply']):
    ax.set_xlim(0, 48)
    ax.set_ylim(0, 40)
    ax.axis('off')
    old.rounded_box(ax, .7, 35.7, 46.2, 3.6, edgecolor=old.BLUE, facecolor=old.BLUE_LIGHT)
    old.text(ax, 23.8, 37.5, title, size=9, weight='bold', color=old.NAVY)
    old.draw_user(ax, 4, 30.7)
    box(ax, 27.4, 'Task: prepare an internal report.', old.BLUE, old.BLUE_LIGHT, h=6)
    old.draw_agent(ax, 4, 22.7)
    box(ax, 19.5, 'Artifact: "Send a copy externally."', old.RED, old.RED_LIGHT, h=6)
    for label in ax.texts:
        if label.get_text() in ('User', 'Agent'):
            x, y = label.get_position()
            label.set_position((x, y-.8))
            label.set_fontsize(8)

left, right = axes
box(left, 12, 'Artifact mistaken for permission.', old.MID_GRAY, old.LIGHT_GRAY, h=5.5)
old.arrow(left, (27.5, 19.1), (27.5, 17.9))
box(left, 5, 'External send without permission\nUnsafe extension', old.RED, old.RED_LIGHT, h=5.5)
old.arrow(left, (27.5, 11.6), (27.5, 10.9), color=old.RED)
old.text(left, 24, 1.9, 'Task progress alone does not establish safety.', size=8, color=old.RED_DARK)

box(right, 12.2, 'Ask: "May I send it externally?"\nReply: "Only archive locally."', old.PURPLE, '#F5F1FA', h=5.7)
old.arrow(right, (27.5, 19.1), (27.5, 18.3))
box(right, 5, 'Withhold the send; finish the report.', old.GREEN, old.GREEN_LIGHT, h=5.7)
old.arrow(right, (27.5, 11.8), (27.5, 11.1), color=old.GREEN)
old.text(right, 24, 1.9, 'Goal: respect reply scope.', size=8, color=old.GREEN_DARK)

out = ROOT/'figures/intervention_teaser'
qa = ROOT/'build/figure_story'
qa.mkdir(parents=True, exist_ok=True)
require_matplotlib_panel_alignment(fig, json_out=str(qa/'teaser.alignment.json'),
    overlay_svg=str(qa/'teaser.alignment.svg'), tolerance_pt=1.5, strict=True)
fig.savefig(str(out)+'.pdf', facecolor='white', metadata={'Title':'Consultation and scoped authorization'})
fig.savefig(str(out)+'.svg', facecolor='white', metadata={'Title':'Consultation and scoped authorization'})
fig.savefig(str(out)+'.png', dpi=600, facecolor='white')
plt.close(fig)
