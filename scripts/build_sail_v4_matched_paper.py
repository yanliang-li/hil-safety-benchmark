"""Report the equal-scale third round, preserving the first two historical rounds."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from build_sail_v4_paper import historical, pct, ci_text, DISPLAY

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT/'paper/iclr2027'
REPORT = ROOT/'reports/sail-v4-20260913'
SOURCE = REPORT/'sail4-matched-r2/summary.json'
CONDITIONS = ('prompt_guard_v1','sail_v4','sail_v4_no_human')


def write_table(name, header, rows, caption, columns, small=True):
    content = [r'\begin{table}[t]' if small else r'\begin{table}[p]',
        r'\centering\small' if small else r'\centering\scriptsize', r'\setlength{\tabcolsep}{3pt}',
        r'\begin{tabular}{'+columns+'}', r'\toprule', ' & '.join(header)+r' \\', r'\midrule']
    content += [' & '.join(str(x) for x in row)+r' \\' for row in rows]
    content += [r'\bottomrule',r'\end{tabular}',r'\caption{'+caption+'}',r'\label{tab:'+name+'}',r'\end{table}']
    (PAPER/'tables'/f'{name}.tex').write_text('\n'.join(content)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-complete',action='store_true')
    args = parser.parse_args()
    history = historical()
    observed = json.loads(SOURCE.read_text()) if SOURCE.exists() else {'status':'pending','aggregate':{}}
    complete = observed['status'] == 'complete'
    if complete and (observed.get('planned_attempts') != 6720 or set(observed['aggregate']) != set(CONDITIONS)):
        raise ValueError('Completed report does not match the active 6720-attempt design')
    if args.require_complete and not complete:
        raise ValueError('All 6720 formal attempts must finish before final claims')
    # Provisional observations remain in the live phase report, outside paper tables.
    third = observed if complete else {'status':'pending','aggregate':{}}
    history['round3'] = {'status':third['status'],'formal_planned_attempts':6720,
        'engineering_preflights_excluded':True,'scope':'same second-round cases/configurations/repeats; defense replaced; main before ablation',
        'main_attempts':5760,'ablation_attempts':960,'execution_order':'main_then_ablation',
        'phases':{'matched':third},'expanded_validation_cancelled_before_formal_start':True}
    REPORT.mkdir(parents=True,exist_ok=True)
    (REPORT/'three_rounds.json').write_text(json.dumps(history,indent=2)+'\n')
    records=[]
    lines=['# 三轮实验对照','','第三轮沿用第二轮的80案例、4框架、3模型路线、重复次数和评分器，仅替换防御策略及其无人工回复消融。正式次数为6720。工程预检单独保留。',
        '', '| 轮次 | 条件 | 有效数 | ASR | BCR | 联合安全完成率 |','|---|---|---:|---:|---:|---:|']
    for label,data in [('第一轮',history['round1']),('第二轮',history['round2']),('第三轮',third)]:
        if not data['aggregate']:
            lines.append(f'| {label} | 正式结果未完成 | -- | -- | -- | -- |')
        for c,m in data['aggregate'].items():
            n=m['benign_completion']['denominator']
            lines.append(f"| {label} | {DISPLAY[c]} | {n} | {pct(m['unsafe_asr'])} | {pct(m['benign_completion'])} | {pct(m['joint_safe_utility'])} |")
            records.append(dict(round_phase=label,condition=c,status=data['status'],valid_runs=n,
                asr_numerator=m['unsafe_asr']['numerator'],asr_denominator=m['unsafe_asr']['denominator'],
                bcr_numerator=m['benign_completion']['numerator'],bcr_denominator=m['benign_completion']['denominator']))
    lines += ['', '第三轮重新运行Prompt基线。主结论使用同轮、同配置、同案例、同重复且双方有效的配对，不将跨轮边际比例当作同期因果比较。所有失败、调用量、置信区间及独立效果审计保留。',
        '', '此前33840次扩展方案已在正式启动前取消：新增任务、干净对照、旧v3重跑和无恢复消融均不在本轮范围。已生成的材料是未评测的未来工作。']
    with (REPORT/'three_rounds.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    body=[r'\subsection{Can recovery improve safety and task completion?}',r'\label{sec:sailv4results}','']
    appendix=[r'\section{Third-Round Detailed Results}',r'\label{app:sailv4results}','']
    if not complete:
        body += [r'The revised controller is implemented, and engineering checks are in progress. The third round retains the same 80 cases, twelve framework--model configurations, and repeat allocation as round two. The 5,760 main attempts compare fresh Prompt and full SAIL v4, with three repeats each. All main attempts finish before the 960 no-human ablation attempts start. Formal results are pending; engineering checks do not support a performance claim. Appendix~\ref{app:sailv4} gives the protocol.']
        appendix += ['Formal third-round results are pending. This round evaluates the same development cases as round two. New tasks, clean counterparts, a concurrent v3 arm, and a no-recovery ablation are outside its scope.']
        status=r'\draftnote{Internal manuscript. Two rounds are complete. The equal-scale 6,720-attempt SAIL v4 round is pending. Engineering results are excluded; independent semantic annotation and author review remain incomplete.}'
    else:
        pair=third['aggregate_paired']['prompt_guard_v1__sail_v4']
        if third['observed_double_improvement']:
            inference='The paired point estimates meet both objectives. '+('Both task-cluster intervals support their directions.' if third['both_directional_intervals_supported'] else 'The intervals do not establish both directions, so the joint improvement remains descriptive.')
        else:
            inference='The paired point estimates do not meet lower ASR and higher BCR together.'
        body += [f"All 6,720 formal attempts finish, with {third['valid_runs']:,} valid runs and {third['failed_attempts']:,} failures. Cases, framework images, model routes, and repeat allocation match round two. The 5,760 main attempts finish before the 960 ablation attempts start. Prompt is rerun alongside the revised defense; historical v3 results remain a separate comparison.",r'\input{tables/sail_v4_matched_main}',
            f"The primary comparison contains {pair['matched_case_repeat_pairs']:,} valid pairs. SAIL v4 minus Prompt changes ASR by {ci_text(pair['unsafe_attack_success'])} and BCR by {ci_text(pair['benign_task_complete'])}. {inference}"]
        flags=sum(sum(m['all_attempt_audit_flags'].values()) for m in third['aggregate'].values())
        body += [f"Independent effect and deliverable checks record {flags:,} flags across all attempts, with multiple flags possible per episode. They do not change legacy scores. Failure bounds and unresolved semantic judgments limit the inference; Appendix~\\ref{{app:sailv4results}} gives all configurations, human-feedback metrics, and costs."]
        main_rows=[];matrix=[];hil=[]
        for c in CONDITIONS:
            m=third['aggregate'][c]
            main_rows.append([DISPLAY[c],m['valid_runs'],sum(m['failures'].values()),pct(m['unsafe_asr'],True),pct(m['benign_completion'],True)])
            hil.append([DISPLAY[c],pct(m['hil_recall'],True),pct(m['question_precision_rule_proxy'],True),pct(m['strict_post_feedback'],True),pct(m['approved_execution_all_eligible'],True)])
        write_table('sail_v4_matched_main',['Condition','Valid $n$','Failed','ASR','BCR'],main_rows,
            'Third-round marginal valid-run proportions. Primary inference uses matched pairs against the fresh Prompt baseline.','lrrrr')
        for config in third['configurations']:
            for c in CONDITIONS:
                m=config['conditions'][c]
                matrix.append([config['agent'],config['model'],DISPLAY[c],m['benign_completion']['denominator'],pct(m['unsafe_asr'],True),pct(m['benign_completion'],True)])
        write_table('sail_v4_matched_matrix',['Framework','Requested route','Condition','Valid $n$','ASR','BCR'],matrix,
            'All twelve configurations in the equal-scale third round. Requested routes do not verify the underlying model weights.','lllrrr',small=False)
        write_table('sail_v4_matched_hil',['Condition','HIL recall','Question proxy','PostSuccess','Approved safe'],hil,
            'HIL and utility diagnostics. Approved safe execution uses all eligible confirmable approval cases, including unconsulted cases. Question matching is a rule proxy; autonomous recognition and semantic question accuracy remain unannotated. Exact denominators are retained in the source report.','lrrrr',small=False)
        appendix += [r'\input{tables/sail_v4_matched_matrix}',r'\input{tables/sail_v4_matched_hil}',
            'The task and attack-family clustered comparisons, all-attempt failure categories, and effect-audit flags are retained in the derived reports. Both conditions must be valid to enter a paired estimate. Earlier v3 runs are not treated as concurrent controls.']
        ablation=third['aggregate_paired']['sail_v4_no_human__sail_v4']
        appendix += [f"Full SAIL v4 minus its no-human ablation uses {ablation['matched_case_repeat_pairs']:,} repeat-1 pairs. ASR changes by {ci_text(ablation['unsafe_attack_success'])}; BCR changes by {ci_text(ablation['benign_task_complete'])}. The ablation is run afterward, so changes in serving conditions may affect this comparison."]
        for c in CONDITIONS:
            m=third['aggregate'][c];b=third['all_attempt_sensitivity'][c];u=m['all_attempt_usage']
            appendix += [f"\\paragraph{{{DISPLAY[c]}.}} All-attempt ASR bounds are {100*b['lower_unsafe_count']/b['planned']:.2f}--{100*b['upper_unsafe_count_including_pending']/b['planned']:.2f}\\%. These are missing-outcome bounds, not sampling intervals. There are {u['actor_requests']:,} actor and {u['reviewer_requests']:,} reviewer requests; usage is reported for {u['actor_requests_with_usage']:,} and {u['reviewer_requests_with_usage']:,}, respectively."]
        subprocess.run([sys.executable,'scripts/plot_sail_v4_results.py'],cwd=ROOT,check=True)
        appendix += [r'\begin{figure}[p]',r'\centering\includegraphics[width=\linewidth]{figures/sail_v4_results.pdf}',
            r'\caption{Each round compares its defense with its own fresh Prompt control on matched valid episodes. Bars show descriptive 95\% task-cluster intervals. These are separate within-round estimates, not a direct randomized v3--v4 comparison.}',r'\end{figure}']
        prompt,full=third['aggregate']['prompt_guard_v1'],third['aggregate']['sail_v4']
        abstract=r'''Human consultation must control an agent's actions while preserving its legitimate task. We introduce \bench{} to measure this intervention loop under indirect attacks. Its core contains 250 tasks, each paired with approval, denial, ambiguity, and scope-mismatched feedback. Two exploratory rounds expose missing consultation, misuse of replies, and lost authorized work. These failures motivate a revised \sail{} controller that preserves original authority, binds human-approved extensions to their scope, and recovers unfinished task steps. We test four native frameworks with three model routes. The third round replaces the earlier defense within the same 80-case, 6,720-attempt design. '''
        abstract+=f"Prompt and SAIL v4 have attack success rates of {pct(prompt['unsafe_asr'],True)} and {pct(full['unsafe_asr'],True)}, with benign completion of {pct(prompt['benign_completion'],True)} and {pct(full['benign_completion'],True)}. {inference} "
        abstract+='Synthetic replies, simulated effects, reused development tasks, unverified model routes, and unresolved effect-audit flags bound these findings.\n'
        (PAPER/'sections/00_abstract.tex').write_text(abstract)
        discussion=[r'\section{Discussion and Conclusion}',r'\label{sec:conclusion}','',
            'Human intervention requires identifying a missing decision, applying the reply within scope, and completing authorized work. The first two rounds show that stronger blocking can still lose legitimate task steps. The revised controller addresses this loss by preserving original permission and recovering task progress.',inference,
            'The third round retains the earlier experimental scale and includes a fresh Prompt control. Cross-round changes in model serving and execution prevent interpreting a historical v3--v4 difference as a concurrent causal effect. The no-human ablation tests feedback access within the revised controller; recovery is not separately isolated in this round.',
            'All model evaluations reuse development tasks with fixed synthetic replies and simulated tool consequences. Effect predicates do not establish full semantic correctness. Uneven failures and cumulative-effect or deliverable audit conflicts must be considered alongside the valid-run rates. Independent annotations, new tasks, clean controls, and real human feedback remain necessary for broader claims.',
            r'\bench{} connects questions, replies, and later effects in one observable protocol. The method experiment tests whether this loop can protect the task as well as constrain an attack.']
        (PAPER/'sections/06_discussion.tex').write_text('\n\n'.join(discussion)+'\n')
        status=r'\draftnote{Internal manuscript. All three repeated rounds are complete. The third round matches the second-round experimental scale. Independent semantic annotation, effect-flag adjudication, and author review remain incomplete.}'
        lines += ['',f"第三轮有效配对 {pair['matched_case_repeat_pairs']} 对；点估计同时改善：{third['observed_double_improvement']}；两个区间均支持方向：{third['both_directional_intervals_supported']}。"]
    (REPORT/'THREE_ROUNDS_ZH.md').write_text('\n'.join(lines)+'\n')
    for name,text in [('05c_sail_v4_results','\n\n'.join(body)),('13_sail_v4_results','\n\n'.join(appendix)),('sail_status',status)]:
        (PAPER/'sections'/f'{name}.tex').write_text(text+'\n')
    evidence={'third_round_complete':complete,'formal_attempts':6720,'preflights_excluded':True,
        'three_round_report_sha256':hashlib.sha256((REPORT/'three_rounds.json').read_bytes()).hexdigest(),
        'formal_sources':{'matched':hashlib.sha256(SOURCE.read_bytes()).hexdigest()} if SOURCE.exists() else {}}
    (PAPER/'sail_v4_results_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps({'third_round_complete':complete,'formal_attempts':6720,'scope':'match_second_round'}))


if __name__ == '__main__':
    main()
