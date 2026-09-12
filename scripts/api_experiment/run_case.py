"""Drive real Codex, Claude Code, and DeepSeek Harness CLIs; no custom model loop."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
from hil_safety_bench.conditions import apply_condition
from hil_safety_bench.evaluate import evaluate_run, write_result


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def configure(args, output, prompt):
    env = dict(os.environ)
    env.update(NO_COLOR='1', NODE_OPTIONS='--max-old-space-size=768')
    mcp = {'type': 'stdio', 'command': sys.executable, 'args': ['-m', 'hil_safety_bench.mcp_server'],
           'env': {'HIL_BENCH_CASE_DIR': '/case', 'HIL_BENCH_RUN_DIR': '/run-output'}}
    if args.agent == 'codex':
        values = {
            'approval_policy': 'never', 'model_provider': 'evaluation',
            'model_providers.evaluation.name': 'Evaluation relay',
            'model_providers.evaluation.base_url': args.base_url,
            'model_providers.evaluation.env_key': 'HIL_RELAY_PLACEHOLDER',
            'model_providers.evaluation.wire_api': 'responses',
            'model_providers.evaluation.request_max_retries': 0,
            'model_providers.evaluation.stream_max_retries': 0,
            'model_providers.evaluation.supports_websockets': False,
            'model_reasoning_effort': 'medium', 'model_supports_reasoning_summaries': False,
            'model_context_window': 32768, 'web_search': 'disabled',
            'features.shell_tool': False, 'features.unified_exec': False,
            'features.multi_agent': False, 'features.shell_snapshot': False,
            'mcp_servers.hil_bench.command': sys.executable,
            'mcp_servers.hil_bench.args': ['-m', 'hil_safety_bench.mcp_server'],
            'mcp_servers.hil_bench.default_tools_approval_mode': 'approve',
        }
        command = ['codex', 'exec', '-m', args.model, '-s', 'read-only', '-C', '/case/workspace',
                   '--skip-git-repo-check', '--ephemeral', '--ignore-user-config', '--ignore-rules', '--json']
        for key, value in values.items():
            command += ['-c', key + '=' + json.dumps(value)]
        command += ['-c', 'mcp_servers.hil_bench.env={HIL_BENCH_CASE_DIR="/case",HIL_BENCH_RUN_DIR="/run-output"}', '-']
        env['HIL_RELAY_PLACEHOLDER'] = 'benchmark-relay'
        save(output/'framework_config.json', values)
        return command, env, prompt
    if args.agent == 'claude-code':
        save(output/'mcp_config.json', {'mcpServers': {'hil_bench': mcp}})
        env.update(ANTHROPIC_BASE_URL=args.base_url.removesuffix('/v1'),
                   ANTHROPIC_API_KEY='benchmark-relay', ANTHROPIC_AUTH_TOKEN='benchmark-relay',
                   ANTHROPIC_MODEL=args.model, ANTHROPIC_DEFAULT_HAIKU_MODEL=args.model,
                   ANTHROPIC_DEFAULT_SONNET_MODEL=args.model, ANTHROPIC_DEFAULT_OPUS_MODEL=args.model,
                   CLAUDE_CODE_SUBAGENT_MODEL=args.model, CLAUDE_CONFIG_DIR='/tmp/claude-config',
                   CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1', DISABLE_AUTOUPDATER='1',
                   DISABLE_TELEMETRY='1', DISABLE_ERROR_REPORTING='1', CLAUDE_CODE_DISABLE_AUTO_MEMORY='1',
                   CLAUDE_CODE_MAX_OUTPUT_TOKENS='4096', MAX_THINKING_TOKENS='0', API_TIMEOUT_MS='180000')
        command = ['claude', '-p', '--output-format', 'stream-json', '--verbose', '--model', args.model,
                   '--mcp-config', str(output/'mcp_config.json'), '--strict-mcp-config',
                   '--no-session-persistence', '--tools', '', '--allowedTools', 'mcp__hil_bench__*',
                   '--permission-mode', 'dontAsk', '--max-turns', '32', prompt]
        save(output/'framework_config.json', {'native_tools': [], 'max_turns': 32,
             'max_output_tokens': 4096, 'thinking_tokens': 0, 'base_url': env['ANTHROPIC_BASE_URL']})
        return command, env, None
    env.update(DSH_HOME='/tmp/dsh', DSH_PERMISSION_MODE='danger-full-access',
               DSH_TELEMETRY_DISABLED='1', HIL_RELAY_PLACEHOLDER='benchmark-relay')
    shutil.copytree('/opt/dsh-seed', '/tmp/dsh', symlinks=True)
    default = Path('/opt/dsh-default-config.yml').read_text()
    disabled = [ident for ident, name in re.findall(r'^- id: ([^\n]+)\n  name: [\x27\"]?([^\n\x27\"]+)', default, re.M)
                if '/dsh-tool-' in name or ident in ['session-title-llm', 'compaction-basic', 'command-compact', 'session-telemetry-otel', 'plan-mode']]
    patches = [{'id': ident, 'disabled': True} for ident in disabled]
    patches += [
        {'id': 'agent-default-model', 'config': {'provider': 'evaluation', 'model': args.model}},
        {'id': 'llm-pi-ai', 'config': {'providers': {'evaluation': {
            'api': 'openai-completions', 'baseURL': args.base_url, 'apiKeyEnv': 'HIL_RELAY_PLACEHOLDER',
            'retryPolicy': {'mode': 'normal', 'maxRetries': 0},
            'models': [{'id': args.model, 'contextWindow': 32768, 'maxTokens': 4096}],
        }}}},
        {'insert': [{'id': 'hil-mcp', 'name': '@deepseek-ai/dsh-mcp-client', 'config': {
            'serverName': 'hil_bench', 'transport': 'stdio', 'command': sys.executable,
            'args': ['-m', 'hil_safety_bench.mcp_server'],
            'env': {'HIL_BENCH_CASE_DIR': '/case', 'HIL_BENCH_RUN_DIR': '/run-output'},
            'failOnStartupError': True}}]},
    ]
    save(output/'dsh.patch.yml', patches)
    save(output/'framework_config.json', {'disabled_plugins': disabled, 'patch_file': 'dsh.patch.yml',
         'sampling': 'provider defaults; no requested reasoning override', 'native_tools': []})
    return ['dsh', '--profile', 'headless', '--patch', str(output/'dsh.patch.yml'), prompt], env, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', choices=['codex', 'claude-code', 'deepseek-harness'], required=True)
    parser.add_argument('--model', required=True); parser.add_argument('--base-url', required=True)
    parser.add_argument('--condition', choices=['neutral', 'prompt_guard_v1'], required=True)
    parser.add_argument('--run-id', required=True); parser.add_argument('--repeat', type=int, default=0)
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    output, case = Path('/run-output'), Path('/case')
    if (output/'run_metadata.json').exists(): raise FileExistsError('Do not overwrite an attempt')
    task = (case/'TASK.md').read_text(); prompt = apply_condition(task, args.condition)
    (output/'effective_prompt.txt').write_text(prompt)
    meta = {'agent': args.agent, 'requested_model': args.model, 'condition': args.condition,
            'repeat': args.repeat, 'run_id': args.run_id, 'started_unix': time.time(),
            'effective_prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
            'task_prompt_sha256': hashlib.sha256(task.encode()).hexdigest(),
            'real_credential_in_agent_container': False, 'timeout_seconds': args.timeout,
            'timed_out': False, 'successful_termination': False}
    stdout, stderr = '', ''
    try:
        command, env, stdin = configure(args, output, prompt)
        meta['command'] = [v if v != prompt else '<TASK_PROMPT>' for v in command]
        process = subprocess.Popen(command, cwd='/case/workspace', env=env, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        try:
            stdout, stderr = process.communicate(input=stdin, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            meta['timed_out'] = True; os.killpg(process.pid, signal.SIGTERM)
            try: stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL); stdout, stderr = process.communicate()
        meta['returncode'] = process.returncode
        records = []
        for line in stdout.splitlines():
            try:
                value = json.loads(line)
                if isinstance(value, dict): records.append(value)
            except ValueError: pass
        if args.agent == 'codex':
            terminal = any(r.get('type') == 'turn.completed' for r in records)
            errors = any(r.get('type') in ('turn.failed', 'error') for r in records)
        elif args.agent == 'claude-code':
            terminal = any(r.get('type') == 'result' and r.get('subtype') == 'success' for r in records)
            errors = any(r.get('type') == 'result' and r.get('is_error') for r in records)
        else: terminal, errors = bool(stdout.strip()), False
        meta['successful_termination'] = process.returncode == 0 and not meta['timed_out'] and terminal and not errors
        meta['stream_event_types'] = sorted({r.get('type', 'unknown') for r in records})
    except Exception as e:
        meta['runner_error'] = type(e).__name__ + ': ' + str(e)
    (output/'agent_stdout.log').write_text(stdout); (output/'agent_stderr.log').write_text(stderr)
    if args.agent == 'deepseek-harness' and Path('/tmp/dsh/sessions').exists():
        shutil.copytree('/tmp/dsh/sessions', output/'dsh_sessions', dirs_exist_ok=True)
    meta['finished_unix'] = time.time()
    for name in ('memory.peak', 'memory.max', 'cpu.stat'):
        p = Path('/sys/fs/cgroup')/name
        if p.exists(): meta['cgroup_'+name.replace('.', '_')] = p.read_text().strip()
    events = output/'events.jsonl'
    meta['benchmark_event_count'] = len(events.read_text().splitlines()) if events.exists() else 0
    # A completed refusal or no-tool answer is a real outcome, not an API failure.
    meta['scorable'] = meta['successful_termination']
    if meta['scorable'] and not events.exists(): events.touch()
    save(output/'run_metadata.json', meta)
    if meta['scorable']:
        result = evaluate_run(case, output); write_result(result, output/'result.json')
        print(json.dumps({'run_id': args.run_id, 'completed': True,
                          'unsafe': result.unsafe_attack_success, 'benign': result.benign_task_complete}))
    else:
        save(output/'failure.json', meta)
        print(json.dumps({'run_id': args.run_id, 'completed': False, 'returncode': meta.get('returncode'), 'error': meta.get('runner_error')}))
        raise SystemExit(2)


if __name__ == '__main__': main()
