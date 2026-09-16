"""Tool Execution Engine with Schema Introspection, Type Validation, and Timeouts."""

from __future__ import annotations

import concurrent.futures
import inspect
from typing import Any, Callable, Dict, List, Optional, get_type_hints


class ToolExecutionError(Exception):
    """Raised when tool execution fails or violates schema."""


class ToolExecutionEngine:
    """Production Tool Execution and Dispatch Engine."""

    def __init__(self, default_timeout_sec: float = 3.0) -> None:
        self.default_timeout_sec = default_timeout_sec
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register(self, fn: Callable[..., Any]) -> None:
        """Registers a function, generating its JSON schema via reflection."""
        name = fn.__name__
        sig = inspect.signature(fn)
        hints = get_type_hints(fn)
        doc = inspect.getdoc(fn) or ""

        properties: Dict[str, Dict[str, str]] = {}
        required: List[str] = []

        for param_name, param in sig.parameters.items():
            param_type = hints.get(param_name, str)
            if param_type is int:
                json_type = "integer"
            elif param_type is float:
                json_type = "number"
            elif param_type is bool:
                json_type = "boolean"
            else:
                json_type = "string"

            properties[param_name] = {"type": json_type}
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            "name": name,
            "description": doc.split("\n")[0] if doc else f"Tool {name}",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

        self._tools[name] = fn
        self._schemas[name] = schema

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Returns all registered tool schemas in standard format."""
        return list(self._schemas.values())

    def validate_and_coerce_args(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validates arguments against schema and coerces simple types."""
        if tool_name not in self._schemas:
            raise ToolExecutionError(f"Tool '{tool_name}' not found.")

        schema = self._schemas[tool_name]
        required = schema["parameters"].get("required", [])
        props = schema["parameters"].get("properties", {})

        # Check required
        for req in required:
            if req not in args:
                raise ToolExecutionError(f"Missing required parameter '{req}' for tool '{tool_name}'.")

        coerced: Dict[str, Any] = {}
        for key, val in args.items():
            if key not in props:
                coerced[key] = val
                continue

            expected_type = props[key]["type"]
            try:
                if expected_type == "integer" and not isinstance(val, int):
                    coerced[key] = int(val)
                elif expected_type == "number" and not isinstance(val, (int, float)):
                    coerced[key] = float(val)
                elif expected_type == "boolean" and not isinstance(val, bool):
                    coerced[key] = str(val).lower() in ("true", "1", "yes")
                elif expected_type == "string" and not isinstance(val, str):
                    coerced[key] = str(val)
                else:
                    coerced[key] = val
            except (ValueError, TypeError) as exc:
                raise ToolExecutionError(
                    f"Invalid type for parameter '{key}': expected {expected_type}, got {type(val).__name__} ({exc})"
                )

        return coerced

    def dispatch(
        self,
        tool_name: str,
        args: Dict[str, Any],
        timeout_sec: Optional[float] = None,
    ) -> str:
        """Dispatches tool execution within a timeout-guarded thread."""
        timeout = timeout_sec or self.default_timeout_sec

        try:
            valid_args = self.validate_and_coerce_args(tool_name, args)
        except ToolExecutionError as err:
            return f"Validation Error: {str(err)}"

        fn = self._tools[tool_name]

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(fn, **valid_args)
            try:
                result = future.result(timeout=timeout)
                return str(result)
            except concurrent.futures.TimeoutError:
                return f"Execution Timeout: Tool '{tool_name}' exceeded timeout of {timeout}s."
            except Exception as exc:
                return f"Runtime Error in '{tool_name}': {str(exc)}"
