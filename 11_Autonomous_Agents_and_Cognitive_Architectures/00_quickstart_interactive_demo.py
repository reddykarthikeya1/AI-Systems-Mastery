"""Course 11 Quickstart: Interactive Model Context Protocol (MCP) & Streaming Parser Demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Module_03_Tool_Execution_and_Constrained_Generation" / "project_solution"))
from mcp_protocol_engine import MCPClient, MCPServer
from streaming_tool_parser import StreamingToolParser


def run_demo() -> None:
    print("=" * 70)
    print(" COURSE 11: AUTONOMOUS AGENTS & COGNITIVE ARCHITECTURES QUICKSTART")
    print("=" * 70)

    print("\n[1] Anthropic Model Context Protocol (MCP) Server & Client Session:")
    server = MCPServer(name="enterprise_k8s_agent", version="2.0.0")

    def scale_cluster(deployment: str, replicas: int) -> str:
        return f"Scaled deployment '{deployment}' to {replicas} pods successfully."

    server.register_tool(
        name="scale_cluster",
        description="Scales a Kubernetes deployment",
        input_schema={"type": "object", "properties": {"deployment": {"type": "string"}, "replicas": {"type": "integer"}}},
        handler=scale_cluster,
    )

    client = MCPClient(server=server)
    init_res = client.initialize()
    print(f"     * Handshake Initialized: Protocol {init_res['protocolVersion']} (Server: {init_res['serverInfo']['name']})")

    tools = client.list_tools()
    print(f"     * Discovered Tool: '{tools[0]['name']}' - {tools[0]['description']}")

    tool_call_result = client.call_tool("scale_cluster", {"deployment": "vllm-serving", "replicas": 8})
    print(f"     * Tool Call Execution Result: {tool_call_result}")

    print("\n[2] Real-time Streaming JSON Tool Parameter Parser:")
    early_extracted = []
    parser = StreamingToolParser(on_field_ready=lambda k, v: early_extracted.append((k, v)))

    token_stream = ['{"pod_name":', ' "vllm-worker-4",', ' "memory_gb":', ' 64,', ' "gpu":', ' "H100"}']
    print("     * Simulating token stream from LLM generation...")
    for chunk in token_stream:
        parser.feed_token(chunk)

    print("     * Asynchronous parameters parsed on-the-fly:")
    for field, val in early_extracted:
        print(f"       -> Parsed '{field}': {val}")

    print("\n" + "=" * 70)
    print(" QUICKSTART DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
