# Debug Lab: PagedAttention Copy-on-Write Fork Corrupts the Parent Sequence
# Course 09 - Module 03 PagedAttention Architecture (vLLM)

BLOCK_SIZE = 4


class PhysicalBlock:
    def __init__(self, block_id):
        self.block_id = block_id
        self.tokens = []
        self.refcount = 1


class PagedSequence:
    """A logical sequence backed by a page table of shared physical blocks,
    mirroring vLLM's PagedAttention block table."""

    def __init__(self, name, block_pool):
        self.name = name
        self.block_pool = block_pool
        self.block_table = []  # list of PhysicalBlock, shared across forks

    def append_token(self, token):
        if not self.block_table or len(self.block_table[-1].tokens) == BLOCK_SIZE:
            new_block = PhysicalBlock(len(self.block_pool))
            self.block_pool.append(new_block)
            self.block_table.append(new_block)
        last_block = self.block_table[-1]
        # Beam search / parallel sampling forks share trailing blocks via COW.
        # Writing into a block with refcount > 1 must copy it first so the
        # other owner's tokens are untouched.
        last_block.tokens.append(token)

    def fork(self, new_name):
        """Fork this sequence (e.g. for parallel sampling): the child starts
        with the same block table, sharing every physical block."""
        child = PagedSequence(new_name, self.block_pool)
        child.block_table = list(self.block_table)
        for block in child.block_table:
            block.refcount += 1
        return child

    def text(self):
        return [tok for block in self.block_table for tok in block.tokens]


if __name__ == "__main__":
    pool = []
    parent = PagedSequence("parent", pool)
    for tok in ["The", "capital", "of"]:
        parent.append_token(tok)  # 3 tokens in block 0 (capacity 4)

    child = parent.fork("beam_2")  # shares block 0, refcount now 2

    print(f"Before divergence, parent tokens: {parent.text()}")
    print(f"Before divergence, child tokens:  {child.text()}")

    # Parent and child now generate DIFFERENT next tokens (this is the whole
    # point of parallel sampling / beam search).
    parent.append_token("France")
    child.append_token("Germany")

    print(f"\nExpected: parent should read 'The capital of France' and child "
          f"should independently read 'The capital of Germany'.")
    print(f"Actual parent tokens: {parent.text()}")
    print(f"Actual child tokens:  {child.text()}")
