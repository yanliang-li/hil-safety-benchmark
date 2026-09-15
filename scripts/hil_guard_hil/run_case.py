"""Run native Codex with the dialogue-aware benchmark/controller."""
import importlib.util
import json
import os
from pathlib import Path
import sys

from hil_safety_bench.intervene_evaluate import evaluate_intervene_run
from .conditions import CONDITIONS, DIRECT_CONDITIONS, apply_condition


def write_result(result, path):
    path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n")


def main():
    argv = list(sys.argv)
    agent = argv[argv.index("--agent") + 1]
    position = argv.index("--condition") + 1
    condition = argv[position]
    if condition not in CONDITIONS:
        raise ValueError("Invalid InterveneBench condition")
    os.environ["HIL_GUARD_CONDITION"] = condition
    base_url = argv[argv.index("--base-url") + 1]
    run_id = argv[argv.index("--run-id") + 1]
    os.environ["HIL_GUARD_BASE_URL"] = base_url.replace(
        "/r/" + run_id + "/", "/r/" + run_id + "_guard/"
    )
    os.environ["HIL_GUARD_MODEL"] = "deepseek-v4-flash"
    path = Path("/opt/frozen-runners") / (
        "hermes_run_case.py" if agent == "hermes" else "run_case.py"
    )
    spec = importlib.util.spec_from_file_location("native_runner", path)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    case_data = json.loads(Path("/case/.benchmark/case.json").read_text())
    native.apply_condition = lambda task, _: apply_condition(
        task, condition, case_data
    )
    native.evaluate_run = evaluate_intervene_run
    native.write_result = write_result
    shared_env = {
        key: os.environ[key]
        for key in (
            "HIL_GUARD_CONDITION",
            "HIL_GUARD_BASE_URL",
            "HIL_GUARD_MODEL",
        )
    }
    shared_env["PYTHONPATH"] = (
        "/opt/intervene-src:/opt/hil-method:/opt/hilbench-src/src"
    )
    if agent == "hermes":
        original_config = native.configuration

        def configuration(model, url):
            config = original_config(model, url)
            mcp = config["mcp_servers"]["hil_bench"]
            mcp["args"] = ["-m", "hil_guard_hil.mcp_server"]
            mcp["env"].update(shared_env)
            return config

        native.configuration = configuration
    else:
        original_configure = native.configure

        def configure(args, output, prompt):
            command, env, stdin = original_configure(args, output, prompt)
            env.update(shared_env)
            if args.agent == "codex":
                values = None
                for index, value in enumerate(command):
                    if value.startswith("mcp_servers.hil_bench.args="):
                        command[index] = (
                            'mcp_servers.hil_bench.args=["-m","hil_guard_hil.mcp_server"]'
                        )
                    if value.startswith("mcp_servers.hil_bench.env="):
                        values = dict(
                            shared_env,
                            HIL_BENCH_CASE_DIR="/case",
                            HIL_BENCH_RUN_DIR="/run-output",
                        )
                        command[index] = "mcp_servers.hil_bench.env={" + ",".join(
                            key + "=" + json.dumps(value)
                            for key, value in values.items()
                        ) + "}"
                config_path = output / "framework_config.json"
                config = json.loads(config_path.read_text())
                config["mcp_servers.hil_bench.args"] = [
                    "-m",
                    "hil_guard_hil.mcp_server",
                ]
                config["mcp_servers.hil_bench.env"] = values
                config_path.write_text(json.dumps(config, indent=2) + "\n")
            elif args.agent == "claude-code":
                config_path = output / "mcp_config.json"
                config = json.loads(config_path.read_text())
                mcp = config["mcpServers"]["hil_bench"]
                mcp["args"] = ["-m", "hil_guard_hil.mcp_server"]
                mcp["env"].update(shared_env)
                config_path.write_text(json.dumps(config, indent=2) + "\n")
            else:
                config_path = output / "dsh.patch.yml"
                patches = json.loads(config_path.read_text())
                for patch in patches:
                    for inserted in patch.get("insert", []):
                        if inserted.get("id") == "hil-mcp":
                            inserted["config"]["args"] = [
                                "-m",
                                "hil_guard_hil.mcp_server",
                            ]
                            inserted["config"]["env"].update(shared_env)
                config_path.write_text(json.dumps(patches, indent=2) + "\n")
            return command, env, stdin

        native.configure = configure
    sys.argv[position] = "prompt_guard_v1"
    code = 0
    try:
        native.main()
    except SystemExit as error:
        code = error.code or 0
    finally:
        folder = Path("/run-output")
        path = folder / "run_metadata.json"
        if path.exists():
            meta = json.loads(path.read_text())
            meta.update(
                condition=condition,
                controller_version=condition,
                guard_model=(
                    None if condition in DIRECT_CONDITIONS else "deepseek-v4-flash"
                ),
                guard_invalid=(folder / "guard_invalid.flag").exists(),
                response_runtime="intervenebench_stateful_v1",
            )
            if meta["guard_invalid"]:
                meta["scorable"] = False
                meta["successful_termination"] = False
                if (folder / "result.json").exists():
                    (folder / "result.json").rename(
                        folder / "invalid_partial_result.json"
                    )
                (folder / "failure.json").write_text(
                    json.dumps(meta, indent=2) + "\n"
                )
                code = 2
            path.write_text(json.dumps(meta, indent=2) + "\n")
    raise SystemExit(code)


if __name__ == "__main__":
    main()
