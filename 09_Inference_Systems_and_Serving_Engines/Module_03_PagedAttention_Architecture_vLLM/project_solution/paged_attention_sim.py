from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class PhysicalBlock:
    block_id: int
    ref_count: int = 1
    tokens: list[int] = dataclasses.field(default_factory=list)


class PagedAttentionBlockManager:
    """Simulates vLLM PagedAttention Physical Block Allocation and Copy-on-Write."""

    def __init__(self, num_blocks: int, block_size: int = 16):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.free_blocks: list[int] = list(range(num_blocks))
        self.physical_blocks: dict[int, PhysicalBlock] = {}
        self.block_tables: dict[str, list[int]] = {}

    def allocate_request(self, request_id: str) -> None:
        if not self.free_blocks:
            raise MemoryError("Out of physical GPU blocks!")
        block_id = self.free_blocks.pop(0)
        self.physical_blocks[block_id] = PhysicalBlock(block_id=block_id)
        self.block_tables[request_id] = [block_id]

    def append_token(self, request_id: str, token_id: int) -> None:
        table = self.block_tables[request_id]
        last_block_id = table[-1]
        last_block = self.physical_blocks[last_block_id]

        # Check if Copy-on-Write is required
        if last_block.ref_count > 1:
            if not self.free_blocks:
                raise MemoryError("Out of physical GPU blocks on CoW!")
            new_block_id = self.free_blocks.pop(0)
            # Copy contents
            self.physical_blocks[new_block_id] = PhysicalBlock(
                block_id=new_block_id,
                ref_count=1,
                tokens=list(last_block.tokens),
            )
            last_block.ref_count -= 1
            table[-1] = new_block_id
            last_block = self.physical_blocks[new_block_id]

        # Check if block is full
        if len(last_block.tokens) < self.block_size:
            last_block.tokens.append(token_id)
        else:
            # Need a new physical block
            if not self.free_blocks:
                raise MemoryError("Out of physical GPU blocks!")
            new_block_id = self.free_blocks.pop(0)
            self.physical_blocks[new_block_id] = PhysicalBlock(
                block_id=new_block_id,
                ref_count=1,
                tokens=[token_id],
            )
            table.append(new_block_id)

    def fork_request(self, parent_id: str, child_id: str) -> None:
        """Forks request for parallel sampling using Copy-on-Write."""
        parent_table = self.block_tables[parent_id]
        # Child shares all physical blocks initially
        for block_id in parent_table:
            self.physical_blocks[block_id].ref_count += 1
        self.block_tables[child_id] = list(parent_table)

    def free_request(self, request_id: str) -> None:
        table = self.block_tables.pop(request_id, [])
        for block_id in table:
            block = self.physical_blocks[block_id]
            block.ref_count -= 1
            if block.ref_count == 0:
                del self.physical_blocks[block_id]
                self.free_blocks.append(block_id)
