import importlib.util
import json
from pathlib import Path
import subprocess
from unittest.mock import patch


def reporter():
    path = Path(__file__).resolve().parents[1] / 'scripts/report_four_framework_capacity.py'
    spec = importlib.util.spec_from_file_location('capacity_reporting', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unavailable_docker_listing_does_not_block_outcome_reporting():
    module = reporter()
    with patch.object(module.subprocess, 'check_output', side_effect=subprocess.TimeoutExpired('docker', 20)):
        containers, owned, errors = module.resource_sample()
    assert containers == [] and owned is None
    assert errors == ['container_listing:TimeoutExpired']


def test_resource_sampling_excludes_other_users_and_created_containers():
    module = reporter()
    agent = 'main01_' + 'a' * 20
    listing = '\n'.join(json.dumps({'Names': name, 'State': state}) for name, state in [
        (agent, 'running'), ('hermes01_' + 'b' * 20, 'created'), ('unrelated', 'paused')])
    stats = json.dumps({'Name': agent, 'MemUsage': '256MiB / 1.5GiB', 'CPUPerc': '50.00%'})
    with patch.object(module.subprocess, 'check_output', return_value=listing), \
            patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stats, '')) as run:
        containers, owned, errors = module.resource_sample()
    assert run.call_args.args[0][5:] == [agent]
    assert len(owned) == 2
    assert containers == [{'name': agent, 'memory_bytes': 256 * 1024**2, 'cpu_cores': .5}]
    assert errors == []


def test_resource_timeout_keeps_known_container_states():
    module = reporter()
    listing = json.dumps({'Names': 'hermes01_' + 'a' * 20, 'State': 'running'})
    with patch.object(module.subprocess, 'check_output', return_value=listing), \
            patch.object(module.subprocess, 'run', side_effect=subprocess.TimeoutExpired('docker', 30)):
        containers, owned, errors = module.resource_sample()
    assert containers == [] and owned[0]['State'] == 'running'
    assert errors == ['container_stats:TimeoutExpired']
