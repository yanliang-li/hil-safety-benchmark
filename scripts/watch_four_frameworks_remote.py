"""Periodically replay the two frozen plans on the experiment server."""
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    last_count = -1
    status = ROOT / 'reports/four-framework-watch.json'
    while True:
        try:
            progress = [json.loads((ROOT / f'reports/{name}-plan-v1_progress.json').read_text()) for name in ['main', 'hermes']]
            count = sum(len(p['results']) for p in progress)
            complete = all(p.get('finished_unix') for p in progress)
            if count != last_count or complete:
                result = subprocess.run(['python3', 'scripts/analyze_four_frameworks.py', '--bootstrap', '10000' if complete else '1000'],
                    cwd=ROOT, env=dict(os.environ, PYTHONPATH=str(ROOT / 'src')),
                    capture_output=True, text=True, timeout=480)
                record = {'checked_unix': time.time(), 'finished_attempts': count,
                          'planned': sum(p['planned'] for p in progress), 'complete': bool(complete),
                          'analysis_returncode': result.returncode, 'stdout': result.stdout[-2000:], 'stderr': result.stderr[-2000:]}
                status.write_text(json.dumps(record, indent=2) + '\n')
                print(json.dumps(record), flush=True)
                if result.returncode == 0:
                    last_count = count
                    if complete:
                        break
        except Exception as error:
            record = {'checked_unix': time.time(), 'error': type(error).__name__ + ': ' + str(error)[:700]}
            status.write_text(json.dumps(record, indent=2) + '\n')
            print(json.dumps(record), flush=True)
        time.sleep(180)


if __name__ == '__main__':
    main()
