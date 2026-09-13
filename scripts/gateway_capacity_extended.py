"""Raise only admission capacity; load the same hash-checked wire handler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import threading

from gateway_capacity_ramp import AdjustableSemaphore


class ExtendedSemaphore(AdjustableSemaphore):
    def __init__(self, control, maximum=256):
        if maximum != 256:
            raise ValueError('The extended ceiling is 256')
        self.control = Path(control)
        self.maximum = maximum
        self.condition = threading.Condition()
        self.active = 0

    def limit(self):
        value = json.loads(self.control.read_text())['gateway_max_inflight']
        if type(value) is not int or value not in (64, 96, 128, 160, 192, 224, 256):
            raise ValueError('Unrecorded relay target')
        return value


class ThreadingCapacity:
    def __init__(self, control):
        self.control = control

    def Lock(self):
        return threading.Lock()

    def BoundedSemaphore(self, limit):
        if limit != 12:
            raise ValueError('Unexpected frozen gateway capacity')
        return ExtendedSemaphore(self.control)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--source-sha256', required=True)
    parser.add_argument('--max-inflight', type=int, required=True)
    parser.add_argument('--capacity-control', type=Path, required=True)
    args, remaining = parser.parse_known_args()
    if args.max_inflight != 256 or hashlib.sha256(args.source.read_bytes()).hexdigest() != args.source_sha256:
        raise ValueError('Frozen gateway source or declared ceiling differs')
    spec = importlib.util.spec_from_file_location('frozen_gateway', args.source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.threading = ThreadingCapacity(args.capacity_control)
    class CapacityServer(module.ThreadingHTTPServer):
        request_queue_size = 512
    module.ThreadingHTTPServer = CapacityServer
    sys.argv = [str(args.source), *remaining]
    module.main()


if __name__ == '__main__':
    main()
