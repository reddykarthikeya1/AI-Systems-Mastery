"""Tests for Mutation Adversarial Fuzzer."""
from __future__ import annotations

import pytest
from p01_mutation_adversarial_fuzzer import mutation_adversarial_fuzzer


def test_mutation_adversarial_fuzzer():
    muts = mutation_adversarial_fuzzer("hello")
    assert muts[0] == "h3ll0"
    assert muts[1] == "h e l l o"
