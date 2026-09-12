"""Generate periodic and final replay reports for the detached Docker controller."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
progress=ROOT/'reports/main-plan-v1_progress.json'
status=ROOT/'reports/main-v1-watch.json'
last_count=-1
while True:
    try:
        p=json.loads(progress.read_text())
        count=len(p['results']); finished=bool(p.get('finished_unix'))
        if count!=last_count or finished:
            cmd=['python3','scripts/api_experiment/analyze.py','--plan','experiments/api-multimodel-20260912/main-plan-v1.json',
                 '--output','reports/api-multimodel-20260912/main','--bootstrap','10000' if finished else '1000']
            env=dict(os.environ,PYTHONPATH=str(ROOT/'src'))
            r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=240)
            record={'checked_unix':time.time(),'completed_attempts':count,'planned':p['planned'],'controller_finished':finished,
                    'analysis_returncode':r.returncode,'analysis_stdout':r.stdout[-2000:],'analysis_stderr':r.stderr[-2000:]}
            status.write_text(json.dumps(record,indent=2)+'\n')
            print(json.dumps(record),flush=True)
            if r.returncode==0:last_count=count
            if finished and r.returncode==0:break
        control=json.loads((ROOT/'reports/main-v1-controller.json').read_text())
        try:os.kill(control['pid'],0)
        except ProcessLookupError:
            if not finished:
                status.write_text(json.dumps({'controller_stopped_incomplete':True,'checked_unix':time.time(),'finished_attempts':count})+'\n')
                break
    except Exception as e:
        status.write_text(json.dumps({'error':type(e).__name__,'checked_unix':time.time()})+'\n')
    time.sleep(180)
