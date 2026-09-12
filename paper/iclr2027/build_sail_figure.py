"""Draw the implemented SAIL v2 information boundary; no empirical quantities."""
import json
from pathlib import Path
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent


def main():
    qa = HERE / 'build/figure_qa'
    qa.mkdir(parents=True, exist_ok=True)
    (qa / 'sail.contract.json').write_text(json.dumps({
        'claim': 'Initial task authority and a scoped human reply jointly determine whether a proposed tool effect may execute.',
        'role': 'Method schematic linking benchmark HIL stages to controller decisions.',
        'archetype': 'schematic-led composite', 'panels': 1,
        'data': 'No observed outcomes or numerical estimates; program structure only.',
        'backend': 'Python / Matplotlib', 'size_inches': [5.5, 2.6],
        'uncertainty': 'Not applicable to a method diagram.',
        'boundary': 'Semantic reviewers are fallible; tool arguments remain untrusted. One-use exact-call binding is implemented, general effect equivalence is not.',
        'reference_style': 'Original diagram; control/data separation in CaMeL informed the conceptual distinction, without reproducing its figure.'
    }, indent=2)+'\n')
    mpl.rcParams.update({'font.family':'sans-serif','font.sans-serif':['DejaVu Sans'],'font.size':7.2,
                         'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white'})
    fig, ax = plt.subplots(figsize=(5.5,2.6))
    fig.subplots_adjust(left=.02,right=.98,top=.96,bottom=.06)
    ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    ink,edge,blue,teal,orange='#263546','#728296','#E9F0F8','#E4F1ED','#FAEADC'
    def box(x,y,w,h,text,color):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.004,rounding_size=0.02',fc=color,ec=edge,lw=.65))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',color=ink,linespacing=1.4)
    def arrow(a,b):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=7,color=edge,lw=.8))
    box(.015,.73,.18,.23,'Original request\nTrusted authority',blue)
    box(.275,.73,.23,.23,'Compile initial scope\nNo workflow input',blue)
    box(.64,.73,.34,.23,'Review proposed effect\nWithin original scope?',blue)
    arrow((.20,.845),(.27,.845)); arrow((.51,.845),(.635,.845))
    box(.015,.34,.23,.24,'Native agent\nReads task artifacts\nProposes a tool call',orange)
    ax.plot([.25,.57,.57],[.46,.46,.845],color=edge,lw=.8)
    arrow((.57,.845),(.635,.845))
    ax.text(.40,.52,'Exact tool arguments',ha='center',va='bottom',fontsize=6.5,color=ink)
    box(.64,.35,.34,.24,'Missing authority\nAsk a scoped question\nCheck the actual reply',teal)
    arrow((.81,.725),(.81,.595))
    ax.text(.84,.665,'Needs help',ha='left',va='center',fontsize=6.5,color=ink)
    box(.365,.02,.27,.20,'One-use permission\nExecute exact call',teal)
    box(.72,.02,.26,.20,'No valid permission\nDefer this effect',orange)
    ax.plot([.70,.50],[.345,.345],color=edge,lw=.8)
    arrow((.50,.345),(.50,.225)); arrow((.85,.345),(.85,.225))
    ax.text(.405,.29,'Approved',ha='center',va='center',fontsize=6.5,color=ink)
    ax.text(.88,.28,'Unresolved',ha='left',va='center',fontsize=6.5,color=ink)
    ax.text(.02,.12,'Already authorized actions proceed.\nClassified hard violations are blocked.',
            ha='left',va='center',fontsize=6.5,color=ink,linespacing=1.5)
    fig.canvas.draw()
    skill=Path.home()/'.codex/skills/nature-figure/scripts'
    sys.path.insert(0,str(skill))
    from audit_panel_alignment import require_matplotlib_panel_alignment
    require_matplotlib_panel_alignment(fig,json_out=str(qa/'sail.alignment.json'),
        overlay_svg=str(qa/'sail.alignment.svg'),strict=True)
    fig.savefig(HERE/'figures/sail_method.pdf')
    fig.savefig(HERE/'figures/sail_method.svg')
    svg = HERE/'figures/sail_method.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(HERE/'figures/sail_method.png',dpi=600)
    plt.close(fig)


if __name__ == '__main__':
    main()
