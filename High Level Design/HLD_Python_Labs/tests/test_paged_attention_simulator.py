"""Tests for PagedAttention KV-Cache Manager & Radix Tree Routing (Workshop 12)."""
import pytest
from workshop_llm_serving.paged_attention_simulator import (
    BlockManager,
    RadixTreeRouter,
    PagedAttentionSimulator,
)


def test_block_allocation_and_page_mapping():
    # 4 blocks of size 4 tokens each
    bm = BlockManager(num_blocks=4, block_size=4, watermark_blocks=1)
    assert bm.get_num_free_blocks() == 4

    # Register sequence of 6 tokens -> requires ceil(6/4) = 2 blocks
    prompt = [101, 102, 103, 104, 105, 106]
    seq = bm.register_sequence("seq_1", prompt)

    assert len(seq.block_table) == 2
    assert bm.get_num_free_blocks() == 2


def test_copy_on_write_parallel_sampling():
    """Copy-on-Write (CoW) Invariant:

    1. Parent sequence has allocated blocks.
    2. Child sequence forks from parent; ref_count increments to 2.
    3. When child appends a token into a shared block, it must allocate a fresh block
       and leave the parent's block unchanged.
    """
    bm = BlockManager(num_blocks=8, block_size=4, watermark_blocks=1)
    parent = bm.register_sequence("parent_seq", [10, 20, 30])  # 3 tokens in 1 block
    p_block_id = parent.block_table[0]

    assert bm.blocks[p_block_id].ref_count == 1

    # Fork parallel sample
    child = bm.fork_sequence("parent_seq", "child_seq")
    assert child.block_table[0] == p_block_id
    assert bm.blocks[p_block_id].ref_count == 2

    # Child appends a new token (token 99)
    bm.append_token("child_seq", 99)

    # CoW occurred: child should now have a distinct physical block
    c_block_id = child.block_table[0]
    assert c_block_id != p_block_id
    assert bm.blocks[p_block_id].token_ids == [10, 20, 30]
    assert bm.blocks[c_block_id].token_ids == [10, 20, 30, 99]
    assert bm.blocks[p_block_id].ref_count == 1
    assert bm.blocks[c_block_id].ref_count == 1


def test_free_sequence():
    bm = BlockManager(num_blocks=4, block_size=4, watermark_blocks=1)
    seq = bm.register_sequence("s1", [1, 2, 3, 4])
    assert bm.get_num_free_blocks() == 3

    bm.free_sequence("s1")
    # Block is retained in cached_prefix_blocks with ref_count == 0
    assert bm.blocks[seq.block_table[0]].ref_count == 0


def test_radix_tree_routing():
    router = RadixTreeRouter(workers=["worker_gpu_0", "worker_gpu_1"])

    # Worker 0 caches prompt prefix [1, 2, 3, 4, 5]
    router.record_cached_prefix("worker_gpu_0", [1, 2, 3, 4, 5])
    # Worker 1 caches prompt prefix [10, 20, 30]
    router.record_cached_prefix("worker_gpu_1", [10, 20, 30])

    # Incoming query shares [1, 2, 3] prefix -> Must route to worker_gpu_0
    best_worker, matched_len = router.find_best_worker([1, 2, 3, 999])
    assert best_worker == "worker_gpu_0"
    assert matched_len == 3

    # Incoming query shares [10, 20, 30, 40] prefix -> Must route to worker_gpu_1
    best_worker2, matched_len2 = router.find_best_worker([10, 20, 30, 40])
    assert best_worker2 == "worker_gpu_1"
    assert matched_len2 == 3


def test_paged_attention_simulator_end_to_end():
    sim = PagedAttentionSimulator(worker_ids=["gpu_0", "gpu_1"], num_blocks_per_worker=16)
    worker, seq = sim.route_and_allocate("req_101", [10, 20, 30, 40])
    assert worker in ["gpu_0", "gpu_1"]
    assert len(seq.block_table) == 1
