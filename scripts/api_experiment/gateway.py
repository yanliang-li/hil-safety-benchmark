"""Allowlisted API relay; keep the real credential outside agent containers.

Pass upstream bytes through unchanged. Record requested/returned model IDs,
payloads, usage and errors, never authentication headers. No hidden retries.
"""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading
import time
import urllib.request
import urllib.error
import urllib.parse


def save(path, value):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text())
    key = profile["api_key"]
    base = profile["base_url"].rstrip("/")
    lock = threading.Lock()
    active = threading.BoundedSemaphore(12)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *_):
            pass

        def respond(self, code, message):
            content = json.dumps({"error": {"message": message}}).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def do_GET(self):
            if self.path != "/health":
                return self.respond(404, "Unknown route")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        def do_POST(self):
            path_part = urllib.parse.urlsplit(self.path).path
            match = re.fullmatch(r"/r/([A-Za-z0-9_-]{1,160})/v1/(chat/completions|responses|messages)", path_part)
            if not match:
                return self.respond(404, "Only registered model inference routes are supported")
            run_id = match[1]
            endpoint = match[2]
            registration = args.registry / f"{run_id}.json"
            if not registration.is_file():
                return self.respond(403, "Unregistered run")
            spec = json.loads(registration.read_text())
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length < 4_000_000:
                return self.respond(413, "Request size limit")
            body = self.rfile.read(length)
            try:
                payload = json.loads(body)
            except ValueError:
                return self.respond(400, "Invalid JSON")
            if payload.get("model") != spec["model"]:
                return self.respond(403, "Model does not match registered run")
            directory = args.evidence / run_id
            directory.mkdir(parents=True, exist_ok=True)
            with lock:
                sequence = len(list(directory.glob("request_*.json"))) + 1
                if sequence > spec.get("max_requests", 64):
                    return self.respond(429, "Registered run request limit reached")
                path = directory / f"request_{sequence:03d}.json"
                record = {
                    "run_id": run_id, "sequence": sequence,
                    "endpoint": endpoint,
                    "started_unix": time.time(), "request": payload,
                    "request_body_sha256": hashlib.sha256(body).hexdigest(),
                    "state": "pending", "transport_retries": 0,
                }
                save(path, record)
            raw = bytearray()
            status = None
            received = 0
            first_byte = None
            upstream = None
            try:
                with active:
                    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
                    if endpoint == "messages":
                        headers.update({"x-api-key": key, "anthropic-version": self.headers.get("anthropic-version", "2023-06-01")})
                        if self.headers.get("anthropic-beta"):
                            headers["anthropic-beta"] = self.headers["anthropic-beta"]
                    request = urllib.request.Request(base + "/" + endpoint, data=body, headers=headers)
                    try:
                        upstream = urllib.request.urlopen(request, timeout=180)
                    except urllib.error.HTTPError as error:
                        upstream = error
                    status = upstream.status
                    record["http_status"] = status
                    record["upstream_request_id"] = upstream.headers.get("x-request-id")
                    record["content_type"] = upstream.headers.get("Content-Type", "application/json")
                    self.send_response(status)
                    self.send_header("Content-Type", record["content_type"])
                    self.send_header("Cache-Control", "no-store")
                    self.end_headers()
                    while True:
                        chunk = upstream.read1(8192)
                        if not chunk:
                            break
                        if first_byte is None:
                            first_byte = time.time()
                        received += len(chunk)
                        if received > 8_000_000:
                            raise ValueError("Response size limit")
                        raw.extend(chunk)
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    record["state"] = "complete" if status == 200 else "upstream_error"
            except Exception as error:
                record["state"] = "transport_error"
                record["error_type"] = type(error).__name__
                if status is None:
                    try:
                        self.respond(502, "Upstream transport failure: " + type(error).__name__)
                    except OSError:
                        pass
            finally:
                if upstream is not None:
                    upstream.close()
                response_text = raw.decode("utf-8", errors="replace").replace(key, "<REDACTED>")
                record.update(finished_unix=time.time(), first_byte_unix=first_byte,
                              response_bytes=received, raw_response=response_text)
                objects = []
                if "text/event-stream" in record.get("content_type", ""):
                    for line in response_text.splitlines():
                        if line.startswith("data:") and line[5:].strip() != "[DONE]":
                            try:
                                objects.append(json.loads(line[5:]))
                            except ValueError:
                                pass
                else:
                    try:
                        objects = [json.loads(response_text)]
                    except ValueError:
                        pass
                expanded = []
                for obj in objects:
                    if isinstance(obj, dict):
                        expanded.extend(obj[k] for k in ("response", "message") if isinstance(obj.get(k), dict))
                        expanded.append(obj)
                objects = expanded
                record["returned_models"] = sorted({o["model"] for o in objects if isinstance(o, dict) and o.get("model")})
                record["system_fingerprints"] = sorted({o["system_fingerprint"] for o in objects if isinstance(o, dict) and o.get("system_fingerprint")})
                usage = {}
                for obj in objects:
                    if isinstance(obj.get("usage"), dict):
                        usage.update({k: v for k, v in obj["usage"].items() if v is not None})
                record["usage"] = usage or None
                safe_record = json.loads(json.dumps(record, ensure_ascii=False).replace(key, "<REDACTED>"))
                save(path, safe_record)

    ThreadingHTTPServer(("0.0.0.0", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
