import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from hil_safety_bench.generate import generate_cases, materialize_case
from hil_safety_bench.responses import TemplateResponseProvider


def test_stdio_mcp_server_lists_tools_and_documents(tmp_path: Path):
    case = generate_cases(
        provider=TemplateResponseProvider(),
        seed=42,
        profiles="all",
    )[0]
    case_dir = materialize_case(case, tmp_path / "cases")
    run_dir = tmp_path / "run"

    async def exercise_server():
        parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "hil_safety_bench.mcp_server"],
            env={
                **os.environ,
                "HIL_BENCH_CASE_DIR": str(case_dir),
                "HIL_BENCH_RUN_DIR": str(run_dir),
            },
        )
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = {tool.name for tool in tools.tools}
                assert "ask_human" in names
                assert "upload_file" in names
                ask_tool = next(
                    tool for tool in tools.tools if tool.name == "ask_human"
                )
                assert set(
                    ask_tool.inputSchema.get("properties", {})
                ) == {"question"}
                result = await session.call_tool("list_documents", {})
                assert not result.isError
                assert result.content

    asyncio.run(exercise_server())

