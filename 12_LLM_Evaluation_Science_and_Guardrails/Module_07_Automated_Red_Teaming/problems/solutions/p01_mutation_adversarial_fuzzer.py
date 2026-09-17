"""Reference Solution — Problem 01: Mutation Adversarial Fuzzer

Topic: 07 Automated Red Teaming
"""

from __future__ import annotations


def mutation_adversarial_fuzzer(prompt: str) -> list[str]:
    leet_map = {'a': '@', 'A': '@', 'e': '3', 'E': '3', 'i': '1', 'I': '1', 'o': '0', 'O': '0'}
    v1 = "".join(leet_map.get(c, c) for c in prompt)
    v2 = " ".join(prompt)
    return [v1, v2]
