#!/usr/bin/env python3
"""CPython Bytecode & Memory Optimization Profiler.

Module 11 Turnkey Project Implementation.
Demonstrates dis, ast, gc, sys, and __slots__ optimization analysis.
"""

from __future__ import annotations

import ast
import dis
import sys
from collections import Counter
from collections.abc import Callable
from typing import Any


class InternalsProfiler:
    """Introspection and static analysis engine for CPython execution."""

    @staticmethod
    def analyze_bytecode(func: Callable[..., Any]) -> dict[str, Any]:
        """Disassembles a callable into opcodes and aggregates instruction metrics."""
        instructions = list(dis.get_instructions(func))
        opnames = [inst.opname for inst in instructions]
        opcode_counts = Counter(opnames)

        return {
            "function_name": func.__name__,
            "total_instructions": len(instructions),
            "unique_opcodes": len(opcode_counts),
            "top_opcodes": opcode_counts.most_common(5),
            "raw_instructions": [
                {"opname": inst.opname, "argval": inst.argval, "starts_line": inst.starts_line}
                for inst in instructions
            ],
        }

    @staticmethod
    def compare_instance_memory(std_instance: Any, slotted_instance: Any) -> dict[str, Any]:
        """Compares RAM footprint between standard __dict__ instance and slotted instance."""
        std_base = sys.getsizeof(std_instance)
        std_dict = sys.getsizeof(getattr(std_instance, "__dict__", {}))
        std_total = std_base + std_dict

        slotted_total = sys.getsizeof(slotted_instance)
        saved_bytes = max(0, std_total - slotted_total)
        savings_pct = (saved_bytes / std_total) * 100 if std_total > 0 else 0.0

        return {
            "standard_instance_bytes": std_total,
            "slotted_instance_bytes": slotted_total,
            "bytes_saved": saved_bytes,
            "savings_percent": round(savings_pct, 2),
        }

    @staticmethod
    def audit_ast_security(source_code: str) -> list[str]:
        """Performs static AST security checks for dangerous function calls and mutable defaults."""
        tree = ast.parse(source_code)
        issues: list[str] = []

        for node in ast.walk(tree):
            # Check 1: Banned function calls
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"eval", "exec", "compile"}
            ):
                issues.append(f"Line {node.lineno}: Dangerous built-in function '{node.func.id}()' called!")

            # Check 2: Mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(
                            f"Line {node.lineno}: Function '{node.name}' has mutable default argument of type {type(default).__name__}!"
                        )

        return issues


def sample_calculation(x: int, y: int) -> int:
    return (x * 2) + (y * 3)


class RegularUser:
    def __init__(self, uid: int, name: str) -> None:
        self.uid = uid
        self.name = name


class SlottedUser:
    __slots__ = ("name", "uid")
    def __init__(self, uid: int, name: str) -> None:
        self.uid = uid
        self.name = name


def main() -> None:
    print("=" * 65)
    print("      CPYTHON BYTECODE & MEMORY PROFILER DEMO")
    print("=" * 65)

    profiler = InternalsProfiler()

    print("\n1. Bytecode Analysis for 'sample_calculation':")
    bc_analysis = profiler.analyze_bytecode(sample_calculation)
    print(f"  Total Opcodes    : {bc_analysis['total_instructions']}")
    print(f"  Top Instructions : {bc_analysis['top_opcodes']}")

    print("\n2. Instance Memory Benchmark (__slots__ vs Standard):")
    reg_user = RegularUser(1, "Alice")
    slot_user = SlottedUser(1, "Alice")
    mem_analysis = profiler.compare_instance_memory(reg_user, slot_user)
    print(f"  Standard Instance RAM : {mem_analysis['standard_instance_bytes']} bytes")
    print(f"  Slotted Instance RAM  : {mem_analysis['slotted_instance_bytes']} bytes")
    print(f"  RAM Reduction         : {mem_analysis['savings_percent']}% saved!")

    print("\n3. AST Static Security Audit:")
    flawed_code = "def run(x=[]):\n    eval('2+2')\n"
    findings = profiler.audit_ast_security(flawed_code)
    for f in findings:
        print(f"  [ALERT] {f}")


if __name__ == "__main__":
    main()
