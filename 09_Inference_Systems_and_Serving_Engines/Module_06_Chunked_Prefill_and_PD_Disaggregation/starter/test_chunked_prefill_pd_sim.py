from __future__ import annotations

from chunked_prefill_pd_sim import ChunkedPrefillSimulator


def test_chunked_prefill_bounds_latency():
    # Prompt of 2,048 tokens with chunk size 512 -> exactly 4 chunks
    sim = ChunkedPrefillSimulator(chunk_size=512, ms_per_token_prefill=0.04)
    res = sim.schedule_prompt(prompt_tokens=2048, decode_step_overhead_ms=10.0)

    assert res.total_chunks == 4
    # Each chunk prefill is 512 * 0.04 = 20.48 ms + 10ms decode = ~30.48 ms
    assert res.max_step_latency_ms < 35.0
    for latency in res.step_latencies_ms:
        assert latency < 35.0


def test_partial_chunk_division():
    sim = ChunkedPrefillSimulator(chunk_size=500)
    res = sim.schedule_prompt(prompt_tokens=1200)
    # 500 + 500 + 200 = 3 chunks
    assert res.total_chunks == 3
