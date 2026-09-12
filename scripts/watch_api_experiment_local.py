"""Fetch immutable completed runs, replay scores locally, and publish audited aggregates.

Connection settings live only in recovery/api_experiment_connection.json.
This controller never reads or copies an authentication token.
"""
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tarfile
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'recovery/api_experiment_connection.json').read_text())
SSH=['ssh','-S',CONFIG['control_path'],'-o','BatchMode=yes','-o','ConnectTimeout=10',CONFIG['ssh_target'],'python3 -']
STATE=ROOT/'recovery/api-multimodel-20260912/local-watch.json'
PLAN=ROOT/'experiments/api-multimodel-20260912/main-plan-v1.json'
PUBLIC=Path(CONFIG['publication_root'])
PYTHON=str(ROOT/'.venv/bin/python')


def run(args,**kwargs):
    return subprocess.run(args,text=True,capture_output=True,check=True,**kwargs)


def remote(code):
    return json.loads(run(SSH,input=code,timeout=240).stdout)


def extract_checked(archive):
    with tarfile.open(archive) as tar:
        for m in tar.getmembers():
            p=Path(m.name)
            if p.is_absolute() or '..' in p.parts or m.issym() or m.islnk():raise ValueError('Unsafe export member')
            if not (m.name.startswith('runs/main-v1/') or m.name.startswith('gateway_evidence/main01_')):raise ValueError('Unexpected export prefix')
        tar.extractall(ROOT,filter='data')


def copy_public():
    for p in (ROOT/'reports/api-multimodel-20260912/main').glob('*'):
        if p.suffix in ('.json','.csv','.md'):
            q=PUBLIC/'reports/api-multimodel-20260912/main'/p.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    for rel in ['paper/iclr2027/main.pdf','paper/iclr2027/tables/api_results.tex','paper/iclr2027/api_results_evidence.json','paper/iclr2027/build_validation_api.json']:
        p=ROOT/rel
        if p.exists():
            q=PUBLIC/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)


def build_paper():
    run([PYTHON,'scripts/build_api_paper_assets.py'],cwd=ROOT,timeout=30)
    p=run([str(ROOT/'recovery/tools/tectonic'),'-X','compile','--keep-logs','--keep-intermediates','paper/iclr2027/main.tex'],cwd=ROOT,timeout=120)
    log=(ROOT/'paper/iclr2027/main.log').read_text()
    if 'Overfull ' in log or re.search(r'(Citation|Reference).*undefined',log):raise ValueError('Paper build requires review')
    pages=int(re.search(r'^Pages:\s+(\d+)',run(['pdfinfo','paper/iclr2027/main.pdf'],cwd=ROOT,timeout=15).stdout,re.M)[1])
    aux=(ROOT/'paper/iclr2027/main.aux').read_text()
    match=re.search(r'newlabel\{sec:conclusion\}\{\{[^}]*\}\{(\d+)\}',aux)
    report={'built_unix':time.time(),'pdf_pages':pages,'main_text_conclusion_page':int(match[1]),'overfull_boxes':0,
            'undefined_references':0,'pdf_sha256':hashlib.sha256((ROOT/'paper/iclr2027/main.pdf').read_bytes()).hexdigest(),
            'status':'API appendix refreshed from observed counts; original pilot claims remain separate.'}
    (ROOT/'paper/iclr2027/build_validation_api.json').write_text(json.dumps(report,indent=2)+'\n')
    paper=ROOT/'paper/iclr2027'
    paths=[paper/n for n in ['main.tex','references.bib','iclr2027_conference.sty','iclr2027_conference.bst','natbib.sty','fancyhdr.sty','SOURCE_README.md']]
    for folder in ['sections','tables','figures']:
        paths += [p for p in (paper/folder).glob('*') if p.suffix in ['.tex','.pdf','.svg']]
    with zipfile.ZipFile(paper/'iclr2027-draft-source.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in paths:z.write(p,str(p.relative_to(paper)))


def publish(count,complete):
    env=dict(os.environ,GH_CONFIG_DIR=CONFIG['gh_config_dir']);env.pop('GH_TOKEN',None);env.pop('GITHUB_TOKEN',None)
    account=run([CONFIG['gh_executable'],'api','user','--jq','.login'],env=env,timeout=30).stdout.strip()
    if account!=CONFIG['github_owner']:raise ValueError('Unexpected GitHub account')
    spec=importlib.util.spec_from_file_location('public_audit',ROOT/'scripts/prepare_public_release.py')
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit);audit.audit(PUBLIC)
    run(['git','add','--','reports/api-multimodel-20260912/main','paper/iclr2027'],cwd=PUBLIC,timeout=30)
    changed=subprocess.run(['git','diff','--cached','--quiet'],cwd=PUBLIC).returncode
    if changed:
        run(['git','commit','--quiet','-m',f'{"Complete" if complete else "Update provisional"} API experiment: {count} finished attempts'],cwd=PUBLIC,timeout=30)
    # Retry a previously committed update even if its first push failed.
    run(['git','push','origin','main'],cwd=PUBLIC,env=env,timeout=120)
    return run(['git','rev-parse','HEAD'],cwd=PUBLIC,timeout=10).stdout.strip()


def main():
    state=json.loads(STATE.read_text()) if STATE.exists() else {'fetched_ids':[],'last_published_count':-1}
    while True:
        try:
            prefix='from pathlib import Path\nimport json,tarfile\nroot=Path('+repr(CONFIG['remote_root'])+')\n'
            progress=remote(prefix+"p=json.loads((root/'reports/main-plan-v1_progress.json').read_text()); print(json.dumps(p))\n")
            complete=bool(progress.get('finished_unix'));finished=[r['run_id'] for r in progress['results']]
            unseen=sorted(set(finished)-set(state['fetched_ids']))
            if complete and not state.get('final_refetch_done'):unseen=sorted(finished)
            if unseen:
                assert all(re.fullmatch(r'main01_[a-f0-9]{20}',r) for r in unseen)
                code=prefix+'ids='+repr(unseen)+"\narchive=root/'reports/closed-runs-export.tar.gz'\nwith tarfile.open(archive,'w:gz') as t:\n for rid in ids:\n  for rel in ['runs/main-v1/'+rid,'gateway_evidence/'+rid]:\n   p=root/rel\n   if p.exists():t.add(p,arcname=rel)\nprint(json.dumps({'archive':str(archive)}))\n"
                archive=remote(code)['archive']
                local=ROOT/'recovery/api-multimodel-20260912/closed-runs-export.tar.gz'
                run(['scp','-o','ControlPath='+CONFIG['control_path'],'-o','BatchMode=yes',CONFIG['ssh_target']+':'+archive,str(local)],timeout=240)
                extract_checked(local)
                state['fetched_ids']=sorted(set(state['fetched_ids'])|set(unseen))
                if complete:state['final_refetch_done']=True
            count=len(finished)
            if count > state.get('last_processed_count', -1) or (complete and not state.get('final_processed')):
                env=dict(os.environ,PYTHONPATH=str(ROOT/'src'))
                run([PYTHON,'scripts/api_experiment/analyze.py','--plan',str(PLAN),'--output','reports/api-multimodel-20260912/main',
                    '--bootstrap','10000' if complete else '1000'],cwd=ROOT,env=env,timeout=240)
                run([PYTHON,'scripts/audit_api_attempts.py'],cwd=ROOT,env=env,timeout=240)
                build_paper();copy_public()
                if state['last_published_count']<0 or count-state['last_published_count']>=100 or complete:
                    state['published_commit']=publish(count,complete);state['last_published_count']=count
                state['last_processed_count']=count
                if complete:state['final_processed']=True
            state.update(checked_unix=time.time(),finished_attempts=len(finished),planned=progress['planned'],remote_complete=complete,last_error=None)
            STATE.write_text(json.dumps(state,indent=2)+'\n')
            print(json.dumps({k:v for k,v in state.items() if k!='fetched_ids'}),flush=True)
            if complete:break
        except Exception as e:
            state.update(checked_unix=time.time(),last_error=type(e).__name__+': '+str(e)[:500])
            STATE.write_text(json.dumps(state,indent=2)+'\n');print(json.dumps({'error':state['last_error']}),flush=True)
        time.sleep(180)


if __name__=='__main__':main()
