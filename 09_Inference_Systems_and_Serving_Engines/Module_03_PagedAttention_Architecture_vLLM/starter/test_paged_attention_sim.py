from __future__ import annotations

import pytest
from paged_attention_sim import PagedAttentionBlockManager


def test_block_allocation_and_paging():
    manager = PagedAttentionBlockManager(num_blocks=10, block_size=4)
    manager.allocate_request("req_1")

    # Append 4 tokens (fills block 0)
    for tok in [10, 11, 12, 13]:
        manager.append_token("req_1", tok)
    assert len(manager.block_tables["req_1"]) == 1

    # 5th token should allocate a second block
    manager.append_token("req_1", 14)
    assert len(manager.block_tables["req_1"]) == 2
    assert len(manager.free_blocks) == 8


def test_copy_on_write_forking():
    manager = PagedAttentionBlockManager(num_blocks=10, block_size=4)
    manager.allocate_request("parent")
    manager.append_token("parent", 1)
    manager.append_token("parent", 2)

    # Fork child request (e.g. beam search / parallel sampling)
    manager.fork_request(parent_id="parent", child_id="child")
    parent_block = manager.block_tables["parent"][0]
    child_block = manager.block_tables["child"][0]

    # Must point to the same physical block with ref_count 2
    assert parent_block == child_block
    assert manager.physical_blocks[parent_block].ref_count == 2

    # Append token to child -> triggers Copy-on-Write
    manager.append_token("child", 99)
    new_child_block = manager.block_tables["child"][0]
    assert new_child_block != parent_block
    assert manager.physical_blocks[parent_block].ref_count == 1
    assert manager.physical_blocks[new_child_block].ref_count == 1


def test_out_of_blocks_error():
    manager = PagedAttentionBlockManager(num_blocks=1, block_size=2)
    manager.allocate_request("req_1")
    manager.append_token("req_1", 1)
    manager.append_token("req_1", 2)

    with pytest.raises(MemoryError, match="Out of physical GPU blocks"):
        manager.append_token("req_1", 3)
