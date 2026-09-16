#!/usr/bin/env python3
"""Micro-benchmark suite for Course 07 GPU & Kernel Engines."""
import time
import numpy as np

def benchmark():
    print("=" * 60)
    print("COURSE 07 GPU KERNEL MICRO-BENCHMARK SUITE")
    print("=" * 60)

    # 1. Tiled GEMM Benchmark
    from Module_05_Tiled_Matrix_Multiplication_GEMM.project_solution.tiled_gemm_sim import tiled_gemm_2d
    a = np.random.randn(64, 64)
    b = np.random.randn(64, 64)
    t0 = time.perf_counter()
    c, g_reads, s_reads = tiled_gemm_2d(a, b, tile_size=16)
    t1 = time.perf_counter()
    print(f"Tiled GEMM (64x64): {(t1 - t0)*1e3:.2f} ms | DRAM Reads: {g_reads} | SRAM Reads: {s_reads}")

    # 2. FlashAttention Benchmark
    from Module_08_FlashAttention_1_and_2_Internals.project_solution.flash_attention_engine import flash_attention_forward
    q = np.random.randn(128, 32)
    k = np.random.randn(128, 32)
    v = np.random.randn(128, 32)
    t0 = time.perf_counter()
    o, fa_reads, fa_writes = flash_attention_forward(q, k, v, block_r=32, block_c=32)
    t1 = time.perf_counter()
    print(f"FlashAttention (N=128, d=32): {(t1 - t0)*1e3:.2f} ms | HBM Reads: {fa_reads} | Writes: {fa_writes}")

    # 3. Fused RMSNorm Benchmark
    from Module_07_Fused_Activations_and_Normalization.project_solution.fused_norm_and_activations import fused_rmsnorm
    x = np.random.randn(8, 256, 128)
    w = np.ones(128)
    t0 = time.perf_counter()
    _ = fused_rmsnorm(x, w)
    t1 = time.perf_counter()
    print(f"Fused RMSNorm (8x256x128): {(t1 - t0)*1e3:.2f} ms")

    print("=" * 60)
    print("ALL BENCHMARKS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    benchmark()
