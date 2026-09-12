"""Render only observed API counts into the manuscript; no model calls."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LABELS={'codex':'Codex','claude-code':'Claude Code','deepseek-harness':'DSH',
        'deepseek-v4-flash':'DeepSeek V4 Flash','glm-5.2':'GLM 5.2','qwen3.7-max':'Qwen 3.7 Max'}


def fmt(pair):
    n,d=pair['numerator'],pair['denominator']
    return f'{n}/{d}' if d else '--'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--summary',type=Path,default=ROOT/'reports/api-multimodel-20260912/main/summary.json');args=parser.parse_args()
    path=ROOT/'paper/iclr2027/tables/api_results.tex'
    if not args.summary.exists():
        path.write_text('\\paragraph{Execution status.} The main matrix is running. No completed main comparison is reported in this snapshot.\n');return
    summary=json.loads(args.summary.read_text())
    complete=summary['status']=='complete'
    status='Completed matrix' if complete else 'Provisional, incomplete matrix'
    text=[r'\paragraph{Execution status.} '+status+f": {summary['finished_attempts']} of {summary['planned_attempts']} attempts have finished. There are {summary['valid_runs']} valid runs, {summary['failed_attempts']} failed attempts, and {summary['pending_attempts']} pending attempts. "+
          ('The tables report the completed run set.' if complete else 'The partial tables do not support a final defense comparison.')]
    for name,keys,headers in [
        ('safety',['unsafe_asr','benign_completion'],['Unsafe ASR','Benign completion']),
        ('interaction',['hil_recall','question_precision_rule_proxy','strict_post_feedback'],['HIL recall','Question proxy','Strict after reply'])]:
        text += [r'\begin{table}[ht]',r'\centering',r'\scriptsize',r'\setlength{\tabcolsep}{4pt}',
                 r'\caption{'+status+'. Each cell lists neutral / prompt-guard counts as two fractions. '+
                 ('Failed attempts are excluded from valid-run denominators.' if name=='safety' else 'Question accuracy is a rule proxy. Post-feedback groups differ between conditions; semantic recognition remains unannotated.')+'}',
                 r'\label{tab:api_'+name+'}',r'\begin{tabular}{@{}l'+'r'*len(keys)+r'@{}}',r'\toprule',
                 'Configuration & '+' & '.join(headers)+r' \\',r'\midrule']
        for config in summary['configurations']:
            label=LABELS[config['agent']]+' / '+LABELS[config['model']]
            left=config['conditions']['neutral'];right=config['conditions']['prompt_guard_v1']
            text.append(label+' & '+' & '.join(fmt(left[k])+' ; '+fmt(right[k]) for k in keys)+r' \\')
        text += [r'\bottomrule',r'\end{tabular}',r'\end{table}']
    path.write_text('\n'.join(text)+'\n')
    (ROOT/'paper/iclr2027/api_results_evidence.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'status':summary['status'],'valid_runs':summary['valid_runs']}))


if __name__=='__main__':main()
