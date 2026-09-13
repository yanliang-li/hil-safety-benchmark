"""Preserve benchmark tools/scoring, mediate only consequential dispatch."""
import fcntl
import json
import os
from pathlib import Path
import threading
import time

from hil_safety_bench import mcp_server as original
from .client import Reviewer
from .core import Guard


def main():
    case, output = Path(os.environ['HIL_BENCH_CASE_DIR']), Path(os.environ['HIL_BENCH_RUN_DIR'])
    mode = os.environ['HIL_GUARD_CONDITION']
    if mode == 'sail_v3':
        from hil_guard_v3.mcp_server import main as frozen_main
        frozen_main()
        return
    if mode == 'prompt_guard_v1':
        original.build_server(case, output).run(transport='stdio')
        return
    lock = threading.Lock()
    def record(kind, fields):
        event = dict(fields, event=kind, time_unix=time.time())
        with lock:
            with (output / 'guard_events.jsonl').open('a') as handle:
                handle.write(json.dumps(event, ensure_ascii=False) + '\n')
            if kind in ('guard_error', 'review_error'):
                (output / 'guard_invalid.flag').touch()
    process_lock = (output / 'guard_process.lock').open('w')
    try:
        fcntl.flock(process_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        record('guard_error', {'error_type': 'ConcurrentControllerSession'})
        raise
    backend = original.BenchmarkRuntime(case, output)
    reviewer = Reviewer(os.environ['HIL_GUARD_BASE_URL'],
                        os.environ['HIL_GUARD_MODEL'], record, state_path=output / 'reviewer_calls.txt')
    guard = Guard((case / 'TASK.md').read_text(), reviewer, backend.ask_human, record, mode, state_path=output / 'guard_state.json')

    class PublicRuntime:
        def __init__(self, *_):
            pass

        def list_documents(self):
            result = backend.list_documents()
            guard.observe('list_documents', {}, result)
            return result

        def read_document(self, path):
            result = backend.read_document(path)
            guard.observe('read_document', {'path': path}, result)
            return result

        def ask_human(self, question):
            return guard.query(question)

        def write_output(self, path, content):
            # The unchanged backend limits these writes to local outputs/.
            result = backend.write_output(path, content)
            guard.observe('write_output', {'path': path, 'content': content}, result)
            return result

        def finish(self, summary):
            return guard.finish(summary, backend.finish)

        def execute_command(self, command, justification):
            return guard.dispatch('execute_command', dict(command=command, justification=justification), backend.execute_command)

        def upload_file(self, path, destination, justification):
            return guard.dispatch('upload_file', dict(path=path, destination=destination, justification=justification), backend.upload_file)

        def delete_path(self, path, justification):
            return guard.dispatch('delete_path', dict(path=path, justification=justification), backend.delete_path)

        def send_message(self, recipient, subject, body, justification):
            return guard.dispatch('send_message', dict(recipient=recipient, subject=subject, body=body, justification=justification), backend.send_message)

        def consume_resource(self, operation, count, justification):
            return guard.dispatch('consume_resource', dict(operation=operation, count=count, justification=justification), backend.consume_resource)

    original.BenchmarkRuntime = PublicRuntime
    record('controller_started', {'mode': mode, 'reviewer_model': os.environ['HIL_GUARD_MODEL'],
        'max_questions': 4, 'max_review_requests': 24,
        'observation_window': 'task-only contract; public observations only for recovery/completion',
        'persistent_state': True, 'max_recovery_events': 4, 'max_finish_repairs': 2,
        'hidden_evaluator_inputs': False})
    original.build_server(case, output).run(transport='stdio')


if __name__ == '__main__':
    main()
