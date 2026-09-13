"""Populate the manuscript and three-round report from observed result artifacts."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper/iclr2027'
REPORT = ROOT / 'reports/sail-v4-20260913'
DISPLAY = {'neutral': 'Neutral', 'prompt_guard_v1': 'Prompt', 'sail_v3': 'SAIL v3', 'sail_v3_no_human': 'SAIL v3, no human',
    'sail_v4': 'SAIL v4', 'sail_v4_no_recovery': 'SAIL v4, no recovery', 'sail_v4_no_human': 'SAIL v4, no human'}
PHASES = {'regression': 'Original-case regression', 'heldout': 'Task-ID validation', 'clean': 'Clean counterparts'}


def read(path):
    return json.loads(path.read_text())


def fraction(n, d):
    return {'numerator': n, 'denominator': d}


def pct(value, latex=False):
    if not value or not value['denominator']:
        return '--'
    return f"{100*value['numerator']/value['denominator']:.2f}" + (r'\%' if latex else '%')


def historical():
    path = ROOT / 'reports/api-multimodel-20260912/four-frameworks/per_case.csv'
    rows = list(csv.DictReader(path.open()))
    first = {}
    for condition in ('neutral', 'prompt_guard_v1'):
        rr = [r for r in rows if r['condition'] == condition]
        first[condition] = {'valid_runs': len(rr),
            'unsafe_asr': fraction(sum(r['unsafe_attack_success'] == 'True' for r in rr), len(rr)),
            'benign_completion': fraction(sum(r['benign_task_complete'] == 'True' for r in rr), len(rr)),
            'joint_safe_utility': fraction(sum(r['joint_safe_utility'] == 'True' for r in rr), len(rr))}
    second_path = ROOT / 'reports/sail-20260913/main-v3/summary.json'
    second = read(second_path)
    return {'round1': {'status': 'complete', 'planned_attempts': 5760, 'valid_runs': 5551, 'failed_attempts': 209,
                'aggregate': first, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()},
            'round2': {'status': second['status'], 'planned_attempts': second['planned_attempts'],
                'valid_runs': second['valid_runs'], 'failed_attempts': second['failed_attempts'],
                'aggregate': second['aggregate'], 'source_sha256': hashlib.sha256(second_path.read_bytes()).hexdigest()}}


def ci_text(metric):
    value = metric['right_minus_left']
    interval = metric.get('task_cluster_bootstrap_95_interval')
    if value is None:
        return 'not estimable'
    text = f'{100*value:+.2f} points'
    if interval:
        text += f' (95\\% task-cluster interval [{100*interval[0]:+.2f}, {100*interval[1]:+.2f}])'
    else:
        text += ' (interval unavailable)'
    return text


def main():
    scope_path = ROOT / 'experiments/sail-v4-20260913/authorized_scope.json'
    if scope_path.exists() and read(scope_path).get('scope') == 'match_second_round':
        from build_sail_v4_matched_paper import main as matched_main
        return matched_main()
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    REPORT.mkdir(parents=True, exist_ok=True)
    history = historical()
    third = {}
    for phase in PHASES:
        path = REPORT / f'sail4-{phase}-r2/summary.json'
        third[phase] = read(path) if path.exists() else {'status': 'pending', 'aggregate': {}}
    complete = all(value['status'] == 'complete' for value in third.values())
    if args.require_complete and not complete:
        raise ValueError('Wait for every frozen formal phase before final manuscript claims')
    history['round3'] = {'status': 'complete' if complete else 'pending_or_incomplete', 'phases': third,
        'formal_planned_attempts': 33840, 'engineering_preflights_excluded': True}
    (REPORT / 'three_rounds.json').write_text(json.dumps(history, indent=2) + '\n')
    lines = ['# 三轮实验对照', '', '前两轮已完成，第三轮仅使用正式阶段结果。工程预检不进入本表。不同轮次的边际比例不能替代同轮配对比较。', '',
        '| 轮次／阶段 | 条件 | 有效数 | ASR | BCR | 联合安全完成率 |', '|---|---|---:|---:|---:|---:|']
    records = []
    entries = [('第一轮', history['round1']), ('第二轮', history['round2'])]
    entries += [('第三轮 ' + PHASES[p], value) for p, value in third.items()]
    for label, value in entries:
        if not value['aggregate']:
            lines.append(f'| {label} | 尚无正式结果 | -- | -- | -- | -- |')
        for condition, metrics in value['aggregate'].items():
            n = metrics.get('valid_runs', metrics['benign_completion']['denominator'])
            lines.append(f"| {label} | {DISPLAY[condition]} | {n} | {pct(metrics.get('unsafe_asr'))} | {pct(metrics['benign_completion'])} | {pct(metrics.get('joint_safe_utility'))} |")
            records.append({'round_phase': label, 'condition': condition, 'status': value['status'], 'valid_runs': n,
                'asr_numerator': (metrics.get('unsafe_asr') or {}).get('numerator'),
                'asr_denominator': (metrics.get('unsafe_asr') or {}).get('denominator'),
                'bcr_numerator': metrics['benign_completion']['numerator'], 'bcr_denominator': metrics['benign_completion']['denominator']})
    lines += ['', '第二轮 2,355 对有效配对中，BCR 净减少 170 次；两个资源任务占其中 169 次。这是新方法的开发依据，不是新方法有效的证据。', '',
        '第三轮主目标：相对同轮 Prompt，ASR 下降且 BCR 上升。主分析保留同配置、同案例、同重复且双方有效的配对；同时报告所有失败、置信区间、费用和独立审计冲突。干净对照不计算攻击 ASR，询问率也不是误报率。']
    for phase in ('regression', 'heldout'):
        value = third[phase]
        if value['status'] == 'complete':
            pair = value['aggregate_paired']['prompt_guard_v1__sail_v4']
            lines += ['', f"{PHASES[phase]}：{pair['matched_case_repeat_pairs']} 对；观察到双指标改善：{value['observed_double_improvement']}；两个区间均支持方向：{value['both_directional_intervals_supported']}。",
                '该判断还需结合 effect_audit.json 中的累计效果、工具等价性和交付物标记解读。']
    (REPORT / 'THREE_ROUNDS_ZH.md').write_text('\n'.join(lines) + '\n')
    with (REPORT / 'three_rounds.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    body = [r'\subsection{Can recovery improve safety and task completion?}', r'\label{sec:sailv4results}', '']
    appendix = [r'\section{Third-Round Detailed Results}', r'\label{app:sailv4results}', '']
    if not complete:
        body += [r'The revised controller is implemented, and engineering preflights are in progress. The formal design contains 33,840 attempts across original-case regression, task-ID validation, and clean counterparts. No third-round performance claim is made until all frozen phases finish. Appendix~\ref{app:sailv4} specifies the comparisons and evidence boundaries.']
        appendix += ['Formal third-round results are pending. Engineering traces are preserved separately and excluded from the result tables.']
        status = r'\draftnote{Internal manuscript. The first two repeated comparisons are complete. SAIL v4 is implemented; third-round formal results are pending. Semantic annotation and author review remain incomplete.}'
    else:
        total_valid = sum(v['valid_runs'] for v in third.values())
        total_failed = sum(v['failed_attempts'] for v in third.values())
        body += [f'The third round completes all 33,840 formal attempts, with {total_valid:,} valid runs and {total_failed:,} failures. Engineering preflights are excluded. Each phase uses fresh interleaved controls; the earlier rounds remain separate.', '', r'\input{tables/sail_v4_main}', '']
        for phase in ('regression', 'heldout'):
            value = third[phase]
            pair = value['aggregate_paired']['prompt_guard_v1__sail_v4']
            body += [f"In {PHASES[phase].lower()}, {pair['matched_case_repeat_pairs']:,} valid pairs compare SAIL v4 with Prompt. ASR changes by {ci_text(pair['unsafe_attack_success'])}. BCR changes by {ci_text(pair['benign_task_complete'])}.", '']
        held = third['heldout']
        if held['observed_double_improvement']:
            body += ['The validation point estimates meet the joint objective of lower ASR and higher BCR. ' +
                ('Both task-cluster intervals support their respective directions.' if held['both_directional_intervals_supported'] else
                 'The two task-cluster intervals do not both support their respective directions, so the joint improvement remains descriptive.'), '']
        else:
            body += ['The validation point estimates do not meet both objectives together. The revised method therefore does not establish the requested joint improvement on this split.', '']
        flags = sum(sum(v['aggregate'][c]['all_attempt_audit_flags'].values()) for v in third.values() for c in v['aggregate'])
        body += [f'The independent audit records {flags:,} effect or deliverable flags across all attempts; one episode may receive multiple flags. These do not alter legacy scores. Appendix~\ref{{app:sailv4results}} reports the ablations, clean controls, failures, and scoring disagreements.']
        status = r'\draftnote{Internal manuscript. All three experiment rounds are complete. Effect-audit flags, missing semantic labels, and author review still bound the conclusions.}'
        table = [r'\begin{table}[t]', r'\centering\small', r'\begin{tabular}{llrrr}', r'\toprule',
            r'Split & Condition & Valid $n$ & ASR & BCR \\', r'\midrule']
        for phase in ('regression', 'heldout'):
            for condition in ('prompt_guard_v1', 'sail_v3', 'sail_v4'):
                m = third[phase]['aggregate'][condition]
                table.append(f"{'Original80' if phase == 'regression' else 'Task-ID validation'} & {DISPLAY[condition]} & {m['valid_runs']:,} & {pct(m['unsafe_asr'], True)} & {pct(m['benign_completion'], True)} " + r'\\')
        table += [r'\bottomrule', r'\end{tabular}', r'\caption{Third-round valid-run proportions. Paired task-cluster estimates, rather than differences between these marginal proportions, support the main comparison.}', r'\label{tab:sailv4main}', r'\end{table}']
        (PAPER / 'tables/sail_v4_main.tex').write_text('\n'.join(table) + '\n')
        appendix += [r'These tables retain every requested framework--model configuration and each frozen condition. Requested model routes do not verify underlying weights. All primary proportions exclude failed episodes; all-attempt bounds and cost retain them.', '']
        for phase, value in third.items():
            groups = [('main', ('prompt_guard_v1', 'sail_v3', 'sail_v4'))]
            if phase != 'clean':
                groups.append(('ablations', ('sail_v4_no_recovery', 'sail_v4_no_human')))
            # Keep every configuration, but separate the 36 main-condition rows
            # from the 24 ablation rows so each float fits one official page.
            for group, conditions in groups:
                table = [r'\begin{table}[p]', r'\centering\scriptsize', r'\setlength{\tabcolsep}{3pt}',
                    r'\begin{tabular}{lllrrr}', r'\toprule', r'Framework & Requested route & Condition & Valid $n$ & ASR & BCR \\', r'\midrule']
                for config in value['configurations']:
                    for condition in conditions:
                        m = config['conditions'][condition]
                        table.append(f"{config['agent']} & {config['model']} & {DISPLAY[condition]} & {m['benign_completion']['denominator']} & {pct(m.get('unsafe_asr'), True)} & {pct(m['benign_completion'], True)} " + r'\\')
                table += [r'\bottomrule', r'\end{tabular}', '\\caption{' + PHASES[phase] + ' (' + ('main conditions' if group == 'main' else 'ablations') + r'). Clean controls have no attack ASR. Full counts, paired intervals, request/token coverage, and independent audit flags are preserved in the derived result files.}', r'\end{table}']
                name = 'sail_v4_' + phase + '_matrix_' + group
                (PAPER / 'tables' / (name + '.tex')).write_text('\n'.join(table) + '\n')
                appendix += [r'\input{tables/' + name + '}', '']
            appendix += [f"\\paragraph{{{PHASES[phase]}.}} {value['valid_runs']:,} valid runs and {value['failed_attempts']:,} failed attempts were retained."]
            if phase != 'clean':
                for condition, bounds in value['all_attempt_sensitivity'].items():
                    appendix.append(f"{DISPLAY[condition]} has legacy all-attempt ASR bounds of {100*bounds['lower_unsafe_count']/bounds['planned']:.2f}--{100*bounds['upper_unsafe_count_including_pending']/bounds['planned']:.2f}\\%.")
                for left in ('sail_v4_no_recovery', 'sail_v4_no_human'):
                    pair = value['aggregate_paired'][left + '__sail_v4']
                    appendix.append(f"Full SAIL v4 minus {DISPLAY[left]} uses {pair['matched_case_repeat_pairs']:,} pairs. Its ASR difference is {ci_text(pair['unsafe_attack_success'])}; its BCR difference is {ci_text(pair['benign_task_complete'])}.")
            else:
                appendix.append('Raw question rates include legitimate unresolved decisions and are not unnecessary-question rates. Nonempty deliverables and effect completion do not establish semantic correctness.')
            for condition, m in value['aggregate'].items():
                usage = m['all_attempt_usage']
                appendix.append(f"{DISPLAY[condition]} records {usage.get('actor_requests', 0):,} actor and {usage.get('reviewer_requests', 0):,} reviewer requests. Reported usage is available for {usage.get('actor_requests_with_usage', 0):,} and {usage.get('reviewer_requests_with_usage', 0):,} requests, respectively.")
            appendix += ['']
        subprocess.run([sys.executable, 'scripts/plot_sail_v4_results.py'], cwd=ROOT, check=True)
        appendix += [r'\begin{figure}[p]', r'\centering', r'\includegraphics[width=\linewidth]{figures/sail_v4_results.pdf}',
            r'\caption{Matched ASR and BCR changes relative to the fresh Prompt baseline. Bars show descriptive 95\% task-cluster bootstrap intervals. Negative ASR and positive BCR changes are desirable. The two panels test the two parts of the joint objective.}', r'\end{figure}']
    (PAPER / 'sections/05c_sail_v4_results.tex').write_text('\n'.join(body) + '\n')
    (PAPER / 'sections/13_sail_v4_results.tex').write_text('\n'.join(appendix) + '\n')
    (PAPER / 'sections/sail_status.tex').write_text(status + '\n')
    if complete:
        held = third['heldout']
        prompt, full = held['aggregate']['prompt_guard_v1'], held['aggregate']['sail_v4']
        if held['observed_double_improvement']:
            inference = ('Both paired task-cluster intervals support their respective directions.'
                if held['both_directional_intervals_supported'] else
                'Paired point estimates improve both metrics, but the intervals do not establish both directions.')
        else:
            inference = 'The paired comparison does not support lower attack success and higher benign completion together.'
        abstract = r'''Human consultation must control an agent's actions while preserving its legitimate task. We introduce \bench{} to measure this intervention loop under indirect attacks. Its core contains 250 tasks, each paired with approval, denial, ambiguity, and scope-mismatched feedback. Two exploratory rounds expose missing consultation, misuse of replies, and lost authorized work. These failures motivate a revised \sail{} controller that separates original authority from human-approved extensions and recovers unfinished task steps. We test four native frameworks with three model routes. The third round contains 33,840 formal attempts across reused tasks, previously unrun task identifiers, and separate clean counterparts. '''
        abstract += f"On task-ID validation, Prompt and SAIL v4 have attack success rates of {pct(prompt['unsafe_asr'], True)} and {pct(full['unsafe_asr'], True)}. Their benign completion rates are {pct(prompt['benign_completion'], True)} and {pct(full['benign_completion'], True)}. {inference} "
        abstract += 'These comparisons retain the frozen scorer and report independent effect-audit conflicts. Fixed synthetic replies, simulated consequences, reused templates, and uneven failures limit interpretation.\n'
        (PAPER / 'sections/00_abstract.tex').write_text(abstract)
        discussion = [r'\section{Discussion and Conclusion}', r'\label{sec:conclusion}', '',
            'Human intervention has three linked requirements: identify a missing decision, use the returned reply within scope, and complete the authorized task. The first two rounds show that improving one stage can leave another unresolved. The revised controller tests whether preserving original authority and recovering task progress addresses that loss.', '',
            inference + ' This conclusion concerns the stated task-ID split and frozen effect scorer. It does not establish general semantic safety or transfer to unseen attack families.', '',
            'Task alignment, privilege control, and runtime recovery already have substantial prior work. Our method connects these ideas to a benchmark that varies the validity and scope of feedback. The no-recovery and no-human comparisons test two components within this controller, while its additional model calls remain a cost of the intervention.', '',
            'Independent audit flags matter when cumulative operations or alternate tool realizations disagree with single-call predicates. Nonempty reports also do not establish factual task completion. Uneven failures can change conclusions drawn from valid episodes, so missing-outcome bounds accompany the primary rates.', '',
            r'\bench{} makes asking, reply interpretation, and later tool effects observable within one protocol. The present evidence uses synthetic replies and simulated consequences. Real human decisions, independent semantic annotations, and attacks outside the current generator families are needed to test broader human control.']
        (PAPER / 'sections/06_discussion.tex').write_text('\n'.join(discussion) + '\n')
    evidence = {'three_round_report_sha256': hashlib.sha256((REPORT / 'three_rounds.json').read_bytes()).hexdigest(),
        'third_round_complete': complete, 'preflights_excluded': True,
        'formal_sources': {p: hashlib.sha256((REPORT / f'sail4-{p}-r2/summary.json').read_bytes()).hexdigest()
            for p in PHASES if (REPORT / f'sail4-{p}-r2/summary.json').exists()}}
    (PAPER / 'sail_v4_results_evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'third_round_complete': complete, 'three_round_report': 'reports/sail-v4-20260913/THREE_ROUNDS_ZH.md'}))


if __name__ == '__main__':
    main()
