"""Unit tests for MemoryBenchmarker."""
from memory_benchmarker import MemoryBenchmarker


def test_measure_runtime():
    def dummy_sum(n: int) -> int:
        return sum(range(n))

    result, duration_ns = MemoryBenchmarker.measure_runtime_ns(dummy_sum, 1000)
    assert result == 499500
    assert duration_ns > 0

def test_measure_peak_memory():
    def allocate_list(n: int) -> list[int]:
        return list(range(n))

    result, peak_bytes = MemoryBenchmarker.measure_peak_memory_bytes(allocate_list, 10000)
    assert len(result) == 10000
    assert peak_bytes > 1000

def test_growth_rate_classification():
    # O(1) constant
    c_timings = [(100, 0.001), (1000, 0.0011), (10000, 0.0012)]
    assert MemoryBenchmarker.check_growth_rate(c_timings) == "O(1)"

    # O(N) linear
    lin_timings = [(100, 0.01), (500, 0.05), (1000, 0.10)]
    assert MemoryBenchmarker.check_growth_rate(lin_timings) == "O(N)"

    # O(N^2) quadratic
    quad_timings = [(100, 0.01), (1000, 1.0)]
    assert MemoryBenchmarker.check_growth_rate(quad_timings) == "O(N^2)"

def test_empty_function_runtime():
    def noop():
        pass
    _, duration = MemoryBenchmarker.measure_runtime_ns(noop)
    assert duration >= 0

def test_single_element_growth():
    timings = [(10, 0.005)]
    assert MemoryBenchmarker.check_growth_rate(timings) == "O(1)"

def test_zero_time_edge_case():
    timings = [(0, 0.0), (10, 0.0)]
    assert MemoryBenchmarker.check_growth_rate(timings) == "O(1)"
def test_benchmarker_empty_and_zero_inputs():
    # No-op function runtime benchmark
    res, ns = MemoryBenchmarker.measure_runtime_ns(lambda: None)
    assert res is None
    assert ns >= 0
    # Peak memory of minimal allocation
    res, mem = MemoryBenchmarker.measure_peak_memory_bytes(lambda: [0] * 100)
    assert len(res) == 100
    assert mem >= 0


def test_benchmarker_growth_rate_classification():
    # O(1) constant runtime function measurements
    growth_const = MemoryBenchmarker.check_growth_rate([(100, 0.001), (200, 0.001), (400, 0.001)])
    assert growth_const == "O(1)"
    # O(N) linear runtime measurements
    growth_lin = MemoryBenchmarker.check_growth_rate([(100, 0.001), (200, 0.002), (400, 0.004)])
    assert growth_lin == "O(N)"
    # O(N^2) quadratic runtime measurements
    growth_quad = MemoryBenchmarker.check_growth_rate([(100, 0.001), (200, 0.004), (400, 0.016)])
    assert growth_quad == "O(N^2)"

