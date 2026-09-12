"""Harmless native Responses/Messages protocol preflight, run in the relay only."""
import concurrent.futures
import argparse
import json
from pathlib import Path
import time
import urllib.request
import urllib.error


def probe(model, protocol, profile):
    key = profile['api_key']
    prompt = 'Call echo once with value HIL_PROBE_731. After the tool replies, output only the receipt.'
    schema = {'type': 'object', 'properties': {'value': {'type': 'string'}}, 'required': ['value']}
    if protocol == 'responses':
        payload = {'model': model, 'input': [{'role': 'user', 'content': prompt}], 'max_output_tokens': 4096,
                   'store': False, 'tools': [{'type': 'function', 'name': 'echo', 'description': 'Harmless receipt test', 'parameters': schema}]}
    else:
        payload = {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 4096,
                   'tools': [{'name': 'echo', 'description': 'Harmless receipt test', 'input_schema': schema}]}
    result = {'model': model, 'protocol': protocol, 'started_unix': time.time(), 'tool_call_ok': False, 'roundtrip_ok': False, 'requests': []}
    try:
        for turn in range(2):
            req = urllib.request.Request(profile['base_url'].rstrip('/') + '/' + protocol, data=json.dumps(payload).encode(),
                headers={'Authorization': 'Bearer ' + key, 'x-api-key': key, 'anthropic-version': '2023-06-01', 'Content-Type': 'application/json'})
            try:
                response = urllib.request.urlopen(req, timeout=150)
            except urllib.error.HTTPError as e:
                response = e
            raw = response.read().decode().replace(key, '<REDACTED>')
            result['requests'].append({'request': payload.copy(), 'status': response.status, 'response': raw})
            if response.status != 200:
                result['failure'] = 'HTTP ' + str(response.status)
                break
            body = json.loads(raw)
            if turn == 1:
                result['roundtrip_ok'] = 'HIL_OK_947' in json.dumps(body)
                break
            output = body.get('output', []) if protocol == 'responses' else body.get('content', [])
            calls = [o for o in output if o.get('type') in ('function_call', 'tool_use')]
            if len(calls) != 1 or calls[0].get('name') != 'echo':
                result['failure'] = 'Expected one echo tool call'
                break
            call = calls[0]
            arguments = json.loads(call['arguments']) if protocol == 'responses' else call['input']
            result['tool_call_ok'] = arguments.get('value') == 'HIL_PROBE_731'
            if not result['tool_call_ok']:
                break
            if protocol == 'responses':
                payload = dict(payload, input=payload['input'] + output + [{'type': 'function_call_output', 'call_id': call['call_id'], 'output': '{"receipt":"HIL_OK_947"}'}])
            else:
                payload = dict(payload, messages=payload['messages'] + [{'role': 'assistant', 'content': output}, {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': call['id'], 'content': '{"receipt":"HIL_OK_947"}'}]}])
    except Exception as e:
        result['failure'] = type(e).__name__
    result['finished_unix'] = time.time()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--models', nargs='+', default=['deepseek-v4-pro', 'glm-5.1', 'qwen3.6-27b'])
    parser.add_argument('--protocols', nargs='+', default=['responses', 'messages'])
    parser.add_argument('--output', default='/evidence/native_protocol_preflight.json')
    args = parser.parse_args()
    profile = json.loads(Path('/run/secrets/profile.json').read_text())
    models = args.models
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(probe, m, p, profile) for m in models for p in args.protocols]
        results = []
        for f in concurrent.futures.as_completed(futures):
            r = f.result(); results.append(r)
            Path(args.output).write_text(json.dumps(results, indent=2) + '\n')
            print(json.dumps({k: v for k, v in r.items() if k != 'requests'}), flush=True)
