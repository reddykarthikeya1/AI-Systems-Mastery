"""Broken benchmark calculating pass@k with math.comb overflow bug."""

class BrokenBenchmark:
    def pass_at_k(self, n, c, k):
        import math
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))


def reproduce_defect():
    print("Sweeping pass@k for n=5, c=2 across k in [1, 3, 5, 10]...")
    bench = BrokenBenchmark()

    print("Expected: every k value returns a defined score, even when k > n")
    for k in [1, 3, 5, 10]:
        try:
            val = bench.pass_at_k(n=5, c=2, k=k)
            print(f"Actual: pass@{k} (n=5, c=2) = {val:.4f}")
        except ZeroDivisionError as e:
            print(f"Actual: pass@{k} (n=5, c=2) crashed: {type(e).__name__}: {e}")


if __name__ == "__main__":
    reproduce_defect()
