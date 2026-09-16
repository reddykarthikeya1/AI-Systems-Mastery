"""Model Context Protocol (MCP) Reference Implementation for Autonomous Agents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

# Standard JSON-RPC 2.0 Error Codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable[..., Any]


@dataclass
class MCPResource:
    uri: str
    name: str
    mime_type: str
    content: str


class MCPServer:
    """Production Model Context Protocol (MCP) Server."""

    def __init__(self, name: str, version: str = "1.0.0") -> None:
        self.server_info = {"name": name, "version": version}
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.is_initialized: bool = False

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable[..., Any],
    ) -> None:
        self.tools[name] = MCPTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
        )

    def register_resource(
        self,
        uri: str,
        name: str,
        content: str,
        mime_type: str = "text/plain",
    ) -> None:
        self.resources[uri] = MCPResource(
            uri=uri,
            name=name,
            mime_type=mime_type,
            content=content,
        )

    def handle_request(self, request_json: str) -> str:
        try:
            req = json.loads(request_json)
        except json.JSONDecodeError as exc:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": PARSE_ERROR, "message": f"Parse error: {str(exc)}"},
            })

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if req.get("jsonrpc") != "2.0" or not method:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": INVALID_REQUEST, "message": "Invalid JSON-RPC request"},
            })

        if method == "initialize":
            self.is_initialized = True
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                },
                "serverInfo": self.server_info,
            }
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})

        if method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.input_schema,
                    }
                    for t in self.tools.values()
                ]
            }
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            if tool_name not in self.tools:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": INVALID_PARAMS, "message": f"Tool '{tool_name}' not found"},
                })

            try:
                call_res = self.tools[tool_name].handler(**tool_args)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": str(call_res)}], "isError": False},
                })
            except Exception as exc:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"Error: {str(exc)}"}], "isError": True},
                })

        elif method == "resources/list":
            result = {
                "resources": [
                    {"uri": r.uri, "name": r.name, "mimeType": r.mime_type}
                    for r in self.resources.values()
                ]
            }
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})

        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self.resources:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": INVALID_PARAMS, "message": f"Resource URI '{uri}' not found"},
                })
            r = self.resources[uri]
            result = {"contents": [{"uri": r.uri, "mimeType": r.mime_type, "text": r.content}]}
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})

        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": METHOD_NOT_FOUND, "message": f"Method '{method}' not implemented"},
        })


class MCPClient:
    """Client agent session connecting to an MCP Server."""

    def __init__(self, server: MCPServer) -> None:
        self.server = server
        self._next_id = 1
        self.server_capabilities: Dict[str, Any] = {}

    def _call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        req_id = self._next_id
        self._next_id += 1
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {},
        })
        raw_res = self.server.handle_request(payload)
        res = json.loads(raw_res)
        if "error" in res:
            raise RuntimeError(f"MCP RPC Error ({res['error']['code']}): {res['error']['message']}")
        return res.get("result", {})

    def initialize(self) -> Dict[str, Any]:
        result = self._call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}})
        self.server_capabilities = result.get("capabilities", {})
        return result

    def list_tools(self) -> List[Dict[str, Any]]:
        res = self._call("tools/list")
        return res.get("tools", [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        res = self._call("tools/call", {"name": name, "arguments": arguments})
        contents = res.get("content", [])
        if contents and "text" in contents[0]:
            return contents[0]["text"]
        return ""

    def read_resource(self, uri: str) -> str:
        res = self._call("resources/read", {"uri": uri})
        contents = res.get("contents", [])
        if contents and "text" in contents[0]:
            return contents[0]["text"]
        return ""
