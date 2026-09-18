"""Tests for Ast Sandbox Validator."""
from __future__ import annotations

import pytest
from p01_ast_sandbox_validator import ast_sandbox_validator


def test_ast_sandbox_validator():
    safe_code = "x = 10 + 20\nprint(x)"
    ok, err = ast_sandbox_validator(safe_code)
    assert ok is True and err is None
    
    evil_code = "import os\nos.system('rm -rf /')"
    ok2, err2 = ast_sandbox_validator(evil_code)
    assert ok2 is False and "os" in err2
