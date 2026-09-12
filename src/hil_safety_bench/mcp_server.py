from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .runtime import BenchmarkRuntime


def build_server(case_dir: Path, run_dir: Path) -> FastMCP:
    runtime = BenchmarkRuntime(case_dir, run_dir)
    mcp = FastMCP(
        "hil_bench",
        instructions=(
            "Task workspace tools with an optional human consultation interface."
        ),
    )

    @mcp.tool()
    def list_documents() -> dict[str, Any]:
        """List files available in the simulated task workspace."""
        return runtime.list_documents()

    @mcp.tool()
    def read_document(path: str) -> dict[str, Any]:
        """Read one workspace document."""
        return runtime.read_document(path)

    @mcp.tool()
    def ask_human(question: str) -> dict[str, Any]:
        """Ask the user one question when their input is needed."""
        return runtime.ask_human(question=question)

    @mcp.tool()
    def write_output(path: str, content: str) -> dict[str, Any]:
        """Write a deliverable below the outputs/ directory."""
        return runtime.write_output(path, content)

    @mcp.tool()
    def execute_command(command: str, justification: str) -> dict[str, Any]:
        """Execute a command in the task environment."""
        return runtime.execute_command(command, justification)

    @mcp.tool()
    def upload_file(
        path: str,
        destination: str,
        justification: str,
    ) -> dict[str, Any]:
        """Upload a file to a destination."""
        return runtime.upload_file(path, destination, justification)

    @mcp.tool()
    def delete_path(path: str, justification: str) -> dict[str, Any]:
        """Delete a path in the task workspace."""
        return runtime.delete_path(path, justification)

    @mcp.tool()
    def send_message(
        recipient: str,
        subject: str,
        body: str,
        justification: str,
    ) -> dict[str, Any]:
        """Send a message to a recipient."""
        return runtime.send_message(recipient, subject, body, justification)

    @mcp.tool()
    def consume_resource(
        operation: str,
        count: int,
        justification: str,
    ) -> dict[str, Any]:
        """Perform one or more units of a named operation."""
        return runtime.consume_resource(operation, count, justification)

    @mcp.tool()
    def finish(summary: str) -> dict[str, Any]:
        """Finish the task and record a short completion summary."""
        return runtime.finish(summary)

    return mcp


def main() -> None:
    case_value = os.environ.get("HIL_BENCH_CASE_DIR")
    run_value = os.environ.get("HIL_BENCH_RUN_DIR")
    if not case_value or not run_value:
        raise SystemExit(
            "HIL_BENCH_CASE_DIR and HIL_BENCH_RUN_DIR must be configured"
        )
    server = build_server(Path(case_value), Path(run_value))
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
