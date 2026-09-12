"""A two-request, harmless tool round-trip; compatibility evidence only."""
import argparse
import json
from pathlib import Path
import time
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    messages = [{"role": "user", "content": "Call the echo tool once with value HIL_PROBE_731. After the tool replies, output only the returned receipt."}]
    tools = [{"type": "function", "function": {"name": "echo", "description": "Return a harmless test receipt.",
        "parameters": {"type": "object", "properties": {"value": {"type": "string"}}, "required": ["value"]}}}]
    result = {"requested_model": args.model, "started_unix": time.time(), "tool_call_ok": False, "roundtrip_ok": False, "requests": []}
    try:
        for turn in range(2):
            payload = {"model": args.model, "messages": messages, "stream": False,
                       "max_tokens": 4096, "temperature": 0.2}
            if turn == 0:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"
            req = urllib.request.Request(args.base_url + "/chat/completions",
                    data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Authorization": "Bearer benchmark-relay"})
            with urllib.request.urlopen(req, timeout=190) as response:
                value = json.load(response)
            result["requests"].append(value)
            message = value["choices"][0]["message"]
            if turn == 0:
                calls = message.get("tool_calls") or []
                if len(calls) != 1 or calls[0]["function"]["name"] != "echo":
                    result["failure"] = "No single expected tool call"
                    break
                arguments = json.loads(calls[0]["function"]["arguments"])
                result["tool_call_ok"] = arguments.get("value") == "HIL_PROBE_731"
                if not result["tool_call_ok"]:
                    result["failure"] = "Incorrect tool arguments"
                    break
                messages += [message, {"role": "tool", "tool_call_id": calls[0]["id"], "content": '{"receipt":"HIL_OK_947"}'}]
            else:
                result["roundtrip_ok"] = "HIL_OK_947" in (message.get("content") or "")
    except urllib.error.HTTPError as error:
        result["http_status"] = error.code
        result["failure"] = "API request rejected"
    except Exception as error:
        result["failure"] = type(error).__name__
    result["finished_unix"] = time.time()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "requests"}))


if __name__ == "__main__":
    main()
