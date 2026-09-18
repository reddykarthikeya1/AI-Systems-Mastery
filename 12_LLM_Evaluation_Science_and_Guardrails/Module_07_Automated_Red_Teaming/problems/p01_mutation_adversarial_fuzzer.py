"""Problem 01 — Mutation Adversarial Fuzzer

Topic: 07 Automated Red Teaming
Target: Production-grade implementation

Generate adversarial prompt variants using character substitutions (leetspeak).

Example:
    >>> mutation_adversarial_fuzzer('hello')
    ['h3ll0', 'h e l l o']

Hints:
    Hint 1: The two mutations are independent transformations of the same
        original string, not chained onto each other — the spaced variant
        should still contain the original letters, not the leetspeak
        ones.
    Hint 2: Build the leetspeak variant with a character-by-character
        substitution through a lookup dict (a/e/i/o -> @/3/1/0), and build
        the spaced variant separately with " ".join(prompt) on the
        untouched original string.
    Hint 3: The leetspeak map needs both cases of each vowel (lowercase
        and uppercase should both get replaced, e.g. 'A' and 'a' both
        become '@') so mixed-case prompts mutate consistently, and any
        character not in the map (consonants, punctuation, spaces) must
        pass through unchanged.
"""

from __future__ import annotations


def mutation_adversarial_fuzzer(prompt: str) -> list[str]:
    """Generate 2 adversarial mutated variants:
    1. leetspeak mutation: replace 'a'->'@', 'e'->'3', 'i'->'1', 'o'->'0'
    2. spaced mutation: join all characters with a space
    Returns list of [leetspeak_variant, spaced_variant].
    """
    raise NotImplementedError("Implement mutation_adversarial_fuzzer")
