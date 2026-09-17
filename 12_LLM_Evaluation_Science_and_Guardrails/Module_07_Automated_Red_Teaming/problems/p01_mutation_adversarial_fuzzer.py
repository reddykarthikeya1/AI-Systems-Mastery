"""Problem 01 — Mutation Adversarial Fuzzer

Topic: 07 Automated Red Teaming
Target: Production-grade implementation

Generate adversarial prompt variants using character substitutions (leetspeak).

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def mutation_adversarial_fuzzer(prompt: str) -> list[str]:
    """Generate 2 adversarial mutated variants:
    1. leetspeak mutation: replace 'a'->'@', 'e'->'3', 'i'->'1', 'o'->'0'
    2. spaced mutation: join all characters with a space
    Returns list of [leetspeak_variant, spaced_variant].
    """
    raise NotImplementedError("Implement mutation_adversarial_fuzzer")
