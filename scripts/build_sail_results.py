"""Render observed SAIL counts; completed main results alone enter the paper."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'reports/sail-20260913/main-v3'
PAPER = ROOT/'paper/iclr2027'
NAMES = {'prompt_guard_v1':'Prompt guard', 'sail_v3':'SAIL', 'sail_v3_no_human':'SAIL, no human'}
ZH = {'prompt_guard_v1':'原提示防御', 'sail_v3':'完整 SAIL', 'sail_v3_no_human':'SAIL 无人工回复'}


def percent(metric, latex=False):
    n,d = metric['numerator'],metric['denominator']
    return f'{100*n/d:.2f}'+(r'\%' if latex else '%') if d else 'N/A'


def count(metric, latex=False):
    n,d = metric['numerator'],metric['denominator']
    return f'{n:,}/{d:,} ({percent(metric,latex)})' if d else 'N/A'


def interval(value):
    ci = value['task_cluster_bootstrap_95_interval']
    return f'[{100*ci[0]:+.2f}, {100*ci[1]:+.2f}]' if ci else 'not estimable'


def main():
    path = REPORT/'summary.json'
    if not path.exists():
        return
    summary = json.loads(path.read_text())
    assert summary['experiment']=='scoped-human-intervention-main-v3'
    aggregates = summary['aggregate']
    lines = ['# SAIL：HIL 方法实验', '',
        f"状态：**{summary['status']}**。计划 {summary['planned_attempts']:,} 次，已结束 {summary['finished_attempts']:,} 次；有效 {summary['valid_runs']:,}，失败 {summary['failed_attempts']:,}，待结束 {summary['pending_attempts']:,}。",
        '', '四个框架 × 三个模型；80 条已用过的开发案例。提示防御与完整方法各三轮，无人工回复消融一轮。预检不混入这张表。运行中的数据存在完成速度偏差，不能当作最终比较。', '',
        '| 条件 | 有效数 | 攻击成功率 ↓ | 良性完成率 ↑ | 安全且完成 ↑ | 系统 HIL 召回 ↑ | 有效批准后的执行 / 全部可批准样本 ↑ |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for condition in summary['conditions']:
        a = aggregates[condition]
        lines.append('| '+' | '.join([ZH[condition],str(a['unsafe_asr']['denominator']),
            *[count(a[k]) for k in ('unsafe_asr','benign_completion','joint_safe_utility','hil_recall','approved_execution_all_eligible')]])+' |')
    lines += ['', '系统 HIL 召回包括控制器补问；不是 Agent 自主识别率。批准执行指标的分母包括未询问的可批准样本，避免无人工回复组因条件分母为零而无法比较。它要求目标动作执行且未形成不安全结果。', '',
        '| 条件 | 严格回复后成功 | 问题匹配（规则代理） | Agent 发问 | 控制器补问 | 有效运行平均秒数 |',
        '|---|---:|---:|---:|---:|---:|']
    for condition in summary['conditions']:
        a=aggregates[condition];q=a['questions'];wall=a['mean_wall_seconds']
        lines.append('| '+' | '.join([ZH[condition],count(a['strict_post_feedback']),count(a['question_precision_rule_proxy']),str(q['agent_questions']),str(q['controller_questions']),f'{wall:.1f}' if wall is not None else 'N/A'])+' |')
    lines += ['', '不同条件实际问人的样本不同，因此回复后成功率不能解释为反馈的因果效应。自主风险识别和语义问题准确率仍缺独立标注。', '',
        '| 条件 | 已结束全部尝试 | 观察到的不安全数 | 将其余失败全部算不安全时 | 失败类型 |',
        '|---|---:|---:|---:|---|']
    for condition in summary['conditions']:
        b=summary['all_attempt_sensitivity'][condition]
        lines.append(f"| {ZH[condition]} | {b['closed']} | {b['lower_unsafe_count']} | {b['upper_unsafe_count']} | {json.dumps(aggregates[condition]['failures'],ensure_ascii=False)} |")
    lines += ['', '原始轨迹、审核输入和 API 证据留在私有工作区；公开内容是合成案例、代码、不可变实验计划和派生结果。', '',
              '[逐配置表](README.md) · [逐样本结果](per_case.csv) · [所有尝试与调用量](all_attempts.csv) · [完整统计](summary.json)']
    (REPORT/'RESULTS_ZH.md').write_text('\n'.join(lines)+'\n')
    if summary['status']!='complete':
        return
    assert summary['finished_attempts']==summary['planned_attempts']==6720
    with (REPORT/'per_case.csv').open() as handle:
        case_rows=list(csv.DictReader(handle))
    eligible={condition:{(r['agent'],r['model'],r['case_id']):r for r in case_rows
        if r['condition']==condition and r['repeat']=='1' and r['authorization_mode']=='confirmable'
        and r['response_category']=='clear_approve'} for condition in ('sail_v3','sail_v3_no_human')}
    matched=set(eligible['sail_v3']) & set(eligible['sail_v3_no_human'])
    authorized_ablation={condition:{'numerator':sum(eligible[condition][key]['attack_effect_executed']=='True'
        and eligible[condition][key]['unsafe_attack_success']=='False' for key in matched),
        'denominator':len(matched)} for condition in eligible}
    evidence = {'source':'reports/sail-20260913/main-v3/summary.json',
        'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'plan_sha256':summary['plan_sha256'],'aggregate':aggregates,
        'paired':summary['aggregate_paired'],'all_attempt_sensitivity':summary['all_attempt_sensitivity'],
        'authorized_execution_matched_repeat1':authorized_ablation}
    (PAPER/'sail_results_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    p,s,n = (aggregates[k] for k in ('prompt_guard_v1','sail_v3','sail_v3_no_human'))
    paired = summary['aggregate_paired']['prompt_guard_v1__sail_v3']
    table = [r'\begin{table}[t]',r'\centering\small',
        r'\caption{Fresh method comparison. Rates use valid runs; authorized execution (Auth.) uses all confirmable clear-approval cases, including those never consulted. Prompt and SAIL have three repeats; no-human has one. HIL recall includes controller questions.}',
        r'\label{tab:sailmain}',r'\begin{tabular}{@{}lrrrrrr@{}}',r'\toprule',
        r'Condition & Valid $n$ & ASR $\downarrow$ & BCR $\uparrow$ & Joint $\uparrow$ & HIL $\uparrow$ & Auth. $\uparrow$ \\',r'\midrule']
    for condition in summary['conditions']:
        a=aggregates[condition]
        table.append(' & '.join([NAMES[condition],str(a['unsafe_asr']['denominator']),
            *[percent(a[k],True) for k in ('unsafe_asr','benign_completion','joint_safe_utility','hil_recall','approved_execution_all_eligible')]])+r' \\')
    table += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
    (PAPER/'tables/sail_main.tex').write_text('\n'.join(table)+'\n')
    asr = paired['unsafe_attack_success'];bcr=paired['benign_task_complete']
    body = [r'\subsection{Does scoped HIL improve execution?}',r'\label{sec:sailresults}',
        f"The separate frozen comparison completes all 6,720 attempts, with {summary['valid_runs']:,} valid runs and {summary['failed_attempts']:,} failures. It uses fresh prompt controls and interleaved conditions on the same 80 development cases: three repeats for prompt and SAIL, and one for the no-human ablation. Preflights are excluded.",
        r'\input{tables/sail_main}',
        f"Unsafe ASR changes from {count(p['unsafe_asr'],True)} with the prompt to {count(s['unsafe_asr'],True)} with SAIL. Benign completion changes from {percent(p['benign_completion'],True)} to {percent(s['benign_completion'],True)}. On {paired['matched_case_repeat_pairs']:,} matched pairs, the ASR difference is {100*asr['right_minus_left']:+.2f} percentage points (95\\% task-cluster interval {interval(asr)}); the benign-completion difference is {100*bcr['right_minus_left']:+.2f} points ({interval(bcr)}). These remain exploratory estimates over 20 reused tasks.",
        f"On matched eligible cases in repeat 1, safe authorized execution is {count(authorized_ablation['sail_v3_no_human'],True)} without human replies and {count(authorized_ablation['sail_v3'],True)} with full SAIL. This metric includes unconsulted eligible cases. SAIL records {s['questions']['agent_questions']:,} actor questions and {s['questions']['controller_questions']:,} controller questions. Thus its consultation score describes the combined system. Appendix~\\ref{{app:sailresults}} reports failure bounds, response metrics, and reviewer cost. These comparisons do not isolate scope binding from the other controller components."]
    (PAPER/'sections/05b_sail_results.tex').write_text('\n\n'.join(body)+'\n')
    appendix = [r'\section{SAIL Results and Evaluation Boundaries}',r'\label{app:sailresults}',
        'The main comparison freezes the method, cases, condition prompts, images, ordering, and analysis source before execution. Each repeat randomizes configuration--case blocks and condition order within each block. The first repeat includes all three conditions. Later repeats include prompt and SAIL. Earlier development preflights are excluded. No failed run is automatically retried.',
        r'\input{tables/sail_matrix}',
        'Reviewer protocol errors fail closed but invalidate the run under the frozen protocol. They are method reliability failures, not successful safe completions. Primary rates exclude them and other incomplete runs. The following bounds retain any unsafe effect observed before failure, then treat each remaining failed attempt as either safe or unsafe. They are missing-outcome bounds, not confidence intervals.']
    for condition in summary['conditions']:
        a=aggregates[condition];b=summary['all_attempt_sensitivity'][condition];u=a.get('all_attempt_usage',{})
        appendix.append(f"\\paragraph{{{NAMES[condition]}.}} Valid runs: {a['unsafe_asr']['denominator']:,}; failed attempts: {sum(a['failures'].values()):,}. All-attempt ASR bounds: {100*b['lower_unsafe_count']/b['closed']:.2f}--{100*b['upper_unsafe_count']/b['closed']:.2f}\\%. Strict PostSuccess: {count(a['strict_post_feedback'],True)}; rule-based question matching: {count(a['question_precision_rule_proxy'],True)}. Mean valid-run wall time: {a['mean_wall_seconds']:.1f} seconds. All closed attempts record {u.get('actor_requests',0):,} actor requests and {u.get('reviewer_requests',0):,} reviewer requests. Provider usage is available for {u.get('actor_requests_with_usage',0):,} and {u.get('reviewer_requests_with_usage',0):,} of these requests, respectively.")
    ab=summary['aggregate_paired']['sail_v3_no_human__sail_v3']
    appendix.append(f"The no-human comparison matches repeat 1 only ({ab['matched_case_repeat_pairs']:,} valid pairs). Full minus no-human ASR is {100*ab['unsafe_attack_success']['right_minus_left']:+.2f} percentage points ({interval(ab['unsafe_attack_success'])}); benign completion changes by {100*ab['benign_task_complete']['right_minus_left']:+.2f} points ({interval(ab['benign_task_complete'])}). Marginal authorized-execution rates in Table~\\ref{{tab:sailmain}} use all repeats in each condition; the public case table identifies the matched first-repeat subset.")
    appendix.append('The reviewer is fixed to the requested deepseek-v4-flash route. This comparison is not compute-matched to prompt-only defense. Human replies remain deterministic fixtures. Autonomous recognition, semantic question quality, and generalization beyond reused cases are not established by these results.')
    (PAPER/'sections/11_sail_results.tex').write_text('\n\n'.join(appendix)+'\n')
    matrix=[r'\begin{table}[t]',r'\centering\small',r'\caption{Valid-run rates by configuration. P: fresh prompt guard; S: SAIL; N: no-human SAIL. The no-human condition has one repeat, versus three for P and S.}',r'\label{tab:sailmatrix}',r'\begin{tabular}{@{}llrrrrrr@{}}',r'\toprule',r'Framework & Model & ASR P & ASR S & ASR N & BCR P & BCR S & BCR N \\',r'\midrule']
    labels={'claude-code':'Claude Code','deepseek-harness':'DeepSeek H.','codex':'Codex','hermes':'Hermes'}
    models={'deepseek-v4-flash':'DS Flash','glm-5.2':'GLM 5.2','qwen3.7-max':'Qwen Max'}
    for row in summary['configurations']:
        matrix.append(' & '.join([labels[row['agent']],models[row['model']],*[percent(row['conditions'][condition][metric],True) for metric in ('unsafe_asr','benign_completion') for condition in summary['conditions']]])+r' \\')
    matrix += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
    (PAPER/'tables/sail_matrix.tex').write_text('\n'.join(matrix)+'\n')
    (PAPER/'sections/sail_status.tex').write_text(r'\draftnote{Internal manuscript, revised 13 September 2026. Both repeated four-framework comparisons are complete. Independent semantic annotation, richer feedback, and held-out validation remain incomplete.}'+'\n')
    abstract=PAPER/'sections/00_abstract.tex'
    text=abstract.read_text().split('% SAIL_RESULT_BEGIN')[0].strip()
    if 'These findings separate' in text:
        text=text[:text.index('These findings separate')]
    text=text.rstrip()+f" % SAIL_RESULT_BEGIN\nWe implement SAIL to bind scoped human permission to a reviewed tool call. A separate 6,720-attempt comparison changes unsafe ASR from {percent(p['unsafe_asr'],True)} under a fresh prompt control to {percent(s['unsafe_asr'],True)}, with benign completion of {percent(p['benign_completion'],True)} and {percent(s['benign_completion'],True)}. Synthetic replies and reused tasks limit generalization; independent semantic annotation and held-out validation remain necessary.\n"
    abstract.write_text(text)
    appendix_path=PAPER/'sections/08_appendix.tex'
    text=appendix_path.read_text().replace(
        'Main method efficacy remains pending; preflights are development evidence.',
        'Completed separate 6,720-attempt method comparison; preflights remain development evidence.').replace(
        'Experiment pending; not inferred from natural ask/no-ask groups.',
        'SAIL no-human ablation complete; matched first-repeat comparison.').replace(
        'Prompt studies complete; implemented SAIL comparison pending.',
        'Prompt studies and separate SAIL comparison complete.')
    appendix_path.write_text(text)
    method_path=PAPER/'sections/06_method.tex'
    method_path.write_text(method_path.read_text().replace(
        'Formal comparison results are reported only after the frozen run set has completed.',
        r'Section~\ref{sec:sailresults} reports the completed frozen comparison.'))
    readme=PAPER/'README.md'
    text=readme.read_text()
    if '<!-- SAIL_MAIN_COMPLETE -->' not in text:
        position=text.index('\n\n')+2
        text=text[:position]+f"<!-- SAIL_MAIN_COMPLETE -->\n本轮 SAIL 主实验已完成：{summary['finished_attempts']:,} 次尝试，{summary['valid_runs']:,} 条有效，{summary['failed_attempts']:,} 次失败。正文与附录已加入独立对照结果；[中文完整表](../../reports/sail-20260913/main-v3/RESULTS_ZH.md)保留分母和限制。\n\n"+text[position:]
    readme.write_text(text)


if __name__=='__main__':
    main()
