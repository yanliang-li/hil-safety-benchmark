"""Keep frozen supervision/analysis, with an explicit alternative launch path."""
import json
import subprocess
import time

import supervise_sail_v4 as original
from launch_sail_v4_extended import verify_amendment


def extended_command(command):
    if isinstance(command, list) and len(command) > 2 and command[1] == 'scripts/launch_sail_v4_sequential.py':
        command = list(command)
        command[1] = 'scripts/launch_sail_v4_extended.py'
        command[command.index('--concurrency') + 1] = '128'
    return command


class ProcessAdapter:
    STDOUT = subprocess.STDOUT

    @staticmethod
    def run(command, **kwargs):
        return subprocess.run(extended_command(command), **kwargs)


def main():
    verify_amendment()
    path = original.ROOT / 'reports/sail4-promotion.json'
    state = json.loads(path.read_text())
    state.update(state='formal_phases', capacity_extension_started_unix=time.time())
    original.save(path, state)
    original.subprocess = ProcessAdapter
    original.main()
    state.update(state='formal_experiments_complete', finished_unix=time.time())
    original.save(path, state)


if __name__ == '__main__':
    main()
