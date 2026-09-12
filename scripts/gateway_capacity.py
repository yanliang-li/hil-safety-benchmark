"""Change relay capacity without changing the frozen request/response implementation."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import sys
import threading


class ThreadingCapacity:
    def __init__(self, limit):
        if not 1 <= limit <= 64:
            raise ValueError('Gateway capacity must be 1..64')
        self.limit = limit

    def Lock(self):
        return threading.Lock()

    def BoundedSemaphore(self, original_limit):
        if original_limit != 12:
            raise ValueError('Unexpected frozen gateway capacity')
        return threading.BoundedSemaphore(self.limit)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--max-inflight', type=int, required=True)
    args, remaining = parser.parse_known_args()
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != args.source_sha256:
        raise ValueError('Frozen gateway source hash differs')
    spec = importlib.util.spec_from_file_location('frozen_gateway', args.source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.threading = ThreadingCapacity(args.max_inflight)

    class CapacityServer(module.ThreadingHTTPServer):
        request_queue_size = 128

    module.ThreadingHTTPServer = CapacityServer
    sys.argv = [str(args.source), *remaining]
    module.main()


if __name__ == '__main__':
    main()
