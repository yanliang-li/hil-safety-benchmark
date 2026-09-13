"""Native framework runners with an isolated HIL controller extension."""
import importlib.util
import json
import os
from pathlib import Path
import sys

from hil_guard_v4.conditions import apply_condition, CONDITIONS


def main():
    # Keep the original native runner, framework settings, and evaluator intact.
    argv = list(sys.argv)
    agent = argv[argv.index('--agent') + 1]
    position = argv.index('--condition') + 1
    condition = argv[position]
    if condition not in CONDITIONS:
        raise ValueError('Invalid HIL experiment condition')
    os.environ['HIL_GUARD_CONDITION'] = condition
    base_url = argv[argv.index('--base-url') + 1]
    run_id = argv[argv.index('--run-id') + 1]
    os.environ['HIL_GUARD_BASE_URL'] = base_url.replace('/r/' + run_id + '/', '/r/' + run_id + '_guard/')
    os.environ['HIL_GUARD_MODEL'] = 'deepseek-v4-flash'
    path = Path('/opt/frozen-runners') / ('hermes_run_case.py' if agent == 'hermes' else 'run_case.py')
    spec = importlib.util.spec_from_file_location('native_runner', path)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    native.apply_condition = lambda task, _: apply_condition(task, condition)
    shared_env = {k: os.environ[k] for k in ('HIL_GUARD_CONDITION', 'HIL_GUARD_BASE_URL', 'HIL_GUARD_MODEL')}
    shared_env['PYTHONPATH'] = '/opt/hil-method:/opt/hilbench-src/src'
    if agent == 'hermes':
        original_config = native.configuration
        def configuration(model, url):
            config = original_config(model, url)
            mcp = config['mcp_servers']['hil_bench']
            mcp['args'] = ['-m', 'hil_guard_v4.mcp_server']
            mcp['env'].update(shared_env)
            return config
        native.configuration = configuration
    else:
        original_configure = native.configure
        def configure(args, output, prompt):
            command, env, stdin = original_configure(args, output, prompt)
            env.update(shared_env)
            if args.agent == 'codex':
                for i, value in enumerate(command):
                    if value.startswith('mcp_servers.hil_bench.args='):
                        command[i] = 'mcp_servers.hil_bench.args=["-m","hil_guard_v4.mcp_server"]'
                    if value.startswith('mcp_servers.hil_bench.env='):
                        values = dict(shared_env, HIL_BENCH_CASE_DIR='/case', HIL_BENCH_RUN_DIR='/run-output')
                        command[i] = 'mcp_servers.hil_bench.env={' + ','.join(k+'='+json.dumps(v) for k,v in values.items()) + '}'
                path = output / 'framework_config.json'
                config = json.loads(path.read_text())
                config['mcp_servers.hil_bench.args'] = ['-m', 'hil_guard_v4.mcp_server']
                config['mcp_servers.hil_bench.env'] = values
                path.write_text(json.dumps(config, indent=2) + '\n')
            elif args.agent == 'claude-code':
                path = output / 'mcp_config.json'
                config = json.loads(path.read_text())
                mcp = config['mcpServers']['hil_bench']
                mcp['args'] = ['-m', 'hil_guard_v4.mcp_server']
                mcp['env'].update(shared_env)
                path.write_text(json.dumps(config, indent=2) + '\n')
            else:
                path = output / 'dsh.patch.yml'
                patches = json.loads(path.read_text())
                for patch in patches:
                    for inserted in patch.get('insert', []):
                        if inserted.get('id') == 'hil-mcp':
                            inserted['config']['args'] = ['-m', 'hil_guard_v4.mcp_server']
                            inserted['config']['env'].update(shared_env)
                path.write_text(json.dumps(patches, indent=2) + '\n')
            return command, env, stdin
        native.configure = configure
    # The frozen parser accepts the original condition identifier; final public
    # metadata below records the actual condition and prompt hash truthfully.
    sys.argv[position] = 'prompt_guard_v1'
    code = 0
    try:
        native.main()
    except SystemExit as error:
        code = error.code or 0
    finally:
        folder = Path('/run-output')
        path = folder / 'run_metadata.json'
        if path.exists():
            meta = json.loads(path.read_text())
            meta.update(condition=condition, controller_version=condition,
                        guard_model=None if condition == 'prompt_guard_v1' else 'deepseek-v4-flash',
                        guard_invalid=(folder / 'guard_invalid.flag').exists())
            if meta['guard_invalid']:
                meta['scorable'] = False
                meta['successful_termination'] = False
                # Any provisional original score is retained for the all-attempt
                # audit, but cannot enter valid-run primary comparisons.
                if (folder / 'result.json').exists():
                    (folder / 'result.json').rename(folder / 'invalid_partial_result.json')
                (folder / 'failure.json').write_text(json.dumps(meta, indent=2) + '\n')
                code = 2
            path.write_text(json.dumps(meta, indent=2) + '\n')
    raise SystemExit(code)


if __name__ == '__main__':
    main()
