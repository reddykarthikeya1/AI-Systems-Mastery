"""Broken benchmark calculating pass@k with math.comb overflow bug."""

class BrokenBenchmark:
    def pass_at_k(self, n, c, k):
        # BUG: Fails when n - c < k
        import math
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))
