"""Unit tests for Model Context Protocol (MCP) Server and Client."""

from __future__ import annotations

import pytest
from mcp_protocol_engine import MCPClient, MCPServer


@pytest.fixture
def mcp_setup() -> tuple[MCPServer, MCPClient]:
    server = MCPServer(name="test_analytics_server", version="1.2.0")

    def query_sales(region: str, quarter: int) -> str:
        return f"Sales for {region} Q{quarter}: $1,500,000"

    server.register_tool(
        name="query_sales",
        description="Query regional sales numbers",
        input_schema={"type": "object", "properties": {"region": {"type": "string"}, "quarter": {"type": "integer"}}},
        handler=query_sales,
    )

    server.register_resource(
        uri="system://schemas/sales.json",
        name="Sales Schema",
        content="{\"type\": \"sales_record\"}",
        mime_type="application/json",
    )

    client = MCPClient(server=server)
    return server, client


def test_mcp_initialize_handshake(mcp_setup: tuple[MCPServer, MCPClient]):
    _, client = mcp_setup
    init_res = client.initialize()
    assert init_res["protocolVersion"] == "2024-11-05"
    assert init_res["serverInfo"]["name"] == "test_analytics_server"
    assert "tools" in client.server_capabilities


def test_mcp_tool_discovery_and_execution(mcp_setup: tuple[MCPServer, MCPClient]):
    _, client = mcp_setup
    client.initialize()
    tools = client.list_tools()
    assert len(tools) == 1
    assert tools[0]["name"] == "query_sales"

    result = client.call_tool("query_sales", {"region": "EMEA", "quarter": 3})
    assert "Sales for EMEA Q3: $1,500,000" in result


def test_mcp_resource_read(mcp_setup: tuple[MCPServer, MCPClient]):
    _, client = mcp_setup
    client.initialize()
    content = client.read_resource("system://schemas/sales.json")
    assert "sales_record" in content


def test_mcp_invalid_tool_error(mcp_setup: tuple[MCPServer, MCPClient]):
    _, client = mcp_setup
    client.initialize()
    with pytest.raises(RuntimeError) as exc_info:
        client.call_tool("unknown_tool", {})
    assert "Tool 'unknown_tool' not found" in str(exc_info.value)
