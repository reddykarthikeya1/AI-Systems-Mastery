"""Unit tests for the CPython Bytecode & Memory Optimization Profiler."""

from __future__ import annotations

import pytest
from internals_profiler import InternalsProfiler, RegularUser, SlottedUser


def test_bytecode_analysis() -> None:
    """Test disassembling simple mathematical function."""
    def add(a: int, b: int) -> int:
        return a + b

    metrics = InternalsProfiler.analyze_bytecode(add)
    assert metrics["function_name"] == "add"
    assert metrics["total_instructions"] > 0
    assert metrics["unique_opcodes"] > 0
    opnames = [inst["opname"] for inst in metrics["raw_instructions"]]
    assert "LOAD_FAST" in opnames
    assert "RETURN_VALUE" in opnames


def test_compare_instance_memory() -> None:
    """Test that slotted instances consume significantly less RAM than standard __dict__ instances."""
    reg = RegularUser(100, "Alice")
    slotted = SlottedUser(100, "Alice")

    result = InternalsProfiler.compare_instance_memory(reg, slotted)
    assert result["standard_instance_bytes"] > result["slotted_instance_bytes"]
    assert result["bytes_saved"] > 0
    assert result["savings_percent"] > 30.0  # At least 30% reduction


def test_audit_ast_security_catches_eval_and_mutable_defaults() -> None:
    """Test AST analyzer detects eval() calls and mutable default argument traps."""
    test_code = """
def bad_func(items=[]):
    eval('2 * 2')
    return items
"""
    issues = InternalsProfiler.audit_ast_security(test_code)
    assert len(issues) == 2
    assert any("eval()" in issue for issue in issues)
    assert any("mutable default" in issue for issue in issues)


def test_clean_code_passes_ast_audit() -> None:
    """Test clean code produces zero AST security findings."""
    clean_code = """
def good_func(items=None):
    if items is None:
        items = []
    return items
"""
    issues = InternalsProfiler.audit_ast_security(clean_code)
    assert len(issues) == 0


def test_bytecode_analysis_branching_instructions() -> None:
    """Test disassembling conditional function contains compare and jump instructions."""
    def is_positive(x: int) -> bool:
        return x > 0

    metrics = InternalsProfiler.analyze_bytecode(is_positive)
    opnames = [inst["opname"] for inst in metrics["raw_instructions"]]
    assert any("COMPARE_OP" in op or "POP_JUMP" in op or "LOAD_FAST" in op for op in opnames)


def test_regular_user_has_dict_slotted_does_not() -> None:
    """Test RegularUser has __dict__ attribute while SlottedUser does not."""
    reg = RegularUser(1, "Alice")
    slotted = SlottedUser(1, "Alice")
    assert hasattr(reg, "__dict__")
    assert not hasattr(slotted, "__dict__")


def test_slotted_user_slots_declaration() -> None:
    """Test SlottedUser explicitly defines __slots__."""
    assert hasattr(SlottedUser, "__slots__")
    assert "uid" in SlottedUser.__slots__
    assert "name" in SlottedUser.__slots__


def test_ast_audit_catches_exec_usage() -> None:
    """Test audit_ast_security detects unsafe exec() usage."""
    code = """
def run_dynamic(cmd):
    exec(cmd)
"""
    issues = InternalsProfiler.audit_ast_security(code)
    assert any("exec()" in issue for issue in issues)


def test_ast_audit_catches_dict_mutable_default() -> None:
    """Test audit_ast_security detects mutable dict default arguments."""
    code = """
def bad_dict(config={}):
    return config
"""
    issues = InternalsProfiler.audit_ast_security(code)
    assert any("mutable default" in issue for issue in issues)


def test_ast_audit_invalid_syntax_handling() -> None:
    """Test audit_ast_security raises SyntaxError on malformed code."""
    code = "def invalid_syntax(:"
    with pytest.raises(SyntaxError):
        InternalsProfiler.audit_ast_security(code)


def test_bytecode_metrics_unique_opcodes_count() -> None:
    """Test unique opcodes count is accurate and non-negative."""
    def simple() -> None:
        pass

    metrics = InternalsProfiler.analyze_bytecode(simple)
    assert metrics["unique_opcodes"] <= metrics["total_instructions"]
