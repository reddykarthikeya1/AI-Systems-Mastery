"""Tests for Bytecode Stack Depth Evaluator."""
from __future__ import annotations

import pytest
from p01_disassemble_stack_depth import calculate_net_stack_effect


def test_disassemble_stack_depth():
    ops = [('LOAD_FAST', 0), ('LOAD_CONST', 1), ('BINARY_OP', 0), ('RETURN_VALUE', 0)]
    assert calculate_net_stack_effect(ops) == 0
