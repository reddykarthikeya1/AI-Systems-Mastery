"""Sandboxed Code Execution Engine with AST Security Analysis and Subprocess Isolation."""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import List


class SecurityViolationError(Exception):
    """Raised when code violates security policies."""


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    is_timeout: bool = False
    security_violations: List[str] = None


class ASTSecurityInspector(ast.NodeVisitor):
    """Inspects Python AST for banned modules, functions, and reflection hacks."""

    BANNED_MODULES = {"os", "sys", "subprocess", "shutil", "socket", "ctypes", "pty"}
    BANNED_BUILTINS = {"eval", "exec", "open", "__import__", "compile", "breakpoint"}

    def __init__(self) -> None:
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root_mod = alias.name.split(".")[0]
            if root_mod in self.BANNED_MODULES:
                self.violations.append(f"Forbidden module import: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            root_mod = node.module.split(".")[0]
            if root_mod in self.BANNED_MODULES:
                self.violations.append(f"Forbidden from-import: '{node.module}'")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id in self.BANNED_BUILTINS:
                self.violations.append(f"Forbidden builtin call: '{node.func.id}()'")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__") and node.attr.endswith("__"):
            if node.attr in {"__subclasses__", "__bases__", "__globals__", "__code__"}:
                self.violations.append(f"Forbidden reflection attribute access: '{node.attr}'")
        self.generic_visit(node)


class SandboxedExecutor:
    """Executes Python code with AST inspection, timeouts, and output sanitization."""

    SECRET_PATTERNS = [
        re.compile(r"sk-[A-Za-z0-9_-]{20,}", re.IGNORECASE),
        re.compile(r"AKIA[0-9A-Z]{16}", re.IGNORECASE),
    ]

    def __init__(self, timeout_sec: float = 2.0) -> None:
        self.timeout_sec = timeout_sec

    def inspect_code(self, code_str: str) -> List[str]:
        """Performs AST static security audit."""
        try:
            tree = ast.parse(code_str)
        except SyntaxError as e:
            return [f"SyntaxError: {str(e)}"]

        inspector = ASTSecurityInspector()
        inspector.visit(tree)
        return inspector.violations

    def sanitize_output(self, text: str) -> str:
        """Redacts secrets and sensitive tokens from execution output."""
        sanitized = text
        for pat in self.SECRET_PATTERNS:
            sanitized = pat.sub("[REDACTED_SECRET]", sanitized)
        return sanitized

    def execute(self, code_str: str) -> ExecutionResult:
        """Audits and runs code in an isolated subprocess."""
        violations = self.inspect_code(code_str)
        if violations:
            return ExecutionResult(
                stdout="",
                stderr="; ".join(violations),
                exit_code=1,
                is_timeout=False,
                security_violations=violations,
            )

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(code_str)
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, tmp_path]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
            )
            return ExecutionResult(
                stdout=self.sanitize_output(proc.stdout),
                stderr=self.sanitize_output(proc.stderr),
                exit_code=proc.returncode,
                is_timeout=False,
                security_violations=[],
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                stdout="",
                stderr=f"Execution timed out after {self.timeout_sec}s",
                exit_code=-1,
                is_timeout=True,
                security_violations=[],
            )
