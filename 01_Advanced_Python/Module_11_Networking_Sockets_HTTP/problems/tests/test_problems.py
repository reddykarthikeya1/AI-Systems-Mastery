"""Tests for HTTP Chunked Transfer Decoder."""
from __future__ import annotations

import pytest
from p01_parse_chunked_body import parse_chunked_body


def test_parse_chunked_body():
    stream = b'4\r\nWiki\r\n5\r\npedia\r\n0\r\n\r\n'
    assert parse_chunked_body(stream) == b'Wikipedia'
    assert parse_chunked_body(b'0\r\n\r\n') == b''
