"""Execute the official Hermes CLI against the frozen benchmark MCP server."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time

from hil_safety_bench.conditions import apply_condition
from hil_safety_bench.evaluate import evaluate_run, write_result

TOOLS = ['list_documents', 'read_document', 'ask_human', 'write_output',
         'execute_command', 'upload_file', 'delete_path', 'send_message',
         'consume_resource', 'finish']


def configuration(model, base_url):
    return {
        'model': {'default': model, 'provider': 'evaluation', 'context_length': 65536},
        'providers': {'evaluation': {'api': base_url, 'api_key': 'benchmark-relay',
            'transport': 'chat_completions', 'discover_models': False,
            'context_length': 65536, 'default_model': model,
            'extra_body': {'max_tokens': 4096}}},
        'fallback_providers': [],
        'platform_toolsets': {'cli': ['hil_bench']},
        'mcp_servers': {'hil_bench': {
            'command': '/opt/hilbench-venv/bin/python',
            'args': ['-m', 'hil_safety_bench.mcp_server'],
            'env': {'HIL_BENCH_CASE_DIR': '/case', 'HIL_BENCH_RUN_DIR': '/run-output',
                    'PYTHONPATH': '/opt/hilbench-src/src'},
            'tools': {'include': TOOLS, 'resources': False, 'prompts': False}}},
        'memory': {'memory_enabled': False, 'user_profile_enabled': False, 'nudge_interval': 0},
        'skills': {'creation_nudge_interval': 0},
        'compression': {'enabled': False},
        'agent': {'api_max_retries': 1, 'verify_on_stop': False, 'environment_probe': False},
        'updates': {'check': False},
        'nous': {'guest': False},
        'telemetry': {'shared_metrics': {'enabled': False, 'send': False}},
    }


def terminal_success(returncode, timed_out, stdout, usage):
    return (returncode == 0 and not timed_out and bool(stdout.strip())
            and usage.get('completed') is True and not usage.get('failed'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', choices=['hermes'], required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--condition', choices=['neutral', 'prompt_guard_v1'], required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--repeat', type=int, default=0)
    parser.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args()
    output, case = Path('/run-output'), Path('/case')
    if (output / 'run_metadata.json').exists():
        raise FileExistsError('Do not overwrite an attempt')
    task = (case / 'TASK.md').read_text()
    prompt = apply_condition(task, args.condition)
    (output / 'effective_prompt.txt').write_text(prompt)
    home = Path('/tmp/hermes')
    home.mkdir(mode=0o700, exist_ok=True)
    config = configuration(args.model, args.base_url)
    config_file = home / 'config.yaml'
    config_file.write_text(json.dumps(config, indent=2) + '\n')
    config_file.chmod(0o600)
    (output / 'framework_config.json').write_text(json.dumps(config, indent=2) + '\n')
    usage_path = output / 'hermes_usage.json'
    command = ['/opt/hermes-venv/bin/hermes', '--ignore-rules', '--model', args.model,
               '--provider', 'evaluation', '--toolsets', 'hil_bench',
               '--usage-file', str(usage_path), '--oneshot', prompt]
    env = dict(os.environ, HERMES_HOME=str(home), HERMES_GUEST_ONBOARDING='0',
               HERMES_IGNORE_RULES='1', HERMES_VERIFY_ON_STOP='0', NO_COLOR='1')
    meta = {'agent': 'hermes', 'requested_model': args.model, 'condition': args.condition,
            'repeat': args.repeat, 'run_id': args.run_id, 'started_unix': time.time(),
            'effective_prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
            'task_prompt_sha256': hashlib.sha256(task.encode()).hexdigest(),
            'real_credential_in_agent_container': False, 'timeout_seconds': args.timeout,
            'timed_out': False, 'successful_termination': False,
            'command': [v if v != prompt else '<TASK_PROMPT>' for v in command]}
    stdout, stderr = '', ''
    try:
        process = subprocess.Popen(command, cwd='/case/workspace', env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            meta['timed_out'] = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
        meta['returncode'] = process.returncode
        usage = json.loads(usage_path.read_text()) if usage_path.exists() else {}
        meta['successful_termination'] = terminal_success(process.returncode, meta['timed_out'], stdout, usage)
        meta['hermes_completed'] = usage.get('completed')
        meta['hermes_failed'] = usage.get('failed')
    except Exception as error:
        meta['runner_error'] = type(error).__name__ + ': ' + str(error)
    (output / 'agent_stdout.log').write_text(stdout)
    (output / 'agent_stderr.log').write_text(stderr)
    state_dir = output / 'hermes_state'
    state_dir.mkdir(exist_ok=True)
    for path in home.iterdir():
        if path.name in ('sessions', 'logs') and path.is_dir():
            shutil.copytree(path, state_dir / path.name, dirs_exist_ok=True)
        elif path.is_file() and (path.name == 'config.yaml' or '.db' in path.name or '.sqlite' in path.name):
            shutil.copy2(path, state_dir / path.name)
    meta['finished_unix'] = time.time()
    for name in ('memory.peak', 'memory.max', 'cpu.stat'):
        path = Path('/sys/fs/cgroup') / name
        if path.exists():
            meta['cgroup_' + name.replace('.', '_')] = path.read_text().strip()
    events = output / 'events.jsonl'
    meta['benchmark_event_count'] = len(events.read_text().splitlines()) if events.exists() else 0
    meta['scorable'] = meta['successful_termination']
    if meta['scorable'] and not events.exists():
        events.touch()
    (output / 'run_metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
    if meta['scorable']:
        result = evaluate_run(case, output)
        write_result(result, output / 'result.json')
        print(json.dumps({'run_id': args.run_id, 'completed': True,
                          'unsafe': result.unsafe_attack_success, 'benign': result.benign_task_complete}))
    else:
        (output / 'failure.json').write_text(json.dumps(meta, indent=2) + '\n')
        print(json.dumps({'run_id': args.run_id, 'completed': False,
                          'returncode': meta.get('returncode'), 'error': meta.get('runner_error')}))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
