"""Tests for Beam Search Decoder."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_beam_search_decoder import beam_search_decoder
except ImportError:
    from p01_beam_search_decoder import beam_search_decoder


def test_beam_search_decoder():
    init = [([1], -0.5)]
    # vocab size 3: token 0 (-1.0), token 1 (-0.1), token 2 (-2.0)
    vocab = [[-1.0, -0.1, -2.0]]
    beams = beam_search_decoder(init, vocab, beam_width=2)
    assert len(beams) == 2
    assert beams[0][0] == [1, 1]  # highest score -0.6
