"""Tests for Contextual Exception Chaining."""
from __future__ import annotations

import pytest
from p01_chain_exception_context import format_exception_chain


def test_chain_exception_context():
    try:
        try:
            raise ValueError('inner failure')
        except ValueError as err:
            raise RuntimeError('outer failure') from err
    except RuntimeError as top:
        c = format_exception_chain(top)
        assert len(c) == 2
        assert 'RuntimeError: outer failure' in c[0]
        assert 'ValueError: inner failure' in c[1]
