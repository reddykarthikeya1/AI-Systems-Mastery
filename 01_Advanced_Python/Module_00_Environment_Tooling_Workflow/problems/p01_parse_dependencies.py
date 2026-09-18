"""Problem 01 — Parse pyproject.toml Dependencies

Target: Production-grade implementation

Example:
    >>> parse_dependencies(['fastapi>=0.100.0', 'pytest'])
    {'fastapi': '>=0.100.0', 'pytest': '*'}

Hints:
    Hint 1: Each spec line is either a bare package name or a name followed
        directly by a version operator and a version string, with no space
        guaranteed around either.
    Hint 2: Loop over the known operators (>=, <=, ==, !=, ~=, >, <) in an
        order where multi-character ones are checked before their
        single-character prefixes, and split on the first one found in the
        line.
    Hint 3: Strip whitespace from both the line and each split piece, lower
        the package name for the dict key, skip blank lines and lines
        starting with '#', and default to '*' for a line with no operator.
"""

from __future__ import annotations


def parse_dependencies(spec_lines: list[str]) -> dict[str, str]:
    raise NotImplementedError('Implement parse_dependencies')
