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


def test_double_free_protection():
    bm = BlockManager(num_blocks=4, block_size=4, watermark_blocks=1)
    b_id = bm.allocate_block()
    assert bm.blocks[b_id].ref_count == 1

    # First free -> ref_count drops to 0, recycled
    bm.free_block(b_id)
    assert bm.blocks[b_id].ref_count == 0

    # Second free on already freed block -> must raise ValueError without corrupting free list
    with pytest.raises(ValueError, match="Double-free detected"):
        bm.free_block(b_id)

    # Verify free_block_ids has no duplicate entries
    assert bm.free_block_ids.count(b_id) == 1


def test_parallel_sampling_n_branches_cow():
    """Verify n > 1 parallel sampling forks sharing prefix blocks with independent CoW divergence."""
    bm = BlockManager(num_blocks=16, block_size=4, watermark_blocks=1)

    # Prompt: 8 tokens -> 2 full blocks [10, 11, 12, 13] and [14, 15, 16, 17]
    prompt = [10, 11, 12, 13, 14, 15, 16, 17]
    parent = bm.register_sequence("prompt_parent", prompt)
    b0, b1 = parent.block_table[0], parent.block_table[1]
    assert bm.blocks[b0].ref_count == 1
    assert bm.blocks[b1].ref_count == 1

    # Fork 3 children for parallel sampling (n = 3)
    c1 = bm.fork_sequence("prompt_parent", "sample_1")
    c2 = bm.fork_sequence("prompt_parent", "sample_2")
    c3 = bm.fork_sequence("prompt_parent", "sample_3")

    # All 4 sequences share the physical blocks
    assert bm.blocks[b0].ref_count == 4
    assert bm.blocks[b1].ref_count == 4

    # Sample 1 generates token 100 -> b1 is full, so it allocates a new block for the next page
    bm.append_token("sample_1", 100)
    assert len(c1.block_table) == 3
    assert c1.block_table[0] == b0
    assert c1.block_table[1] == b1
    # Sample 1's new block
    new_b_c1 = c1.block_table[2]
    assert bm.blocks[new_b_c1].token_ids == [100]

    # Shared prefix blocks remain referenced by other branches
    assert bm.blocks[b0].ref_count == 4
    assert bm.blocks[b1].ref_count == 4

    # Sample 2 generates token 200 -> allocates its own distinct third block
    bm.append_token("sample_2", 200)
    assert len(c2.block_table) == 3
    new_b_c2 = c2.block_table[2]
    assert new_b_c2 != new_b_c1
    assert bm.blocks[new_b_c2].token_ids == [200]


def test_partial_final_block_handling():
    """Verify handling of sequences whose prompt length is not an exact multiple of block_size."""
    bm = BlockManager(num_blocks=8, block_size=4, watermark_blocks=1)

    # 6 tokens -> Block 0: 4 tokens (full), Block 1: 2 tokens (partial: [5, 6])
    seq = bm.register_sequence("partial_seq", [1, 2, 3, 4, 5, 6])
    assert len(seq.block_table) == 2
    b0, b1 = seq.block_table

    assert bm.blocks[b0].token_ids == [1, 2, 3, 4]
    assert bm.blocks[b1].token_ids == [5, 6]

    # Append 3rd token to partial block
    bm.append_token("partial_seq", 7)
    assert len(seq.block_table) == 2
    assert bm.blocks[b1].token_ids == [5, 6, 7]

    # Append 4th token -> completes block 1
    bm.append_token("partial_seq", 8)
    assert len(seq.block_table) == 2
    assert bm.blocks[b1].token_ids == [5, 6, 7, 8]

    # Append 5th token -> block 1 is full, allocates new block 2
    bm.append_token("partial_seq", 9)
    assert len(seq.block_table) == 3
    b2 = seq.block_table[2]
    assert bm.blocks[b2].token_ids == [9]


def test_watermark_lru_cache_eviction():
    """Verify that cold cached prefix blocks are evicted via LRU when free blocks drop below watermark."""
    # 4 blocks, block_size=2, watermark=2
    bm = BlockManager(num_blocks=4, block_size=2, watermark_blocks=2)

    # Sequence 1 uses 1 full block [1, 2]
    s1 = bm.register_sequence("s1", [1, 2])
    b1_id = s1.block_table[0]
    bm.free_sequence("s1")
    # b1 is now cached prefix with ref_count 0
    assert (1, 2) in bm.cached_prefix_blocks
    assert bm.get_num_free_blocks() == 3

    # Sequence 2 uses 1 full block [3, 4]
    s2 = bm.register_sequence("s2", [3, 4])
    b2_id = s2.block_table[0]
    bm.free_sequence("s2")
    assert (3, 4) in bm.cached_prefix_blocks
    assert bm.get_num_free_blocks() == 2  # At watermark threshold (2)

    # Now allocate a new sequence [5, 6] -> free blocks (2) <= watermark (2), so LRU cached block is evicted!
    s3 = bm.register_sequence("s3", [5, 6])
    assert s3 is not None
    # (1, 2) was the oldest, so it was evicted
    assert (1, 2) not in bm.cached_prefix_blocks


def test_sequence_preemption_on_memory_exhaustion():
    """Verify that active sequences can be preempted to reclaim blocks without corrupting state."""
    bm = BlockManager(num_blocks=2, block_size=2, watermark_blocks=0)

    # Sequence A takes block 0
    seq_a = bm.register_sequence("seq_a", [10, 20])
    # Sequence B takes block 1
    seq_b = bm.register_sequence("seq_b", [30, 40])
    assert bm.get_num_free_blocks() == 0

    # Allocating another block now would raise OOM
    with pytest.raises(MemoryError, match="GPU OOM"):
        bm.allocate_block()

    # Preempt Sequence A to reclaim blocks
    freed = bm.preempt_sequence("seq_a")
    assert len(freed) == 1
    assert seq_a.is_preempted is True
    assert len(seq_a.block_table) == 0

    # Sequence C can now allocate the reclaimed block
    seq_c = bm.register_sequence("seq_c", [50, 60])
    assert len(seq_c.block_table) == 1
    assert seq_c.block_table[0] in freed


def test_re_register_sequence_releases_old_blocks():
    """Register sequence s1 with 8 tokens (2 blocks). Overwrite s1 with a new sequence of 4 tokens (1 block).
    Verify that previous blocks are freed and bm.get_num_free_blocks() does not leak blocks."""
    # 8 blocks total, block_size = 4, watermark = 0
    bm = BlockManager(num_blocks=8, block_size=4, watermark_blocks=0)
    assert bm.get_num_free_blocks() == 8

    # 1. Register s1 with 8 tokens -> 2 full blocks
    s1 = bm.register_sequence("s1", [1, 2, 3, 4, 5, 6, 7, 8])
    assert len(s1.block_table) == 2
    old_b0, old_b1 = s1.block_table[0], s1.block_table[1]
    assert bm.blocks[old_b0].ref_count == 1
    assert bm.blocks[old_b1].ref_count == 1
    assert bm.get_num_free_blocks() == 6

    # 2. Overwrite s1 with new sequence of 4 tokens (1 block)
    # The previous 2 blocks must be freed before allocating the new sequence
    s1_new = bm.register_sequence("s1", [10, 20, 30, 40])
    assert len(s1_new.block_table) == 1
    new_b = s1_new.block_table[0]

    # Verify that previous blocks were released (ref_count == 0) and not leaked
    assert bm.blocks[old_b0].ref_count == 0
    assert bm.blocks[old_b1].ref_count == 0
    assert bm.blocks[new_b].ref_count == 1

    # Overwrite again with partial block tokens (e.g. 2 tokens)
    s1_partial = bm.register_sequence("s1", [100, 101])
    assert len(s1_partial.block_table) == 1
    partial_b = s1_partial.block_table[0]

    # new_b (full block) ref_count dropped to 0
    assert bm.blocks[new_b].ref_count == 0

    # Finally free s1
    bm.free_sequence("s1")
    # partial_b had < block_size tokens, so upon freeing it returns directly to free_block_ids
    assert partial_b in bm.free_block_ids

    # All blocks ever allocated for s1 have ref_count == 0 (zero leaked block references)
    for b_id in [old_b0, old_b1, new_b, partial_b]:
        assert bm.blocks[b_id].ref_count == 0


def test_fork_sequence_existing_child_cleaned_up():
    """Fork to an already existing sequence ID and verify no leaked block references."""
    bm = BlockManager(num_blocks=8, block_size=4, watermark_blocks=1)

    # Register parent sequence
    parent = bm.register_sequence("parent_seq", [1, 2, 3, 4])
    parent_b = parent.block_table[0]
    assert bm.blocks[parent_b].ref_count == 1

    # Register an initial child sequence that holds a distinct block
    initial_child = bm.register_sequence("child_seq", [10, 20, 30, 40])
    child_old_b = initial_child.block_table[0]
    assert bm.blocks[child_old_b].ref_count == 1

    # Fork parent to child_seq (overwriting existing child_seq)
    forked_child = bm.fork_sequence("parent_seq", "child_seq")

    # The old block held by child_seq must be cleanly freed (ref_count == 0)
    assert bm.blocks[child_old_b].ref_count == 0

    # The forked child now shares the parent block (ref_count == 2)
    assert forked_child.block_table[0] == parent_b
    assert bm.blocks[parent_b].ref_count == 2

    # Clean up both sequences
    bm.free_sequence("child_seq")
    assert bm.blocks[parent_b].ref_count == 1
    bm.free_sequence("parent_seq")
    assert bm.blocks[parent_b].ref_count == 0


