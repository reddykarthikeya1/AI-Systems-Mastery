"""Unit tests for Sandboxed Code Executor."""

from __future__ import annotations

import pytest
from sandboxed_executor import SandboxedExecutor


@pytest.fixture
def executor() -> SandboxedExecutor:
    return SandboxedExecutor(timeout_sec=1.0)


def test_safe_code_execution(executor: SandboxedExecutor):
    code = "vals = [x * 2 for x in range(5)]\nprint(vals)"
    res = executor.execute(code)
    assert res.exit_code == 0
    assert "[0, 2, 4, 6, 8]" in res.stdout
    assert len(res.security_violations) == 0


def test_block_forbidden_modules(executor: SandboxedExecutor):
    code = "import os\nos.system('echo hacked')"
    res = executor.execute(code)
    assert res.exit_code != 0
    assert any("Forbidden module import: 'os'" in v for v in res.security_violations)


def test_block_reflection_exploit(executor: SandboxedExecutor):
    code = "subs = ().__class__.__base__.__subclasses__()"
    res = executor.execute(code)
    assert res.exit_code != 0
    assert any("__subclasses__" in v for v in res.security_violations)


def test_timeout_enforcement(executor: SandboxedExecutor):
    code = "import time\ntime.sleep(2.5)"
    res = executor.execute(code)
    assert res.is_timeout is True
    assert "timed out" in res.stderr


def test_secret_sanitization(executor: SandboxedExecutor):
    code = "print('Using key sk-1234567890abcdef1234567890 to connect')"
    res = executor.execute(code)
    assert res.exit_code == 0
    assert "sk-1234567890abcdef1234567890" not in res.stdout
    assert "[REDACTED_SECRET]" in res.stdout
