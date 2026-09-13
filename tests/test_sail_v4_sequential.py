from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import threading

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prepare_sail_v4_matched import matched_plan
from prepare_sail_v4_sequential import ordered_plan
from launch_sail_v4_sequential import MainFirstPool


def test_reordering_adds_no_jobs_and_preserves_main_and_ablation_relative_order():
    parent=json.loads((Path(__file__).resolve().parents[1]/'experiments/sail-20260913/sail-main-v3.json').read_text())
    old,new=matched_plan(parent),ordered_plan(parent)
    assert len(new['jobs'])==6720
    assert {j['run_id']:j for j in old['jobs']}=={j['run_id']:j for j in new['jobs']}
    assert new['jobs'][:5760]==[j for j in old['jobs'] if j['condition']!='sail_v4_no_human']
    assert new['jobs'][5760:]==[j for j in old['jobs'] if j['condition']=='sail_v4_no_human']


def test_ablation_cannot_start_while_any_main_worker_is_running(tmp_path):
    release=threading.Event(); started=threading.Event(); requested=threading.Event(); ablated=threading.Event()
    class Pool(MainFirstPool):
        expected_main=1
        already_closed_main=0
        checkpoint=tmp_path/'main-complete.json'
        check_resources=staticmethod(lambda:True)
    def run(job):
        if job['condition']=='sail_v4_no_human':ablated.set();return
        started.set();assert release.wait(5)
    with Pool(max_workers=2) as pool, ThreadPoolExecutor(max_workers=1) as caller:
        first=pool.submit(run,{'condition':'sail_v4'})
        assert started.wait(1)
        def submit_ablation():
            requested.set()
            return pool.submit(run,{'condition':'sail_v4_no_human'})
        pending=caller.submit(submit_ablation)
        assert requested.wait(1)
        assert not ablated.wait(.1)
        release.set();first.result(timeout=1);pending.result(timeout=1).result(timeout=1)
    assert ablated.is_set() and json.loads(Pool.checkpoint.read_text())['main_attempts']==1
