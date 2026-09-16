#!/usr/bin/env python3
"""Module 11: AST (Abstract Syntax Tree) Security Linter Demonstration.

This script demonstrates parsing Python source code into an AST and
building a static security audit scanner.
"""

from __future__ import annotations

import ast

CODE_TO_AUDIT = """
import os

def authenticate_user(username, password):
    # Security Flaw 1: Hardcoded sensitive secret
    api_key = "sk_live_SECRET_KEY_12345"

    # Security Flaw 2: Dangerous eval execution
    user_data = eval(username)

    return True
"""


class SecurityAuditVisitor(ast.NodeVisitor):
    """AST visitor searching for dangerous function calls and secrets."""

    def __init__(self) -> None:
        self.findings: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        # Detect calls to eval() or exec()
        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            self.findings.append(
                f"[CRITICAL VULNERABILITY] Use of dangerous function '{node.func.id}()' detected at line {node.lineno}!"
            )
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        # Detect hardcoded secret tokens
        for target in node.targets:
            if (
                ((isinstance(target, ast.Name) and "key" in target.id.lower()) or "secret" in target.id.lower())
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
            ):
                self.findings.append(
                    f"[SECURITY RISK] Potential hardcoded credential '{target.id}' at line {node.lineno}!"
                )
        self.generic_visit(node)


def main() -> None:
    print("=" * 60)
    print("  AST-Based Static Code Security Linter Demonstration")
    print("=" * 60)

    parsed_ast = ast.parse(CODE_TO_AUDIT)
    auditor = SecurityAuditVisitor()
    auditor.visit(parsed_ast)

    print(f"Scanned AST Nodes. Total Security Findings: {len(auditor.findings)}\n")
    for finding in auditor.findings:
        print(f"  {finding}")


if __name__ == "__main__":
    main()
