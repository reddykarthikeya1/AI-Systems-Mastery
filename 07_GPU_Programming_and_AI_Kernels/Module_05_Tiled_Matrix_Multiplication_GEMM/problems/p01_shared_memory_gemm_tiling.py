"""Problem 01 — Shared Memory Gemm Tiling

Topic: 05 Tiled Matrix Multiplication GEMM
Target: Production-grade implementation

Compute 2x2 matrix product using shared memory block tiles.

Example:
    >>> shared_memory_gemm_tiling([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]])
    [[19.0, 22.0], [43.0, 50.0]]

Hints:
    Hint 1: Tiling is an implementation detail for how a real GPU kernel
        would stage data through shared memory — here it just needs to
        reproduce the same output as a plain dense matrix multiply.
    Hint 2: For each output cell `C[i][j]`, take the dot product of row `i`
        of `A` with column `j` of `B`: `sum(A[i][k] * B[k][j] for k in
        range(n))`.
    Hint 3: Round each accumulated dot product to exactly 4 decimal places
        before storing it, and size the output from `len(A)` so the
        function isn't hard-coded to 2x2 even though the docstring's
        example uses that size.
"""

from __future__ import annotations


def shared_memory_gemm_tiling(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Compute C = A x B for 2x2 matrices rounded to 4 decimals."""
    raise NotImplementedError("Implement shared_memory_gemm_tiling")
