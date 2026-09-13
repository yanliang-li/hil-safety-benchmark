import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import handoff_sail_v4_orphan_closeout as closeout


def test_only_terminal_failures_can_be_closed_and_evidence_is_unchanged(tmp_path,monkeypatch):
    def save(relative,value):
        path=tmp_path/relative;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(value));return path
    monkeypatch.setattr(closeout.handoff,'ROOT',tmp_path)
    monkeypatch.setattr(closeout.handoff,'owned_pause',lambda:True)
    monkeypatch.setattr(closeout,'is_really_idle',lambda:False)
    monkeypatch.setattr(closeout.handoff,'inspect',lambda _:{'State':{'Pid':123}})
    status=tmp_path/'proc-status';status.write_text('Threads:\t2\n')
    monkeypatch.setattr(closeout,'Path',lambda *args:status if args[0]=='/proc' else Path(*args))
    save('reports/sail4-matched-r2_progress.json',{'active':0})
    save('experiments/sail-v4-20260913/sail4-matched-r2.json',{'jobs':[{'run_id':'one','stage':'main'}]})
    request=save('gateway_evidence/one/request_001.json',{'state':'pending','started_unix':time.time()-900})
    terminal=save('runs/main/one/attempt_status.json',{'completed':False,'finished_unix':time.time()-300})
    before=request.read_bytes(),terminal.read_bytes()
    assert closeout.ready_with_closed_orphans()
    assert before==(request.read_bytes(),terminal.read_bytes())
    receipt=json.loads((tmp_path/'reports/sail4-orphaned-gateway-closeout.json').read_text())
    assert len(receipt['orphaned_requests'])==1 and not receipt['requests_retried']
    terminal.write_text(json.dumps({'completed':True,'finished_unix':time.time()-300}))
    assert not closeout.ready_with_closed_orphans()
    terminal.unlink()
    assert not closeout.ready_with_closed_orphans()
