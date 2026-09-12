"""Adjust only relay admission limits; the frozen protocol handler is unchanged."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import threading
import time


class AdjustableSemaphore:
    def __init__(self, control, maximum=128):
        if maximum != 128:
            raise ValueError('The recorded relay ceiling is 128')
        self.control = Path(control)
        self.maximum = maximum
        self.condition = threading.Condition()
        self.active = 0

    def limit(self):
        value = json.loads(self.control.read_text())['gateway_max_inflight']
        if type(value) is not int or value not in (64, 96, 128) or value > self.maximum:
            raise ValueError('Unrecorded relay target')
        return value

    def acquire(self, blocking=True, timeout=None):
        end = time.monotonic() + timeout if timeout is not None else None
        with self.condition:
            while self.active >= self.limit():
                if not blocking:
                    return False
                remaining = end - time.monotonic() if end is not None else .1
                if remaining <= 0:
                    return False
                self.condition.wait(min(.1, remaining))
            self.active += 1
            return True

    def release(self):
        with self.condition:
            if self.active <= 0:
                raise ValueError('Unmatched relay permit release')
            self.active -= 1
            self.condition.notify_all()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *_):
        self.release()


class ThreadingCapacity:
    def __init__(self, control, maximum):
        self.control, self.maximum = control, maximum

    def Lock(self):
        return threading.Lock()

    def BoundedSemaphore(self, original_limit):
        if original_limit != 12:
            raise ValueError('Unexpected frozen gateway capacity')
        return AdjustableSemaphore(self.control, self.maximum)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--max-inflight', type=int, required=True)
    parser.add_argument('--capacity-control', type=Path, required=True)
    args, remaining = parser.parse_known_args()
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != args.source_sha256:
        raise ValueError('Frozen gateway source hash differs')
    spec = importlib.util.spec_from_file_location('frozen_gateway', args.source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.threading = ThreadingCapacity(args.capacity_control, args.max_inflight)

    class CapacityServer(module.ThreadingHTTPServer):
        request_queue_size = 256

    module.ThreadingHTTPServer = CapacityServer
    sys.argv = [str(args.source), *remaining]
    module.main()


if __name__ == '__main__':
    main()
