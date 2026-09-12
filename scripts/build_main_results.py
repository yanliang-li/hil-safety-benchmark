"""Build main-text tables from the completed, immutable four-framework matrix."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / 'reports/api-multimodel-20260912/four-frameworks'
    source = folder / 'summary.json'
    summary = json.loads(source.read_text())
    if summary['status'] != 'complete':
        raise ValueError('Main-text final results require a complete matrix')
    configs = summary['configurations']
    labels = {'codex': 'Codex', 'claude-code': 'Claude Code',
              'hermes': 'Hermes', 'deepseek-harness': 'DSH',
              'deepseek-v4-flash': 'DeepSeek V4 Flash',
              'glm-5.2': 'GLM 5.2', 'qwen3.7-max': 'Qwen 3.7 Max'}
    def rate(value):
        return 100 * value['numerator'] / value['denominator']
    lines = [r'\begin{table}[t]', r'\centering', r'\small',
             r'\caption{Completed four-framework comparison. Cells show neutral $\to$ prompt defense percentages. ASR is lower-is-better; the other rates are higher-is-better. Each condition schedules 240 runs per configuration; valid counts and all conditional denominators are in Appendix~\ref{app:api}.}',
             r'\label{tab:main_matrix}', r'\begin{tabular}{@{}llrrrr@{}}',
             r'\toprule', r'Framework & Requested model & ASR & BCR & HIL recall & PostSuccess \\', r'\midrule']
    for x in configs:
        left, right = (x['conditions'][c] for c in ['neutral', 'prompt_guard_v1'])
        cells = [labels[x['agent']], labels[x['model']]]
        for key in ['unsafe_asr', 'benign_completion', 'hil_recall', 'strict_post_feedback']:
            cells.append(f"{rate(left[key]):.1f}$\\to${rate(right[key]):.1f}")
        lines.append(' & '.join(cells) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}', r'\end{table}']
    (ROOT / 'paper/iclr2027/tables/main_matrix.tex').write_text('\n'.join(lines) + '\n')
    with (folder / 'per_case.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    totals = {}
    for condition in ['neutral', 'prompt_guard_v1']:
        selected = [x for x in rows if x['condition'] == condition]
        totals[condition] = {
            'valid_runs': len(selected),
            'unsafe_without_matched_question': sum(x['unsafe_attack_success'] == 'True' and x['asked_human'] == 'False' for x in selected),
            'unsafe_after_matched_question': sum(x['unsafe_attack_success'] == 'True' and x['asked_human'] == 'True' for x in selected),
            'approved_consulted': sum(x['authorization_mode'] == 'confirmable' and x['response_category'] == 'clear_approve' and x['asked_human'] == 'True' for x in selected),
            'approved_executed': sum(x['authorization_mode'] == 'confirmable' and x['response_category'] == 'clear_approve' and x['asked_human'] == 'True' and x['attack_effect_executed'] == 'True' for x in selected),
            'human_questions': sum(int(x['total_human_questions']) for x in selected),
        }
        for metric in ['unsafe_asr', 'benign_completion', 'joint_safe_utility', 'hil_recall', 'strict_post_feedback', 'hard_prohibition_block']:
            values = [x['conditions'][condition][metric] for x in configs]
            totals[condition][metric] = {key: sum(v[key] for v in values) for key in ['numerator', 'denominator']}
    evidence = {'source': str(source.relative_to(ROOT)), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'totals': totals}
    (ROOT / 'paper/iclr2027/main_results_evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(evidence))


if __name__ == '__main__':
    main()
