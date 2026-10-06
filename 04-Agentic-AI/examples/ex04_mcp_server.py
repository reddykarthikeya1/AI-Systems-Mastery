"""Example 4: a real MCP server (official Python SDK, mcp==2.3.0).

NOTE: in mcp 1.x the class is `mcp.server.fastmcp.FastMCP`; in mcp 2.x it is
`mcp.server.mcpserver.MCPServer`. Pin your version (requirements.txt).

Run as a server (stdio transport): python ex04_mcp_server.py serve
Self-test (calls the tools in-process):  python ex04_mcp_server.py
"""
import asyncio
import sys

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("orders")

ORDERS = {"A-1001": {"status": "shipped", "eta_days": 2}, "A-1002": {"status": "processing", "eta_days": 5}}


@mcp.tool()
def get_order_status(order_id: str) -> str:
    """Look up the shipping status of an order by its ID (format A-1234)."""
    order = ORDERS.get(order_id)
    if order is None:
        # Return the explanation instead of raising: in mcp 2.3 an uncaught exception reaches the model only as
        # "Error executing tool ...", so a fixable mistake should be reported in the result text.
        return f"ERROR: unknown order {order_id!r}. Valid IDs look like A-1001."
    return f"{order_id}: {order['status']}, arrives in {order['eta_days']} days"


@mcp.resource("orders://summary")
def summary() -> str:
    """A read-only resource: counts by status."""
    counts = {}
    for o in ORDERS.values():
        counts[o["status"]] = counts.get(o["status"], 0) + 1
    return ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))


async def self_test():
    tools = await mcp.list_tools()
    names = [t.name for t in tools]
    assert names == ["get_order_status"], names
    assert "order_id" in str(tools[0].input_schema or getattr(tools[0], "inputSchema", ""))  # schema derived from type hints
    result = await mcp.call_tool("get_order_status", {"order_id": "A-1001"})
    text = str(result)
    assert "shipped" in text, text
    bad = await mcp.call_tool("get_order_status", {"order_id": "ZZZ"})
    assert "unknown order" in str(bad), bad   # the model can read how to fix its call
    print("OK: tools =", names)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        mcp.run()  # stdio by default
    else:
        asyncio.run(self_test())
