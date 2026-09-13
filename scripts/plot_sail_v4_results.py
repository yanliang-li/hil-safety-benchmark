"""Plot completed paired safety/utility estimates, with no invented placeholders."""
import csv
import json
from pathlib import Path
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parents[1]
QA_TOOLS = Path.home() / '.codex/skills/nature-figure/scripts'
sys.path.insert(0, str(QA_TOOLS))
from audit_panel_alignment import require_matplotlib_panel_alignment


def main():
    rows = []
    sources = [('round2', 'Round 2', ROOT/'reports/sail-20260913/main-v3/summary.json', 'sail_v3'),
        ('round3', 'Round 3', ROOT/'reports/sail-v4-20260913/sail4-matched-r2/summary.json', 'sail_v4')]
    for phase, title, source, condition in sources:
        data = json.loads(source.read_text())
        if data['status'] != 'complete':
            raise ValueError('Quantitative paper plot requires completed formal phases')
        pair = data['aggregate_paired']['prompt_guard_v1__' + condition]
        for metric in ('unsafe_attack_success', 'benign_task_complete'):
            item = pair[metric]
            interval = item['task_cluster_bootstrap_95_interval']
            rows.append({'phase': phase, 'split_label': title, 'condition': condition,
                'metric': metric, 'paired_n': pair['matched_case_repeat_pairs'], 'task_clusters': pair['task_clusters'],
                'difference_pp': None if item['right_minus_left'] is None else 100 * item['right_minus_left'],
                'ci_low_pp': None if interval is None else 100 * interval[0],
                'ci_high_pp': None if interval is None else 100 * interval[1]})
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['DejaVu Sans'],
        'font.size': 8, 'axes.labelsize': 8, 'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5,
        'svg.fonttype': 'none', 'pdf.fonttype': 42, 'axes.spines.top': False,
        'axes.spines.right': False, 'legend.frameon': False})
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.8), sharey=True)
    fig.subplots_adjust(left=.32, right=.98, bottom=.2, top=.85, wspace=.26)
    labels = []
    for index, (ax, metric, title) in enumerate(zip(axes,
            ('unsafe_attack_success', 'benign_task_complete'), ('ASR: lower is better', 'BCR: higher is better'))):
        points = [r for r in rows if r['metric'] == metric]
        vals = [v for r in points for v in (r['difference_pp'], r['ci_low_pp'], r['ci_high_pp']) if v is not None]
        extent = max([abs(v) for v in vals] + [1]) * 1.2
        ax.set_xlim(-extent, extent)
        ax.set_ylim(len(points)-.4, -.6)
        ax.axvline(0, color='#9DA5AD', linewidth=.8, zorder=1)
        for y, row in enumerate(points):
            color = '#167D8D' if row['condition'] == 'sail_v4' else '#747F8A'
            label = row['split_label'] + '\n' + ('SAIL v4' if row['condition'] == 'sail_v4' else 'SAIL v3') + f" (n={row['paired_n']:,})"
            if index == 0:
                labels.append(label)
            if row['difference_pp'] is None:
                ax.text(.5, y, 'Not estimable', transform=ax.get_yaxis_transform(), ha='center', fontsize=7)
                continue
            if row['ci_low_pp'] is not None:
                ax.hlines(y, row['ci_low_pp'], row['ci_high_pp'], color=color, linewidth=1.2)
                ax.vlines([row['ci_low_pp'], row['ci_high_pp']], y-.07, y+.07, color=color, linewidth=1.0)
            ax.scatter(row['difference_pp'], y, color=color, marker='o' if row['condition'] == 'sail_v4' else 's', s=24, zorder=3)
        ax.set_yticks(range(len(points)))
        ax.set_yticklabels(labels if index == 0 else [''] * len(points))
        ax.tick_params(axis='y', length=0, pad=8)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.set_xlabel('Change from Prompt (pp)')
        ax.text(0, 1.08, 'ab'[index], transform=ax.transAxes, weight='bold', fontsize=9, va='bottom')
        ax.set_title(title, fontsize=8, pad=16)
    # sharey shares tick labels too; set left labels only after all axis setup.
    axes[0].set_yticklabels(labels)
    axes[1].tick_params(labelleft=False)
    qa = ROOT / 'paper/iclr2027/build/figure_qa'
    qa.mkdir(parents=True, exist_ok=True)
    out = ROOT / 'paper/iclr2027/figures'
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig, json_out=str(qa / 'sail_v4_results.alignment.json'), strict=True)
    fig.savefig(out / 'sail_v4_results.pdf', facecolor='white')
    fig.savefig(out / 'sail_v4_results.svg', facecolor='white')
    fig.savefig(out / 'sail_v4_results.png', dpi=600, facecolor='white')
    plt.close(fig)
    with (out / 'sail_v4_results_source.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    contract = {'question': 'Does SAIL v4 reduce ASR while increasing BCR relative to fresh Prompt?',
        'roles': {'a': 'Safety part of joint objective', 'b': 'Utility part of joint objective'},
        'archetype': 'two-panel paired comparison', 'backend': 'Python/matplotlib',
        'statistics': 'Right-minus-left proportions; 10,000 base-task cluster bootstrap draws; both-valid matched episodes.',
        'data_scope': 'Each round uses its own fresh Prompt control; all configurations retained. Engineering and failed/unmatched episodes are excluded by the estimand. Rounds are separate, not a direct concurrent v3-v4 contrast.',
        'failure_evidence': 'All-attempt failure and missing-outcome bounds remain in the main result files.',
        'width_note': '6.6-inch source is placed at ICLR 5.5-inch linewidth; 7.5-pt ticks render at 6.25 pt.',
        'semantic_boundary': 'Legacy effect scores; independent audit flags are not silently relabeled.'}
    (qa / 'sail_v4_results.contract.json').write_text(json.dumps(contract, indent=2) + '\n')
    for script, arguments in (
        ('validate_figure.py', [str(Path(__file__)), '--json']),
        ('audit_pdf_text.py', [str(out / 'sail_v4_results.pdf'), '--min-pt', '5', '--json']),
        ('audit_figure_collisions.py', [str(out / 'sail_v4_results.pdf'), '--json-out', str(qa / 'sail_v4_results.collisions.json'), '--overlay-pdf', str(qa / 'sail_v4_results.collisions.pdf')])):
        result = subprocess.run([sys.executable, str(QA_TOOLS / script), *arguments], text=True, capture_output=True)
        (qa / ('sail_v4_results.' + script.replace('.py', '.log'))).write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError('Figure QA requires review: ' + script)


if __name__ == '__main__':
    main()
