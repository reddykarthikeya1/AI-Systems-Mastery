"""Tests for Recursive Token Splitter."""
from __future__ import annotations

import pytest
from p01_recursive_token_splitter import recursive_token_splitter


def test_recursive_token_splitter():
    text = "one two three four five six seven eight"
    chunks = recursive_token_splitter(text, max_chunk_words=4, overlap_words=1)
    assert chunks[0] == "one two three four"
    assert chunks[1] == "four five six seven"
