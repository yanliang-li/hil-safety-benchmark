"""Reproduce the completed second-round utility loss that motivated v4."""
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'reports/sail-20260913/main-v3/per_case.csv'
    rows = list(csv.DictReader(source.open()))
    groups = {c: {(r['agent'], r['model'], r['case_id'], r['repeat']): r for r in rows if r['condition'] == c}
              for c in ('prompt_guard_v1', 'sail_v3')}
    left, right = groups['prompt_guard_v1'], groups['sail_v3']
    summary = defaultdict(lambda: {'matched_pairs': 0, 'prompt_bcr_count': 0, 'sail_bcr_count': 0, 'lost': 0, 'gained': 0})
    for key in sorted(set(left) & set(right)):
        l, r = left[key], right[key]
        a, b = l['benign_task_complete'] == 'True', r['benign_task_complete'] == 'True'
        value = summary[l['task_id']]
        value['matched_pairs'] += 1
        value['prompt_bcr_count'] += a
        value['sail_bcr_count'] += b
        value['lost'] += a and not b
        value['gained'] += b and not a
    for value in summary.values():
        value['net_loss'] = value['lost'] - value['gained']
    total = {k: sum(v[k] for v in summary.values()) for k in next(iter(summary.values()))}
    focal = ('invoice_reconciliation', 'policy_revision__resource_budget')
    output = {'source': str(source.relative_to(ROOT)), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'paired_totals': total, 'by_task': dict(summary),
        'two_diagnosed_tasks_net_loss': sum(summary[t]['net_loss'] for t in focal),
        'interpretation': 'Concentration is of NET loss, not all failed or lost episodes. Development diagnosis only, not independent validation of v4.'}
    path = ROOT / 'reports/sail-v4-20260913/v3_utility_diagnosis.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'paired_totals': total, 'two_task_net_loss': output['two_diagnosed_tasks_net_loss']}))


if __name__ == '__main__':
    main()
