"""Transport and attempt identity checks; these tests make no external API calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
import hashlib
import pytest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]


def test_paired_cluster_analysis_preserves_repeats_and_excludes_unmatched():
    spec=importlib.util.spec_from_file_location('api_analysis',ROOT/'scripts/api_experiment/analyze.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    left={};right={}
    for task in range(5):
        for repeat in range(3):
            key=(f'case{task}',repeat)
            left[key]={'task_id':str(task),'unsafe_attack_success':True,'benign_task_complete':True,'joint_safe_utility':False}
            right[key]={'task_id':str(task),'unsafe_attack_success':False,'benign_task_complete':True,'joint_safe_utility':True}
    left[('unmatched',1)]=dict(left[('case0',0)],task_id='unmatched')
    result=module.paired_stats(left,right,draws=100)
    assert result['matched_case_repeat_pairs']==15
    assert result['task_clusters']==5
    assert result['unsafe_attack_success']['task_cluster_bootstrap_95_interval']==[-1,-1]
    assert result['benign_task_complete']['guard_minus_neutral']==0


@pytest.mark.parametrize('capacity', [None, 40, 64, 96, 128])
def test_relay_native_passthrough_and_attempt_limits(tmp_path, capacity):
    requests = []
    body = b'data: {"type":"response.completed","response":{"model":"test-model","usage":{"output_tokens":4}}}\n\n'
    class Upstream(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def do_POST(self):
            payload = self.rfile.read(int(self.headers['Content-Length']))
            requests.append((self.path, payload, self.headers['Authorization']))
            self.send_response(200); self.send_header('Content-Type', 'text/event-stream'); self.end_headers(); self.wfile.write(body)
    upstream = ThreadingHTTPServer(('127.0.0.1', 0), Upstream)
    thread = threading.Thread(target=upstream.serve_forever, daemon=True); thread.start()
    profile = tmp_path/'profile.json'; registry=tmp_path/'registry'; evidence=tmp_path/'evidence'
    registry.mkdir(); evidence.mkdir()
    profile.write_text(json.dumps({'base_url':f'http://127.0.0.1:{upstream.server_port}/v1','api_key':'UNIT_TEST_PRIVATE_CREDENTIAL'}))
    (registry/'allowed.json').write_text(json.dumps({'model':'test-model','max_requests':1}))
    import socket
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
    gateway=ROOT/'scripts/api_experiment/gateway.py'
    command=[sys.executable,str(gateway)]
    if capacity:
        command=[sys.executable,str(ROOT/'scripts/gateway_capacity.py'),'--source',str(gateway),
                 '--source-sha256',hashlib.sha256(gateway.read_bytes()).hexdigest(),'--max-inflight',str(capacity)]
        if capacity > 64:
            control = tmp_path/'capacity.json'
            control.write_text(json.dumps({'gateway_max_inflight':capacity}))
            command=[sys.executable,str(ROOT/'scripts/gateway_capacity_ramp.py'),'--source',str(gateway),
                     '--source-sha256',hashlib.sha256(gateway.read_bytes()).hexdigest(),'--max-inflight','128',
                     '--capacity-control',str(control)]
    process=subprocess.Popen(command+['--profile',str(profile),
                              '--registry',str(registry),'--evidence',str(evidence),'--port',str(port)])
    base=f'http://127.0.0.1:{port}'
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(base+'/health',timeout=.1).close();break
            except OSError: time.sleep(.02)
        payload=json.dumps({'model':'test-model','input':'hello','stream':True}).encode()
        def post(route,data=payload):
            req=urllib.request.Request(base+route,data=data,headers={'Content-Type':'application/json','Authorization':'Bearer placeholder'})
            try:
                with urllib.request.urlopen(req,timeout=2) as r:return r.status,r.read()
            except urllib.error.HTTPError as e:return e.code,e.read()
        assert post('/r/absent/v1/responses')[0]==403
        assert post('/r/allowed/v1/responses',b'{"model":"wrong"}')[0]==403
        assert post('/r/allowed/v1/responses')==(200,body)
        assert post('/r/allowed/v1/responses')[0]==429
        assert requests==[('/v1/responses',payload,'Bearer UNIT_TEST_PRIVATE_CREDENTIAL')]
        artifact=evidence/'allowed/request_001.json'
        for _ in range(100):
            result=json.loads(artifact.read_text())
            if result['state']=='complete':break
            time.sleep(.01)
        assert result['returned_models']==['test-model']
        assert result['usage']=={'output_tokens':4}
        assert 'UNIT_TEST_PRIVATE_CREDENTIAL' not in artifact.read_text()
    finally:
        process.terminate(); process.wait(timeout=3); upstream.shutdown()
