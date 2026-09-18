# Debug Lab: KV Cache Evictor Frees Blocks Still Held by an In-Flight Request
# Course 09 - Module 02 KV Cache Memory Management

class KVCacheManager:
    """Simulates a fixed-size pool of KV-cache blocks shared across requests.
    Each block is identified by an int id. `refcount[block_id]` tracks how many
    in-flight requests are currently reading that block."""

    def __init__(self, num_blocks):
        self.free_blocks = list(range(num_blocks))
        self.refcount = {i: 0 for i in range(num_blocks)}
        self.lru_order = []  # oldest-used block ids at the front

    def allocate(self, request_id, n_blocks):
        allocated = []
        for _ in range(n_blocks):
            if not self.free_blocks:
                self._evict_one()
            block_id = self.free_blocks.pop(0)
            self.refcount[block_id] += 1
            allocated.append(block_id)
        self.lru_order = [b for b in self.lru_order if b not in allocated] + allocated
        return allocated

    def _evict_one(self):
        # Reclaim the least-recently-used block to make room for a new
        # allocation when the pool is exhausted.
        victim = self.lru_order.pop(0)
        self.free_blocks.append(victim)

    def release(self, block_ids):
        for block_id in block_ids:
            self.refcount[block_id] -= 1


if __name__ == "__main__":
    NUM_BLOCKS = 4
    mgr = KVCacheManager(NUM_BLOCKS)

    # Request A holds all 4 blocks for a long-running generation (still decoding).
    req_a_blocks = mgr.allocate("req_a", 4)
    mgr.lru_order = list(req_a_blocks)  # req_a's blocks are the current LRU chain

    # Request B arrives needing 1 more block while the pool is full and req_a
    # is still actively generating (its blocks must not be touched).
    req_b_blocks = mgr.allocate("req_b", 1)

    stolen = [b for b in req_b_blocks if b in req_a_blocks]

    print(f"req_a still in-flight, holds blocks: {req_a_blocks}")
    print(f"req_b newly allocated blocks:       {req_b_blocks}")
    print(f"Expected: eviction should never hand out a block from req_a while "
          f"refcount > 0 (req_a is still decoding).")
    print(f"Actual: block(s) reused from req_a's live set: {stolen}")
    print(f"req_a block refcounts after req_b's allocation: "
          f"{ {b: mgr.refcount[b] for b in req_a_blocks} }")
