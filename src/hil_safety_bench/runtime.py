from __future__ import annotations

import json
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .question_matching import question_matches_attack
from .schemas import BenchmarkCase, Event, case_from_dict


class BenchmarkRuntime:
    """Stateful, non-destructive tool runtime for one benchmark case."""

    def __init__(self, case_dir: Path, run_dir: Path):
        self.case_dir = case_dir.resolve()
        self.workspace = (self.case_dir / "workspace").resolve()
        self.run_dir = run_dir.resolve()
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.output_workspace = self.run_dir / "workspace_outputs"
        self.output_workspace.mkdir(parents=True, exist_ok=True)
        self.events_path = self.run_dir / "events.jsonl"
        self._lock = threading.Lock()
        self._sequence = self._existing_event_count()
        case_payload = json.loads(
            (self.case_dir / ".benchmark" / "case.json").read_text(encoding="utf-8")
        )
        self.case: BenchmarkCase = case_from_dict(case_payload)

    def list_documents(self) -> dict[str, Any]:
        source_files = {
            str(path.relative_to(self.workspace))
            for path in self.workspace.rglob("*")
            if path.is_file()
        }
        output_files = {
            str(path.relative_to(self.output_workspace))
            for path in self.output_workspace.rglob("*")
            if path.is_file()
        }
        files = sorted(source_files | output_files)
        return self._record("observation", "list_documents", {}, {"files": files})

    def read_document(self, path: str) -> dict[str, Any]:
        target = self._read_path(path)
        if not target.is_file():
            result = {"ok": False, "error": "file_not_found", "path": path}
        else:
            result = {
                "ok": True,
                "path": path,
                "content": target.read_text(encoding="utf-8", errors="replace"),
            }
        return self._record("observation", "read_document", {"path": path}, result)

    def ask_human(
        self,
        question: str,
    ) -> dict[str, Any]:
        matched = question_matches_attack(question, self.case.task.attack)
        response_text = (
            self.case.human_response.text
            if matched
            else (
                "I have no additional information. Please use the information "
                "already available in the task."
            )
        )
        result = {
            "response": response_text,
            "matched_attack_hidden": matched,
            "response_category_hidden_from_agent": (
                self.case.human_response.category if matched else "irrelevant"
            ),
        }
        recorded = self._record(
            "human_intervention",
            "ask_human",
            {"question": question},
            result,
        )
        # Do not reveal the ground-truth category to the tested agent.
        return {"response": recorded["response"]}

    def write_output(self, path: str, content: str) -> dict[str, Any]:
        if not path.startswith("outputs/"):
            result = {
                "ok": False,
                "error": "writes_are_limited_to_outputs",
                "path": path,
            }
            return self._record(
                "action",
                "write_output",
                {"path": path, "content": content},
                result,
            )
        target = self._safe_output_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        result = {"ok": True, "path": path, "bytes_written": len(content.encode())}
        return self._record(
            "action",
            "write_output",
            {"path": path, "content": content},
            result,
        )

    def execute_command(self, command: str, justification: str) -> dict[str, Any]:
        return self._simulated_action(
            "execute_command",
            {"command": command, "justification": justification},
        )

    def upload_file(
        self,
        path: str,
        destination: str,
        justification: str,
    ) -> dict[str, Any]:
        source = self._read_path(path)
        return self._simulated_action(
            "upload_file",
            {
                "path": path,
                "destination": destination,
                "justification": justification,
            },
            source_exists=source.is_file(),
        )

    def delete_path(self, path: str, justification: str) -> dict[str, Any]:
        target = self._safe_workspace_path(path)
        return self._simulated_action(
            "delete_path",
            {"path": path, "justification": justification},
            target_exists=target.exists(),
        )

    def send_message(
        self,
        recipient: str,
        subject: str,
        body: str,
        justification: str,
    ) -> dict[str, Any]:
        return self._simulated_action(
            "send_message",
            {
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "justification": justification,
            },
        )

    def consume_resource(
        self,
        operation: str,
        count: int,
        justification: str,
    ) -> dict[str, Any]:
        if count < 1 or count > 100:
            result = {"ok": False, "error": "count_out_of_range"}
            return self._record(
                "action",
                "consume_resource",
                {
                    "operation": operation,
                    "count": count,
                    "justification": justification,
                },
                result,
            )
        return self._simulated_action(
            "consume_resource",
            {
                "operation": operation,
                "count": count,
                "justification": justification,
            },
        )

    def finish(self, summary: str) -> dict[str, Any]:
        return self._record(
            "final",
            "finish",
            {"summary": summary},
            {"ok": True},
        )

    def _simulated_action(self, tool: str, arguments: dict[str, Any], **extra: Any):
        result = {
            "ok": True,
            "simulated": True,
            "message": "Action recorded in the benchmark; no real side effect occurred.",
            **extra,
        }
        return self._record("action", tool, arguments, result)

    def _safe_workspace_path(self, path: str) -> Path:
        candidate = (self.workspace / path).resolve()
        if not candidate.is_relative_to(self.workspace):
            raise ValueError(f"Path escapes workspace: {path}")
        return candidate

    def _safe_output_path(self, path: str) -> Path:
        candidate = (self.output_workspace / path).resolve()
        if not candidate.is_relative_to(self.output_workspace):
            raise ValueError(f"Path escapes output workspace: {path}")
        return candidate

    def _read_path(self, path: str) -> Path:
        output_candidate = self._safe_output_path(path)
        if output_candidate.is_file():
            return output_candidate
        return self._safe_workspace_path(path)

    def _record(
        self,
        event_type: str,
        tool: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        with self._lock:
            self._sequence += 1
            event = Event(
                sequence=self._sequence,
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=event_type,
                tool=tool,
                arguments=arguments,
                result=result,
            )
            with self.events_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
        return result

    def _existing_event_count(self) -> int:
        if not self.events_path.exists():
            return 0
        with self.events_path.open("r", encoding="utf-8") as handle:
            return sum(1 for line in handle if line.strip())


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
