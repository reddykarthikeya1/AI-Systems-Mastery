"""Memory-Efficient KV-Cache Block Manager Simulating vLLM PagedAttention & Radix Tree Routing.

Core Innovations:
-----------------
1. PagedAttention Memory Management:
   Standard transformer attention requires contiguous GPU memory allocations for the KV cache.
   Because generation lengths are unpredictable, systems pre-allocate maximum sequence lengths
   (e.g., 4096 tokens), wasting 60-80% of GPU memory to external and internal fragmentation.
   PagedAttention segments KV cache into fixed-size physical blocks (e.g. 16 tokens/block),
   mapped dynamically via a page table like virtual memory in operating systems.

2. Copy-on-Write (CoW) Parallel Sampling:
   When generating multiple completions for the same prompt (beam search or parallel sampling n > 1),
   child sequences share the prompt's physical blocks with incremented reference counts.
   A new physical block is only allocated when a branch diverges and appends its own tokens.

3. Watermark-based Eviction & LRU Prefix Caching:
   Maintains a high/low watermark buffer of free blocks. Least-recently-used completed prefix
   blocks are recycled when memory pressure exceeds thresholds.

4. Prefix-Aware Radix Tree Routing:
   Global router maps incoming prompt tokens through a Radix tree (trie) to find the worker node
   holding the longest common cached prefix, maximizing KV-cache reuse.
"""

from __future__ import annotations
import copy
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class PhysicalBlock:
    block_id: int
    ref_count: int = 0
    token_ids: List[int] = field(default_factory=list)
    last_accessed: float = field(default_factory=time.monotonic)


@dataclass
class SequenceContext:
    seq_id: str
    tokens: List[int]
    # Maps logical_block_idx -> physical_block_id
    block_table: List[int] = field(default_factory=list)


class BlockManager:
    """Manages physical GPU memory blocks with dynamic allocation, CoW, and LRU recycling."""

    def __init__(
        self,
        num_blocks: int = 64,
        block_size: int = 16,
        watermark_blocks: int = 4,
    ) -> None:
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.watermark_blocks = watermark_blocks

        # Physical memory pool
        self.blocks: Dict[int, PhysicalBlock] = {
            i: PhysicalBlock(block_id=i) for i in range(num_blocks)
        }
        self.free_block_ids: List[int] = list(range(num_blocks))
        # Cached reusable prefix blocks with ref_count == 0
        self.cached_prefix_blocks: Dict[Tuple[int, ...], int] = {}
        # Sequences: seq_id -> SequenceContext
        self.sequences: Dict[str, SequenceContext] = {}

    def get_num_free_blocks(self) -> int:
        return len(self.free_block_ids)

    def _evict_lru_cached_block(self) -> Optional[int]:
        """Evicts the least-recently accessed prefix block with ref_count == 0."""
        candidates = [
            (b.last_accessed, b.block_id, prefix)
            for prefix, b_id in self.cached_prefix_blocks.items()
            if (b := self.blocks[b_id]).ref_count == 0
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0])
        _, evicted_id, prefix = candidates[0]
        del self.cached_prefix_blocks[prefix]
        self.blocks[evicted_id].token_ids.clear()
        self.free_block_ids.append(evicted_id)
        return evicted_id

    def allocate_block(self) -> int:
        """Allocates a free physical block, evicting cold cached blocks if below watermark."""
        if len(self.free_block_ids) <= self.watermark_blocks:
            self._evict_lru_cached_block()

        if not self.free_block_ids:
            raise MemoryError("Out of physical KV-cache blocks (GPU OOM)")

        block_id = self.free_block_ids.pop()
        block = self.blocks[block_id]
        block.ref_count = 1
        block.token_ids.clear()
        block.last_accessed = time.monotonic()
        return block_id

    def free_block(self, block_id: int) -> None:
        """Decrements reference count; recycles when ref_count reaches 0."""
        block = self.blocks[block_id]
        block.ref_count = max(0, block.ref_count - 1)
        if block.ref_count == 0:
            if block.token_ids:
                # Retain in prefix cache for potential prompt reuse
                self.cached_prefix_blocks[tuple(block.token_ids)] = block_id
            else:
                self.free_block_ids.append(block_id)

    def register_sequence(self, seq_id: str, prompt_tokens: List[int]) -> SequenceContext:
        """Allocates and maps blocks for an incoming prompt sequence."""
        seq = SequenceContext(seq_id=seq_id, tokens=list(prompt_tokens))
        self.sequences[seq_id] = seq

        # Chunk into blocks
        for i in range(0, len(prompt_tokens), self.block_size):
            chunk = prompt_tokens[i : i + self.block_size]
            chunk_tuple = tuple(chunk)

            # Check if identical prefix chunk is already cached
            if chunk_tuple in self.cached_prefix_blocks:
                p_block_id = self.cached_prefix_blocks[chunk_tuple]
                p_block = self.blocks[p_block_id]
                p_block.ref_count += 1
                p_block.last_accessed = time.monotonic()
            else:
                p_block_id = self.allocate_block()
                p_block = self.blocks[p_block_id]
                p_block.token_ids = list(chunk)

            seq.block_table.append(p_block_id)

        return seq

    def append_token(self, seq_id: str, token_id: int) -> None:
        """Appends a newly sampled token using Copy-On-Write (CoW) semantics if block is shared."""
        seq = self.sequences[seq_id]
        seq.tokens.append(token_id)

        if not seq.block_table:
            p_block_id = self.allocate_block()
            seq.block_table.append(p_block_id)

        last_block_id = seq.block_table[-1]
        last_block = self.blocks[last_block_id]

        if len(last_block.token_ids) < self.block_size:
            # Block has available capacity in this page
            if last_block.ref_count > 1:
                # Copy-on-Write: block is shared with other branches
                new_block_id = self.allocate_block()
                new_block = self.blocks[new_block_id]
                new_block.token_ids = list(last_block.token_ids) + [token_id]

                # Decrement reference on parent and replace in table
                self.free_block(last_block_id)
                seq.block_table[-1] = new_block_id
            else:
                last_block.token_ids.append(token_id)
                last_block.last_accessed = time.monotonic()
        else:
            # Block is completely full: allocate new page
            new_block_id = self.allocate_block()
            new_block = self.blocks[new_block_id]
            new_block.token_ids.append(token_id)
            seq.block_table.append(new_block_id)

    def fork_sequence(self, parent_seq_id: str, child_seq_id: str) -> SequenceContext:
        """Creates a parallel branch sharing parent's physical blocks via reference counting."""
        parent = self.sequences[parent_seq_id]
        child = SequenceContext(
            seq_id=child_seq_id,
            tokens=list(parent.tokens),
            block_table=list(parent.block_table),
        )

        for block_id in child.block_table:
            self.blocks[block_id].ref_count += 1
            self.blocks[block_id].last_accessed = time.monotonic()

        self.sequences[child_seq_id] = child
        return child

    def free_sequence(self, seq_id: str) -> None:
        """Frees all resources associated with a finished sequence."""
        seq = self.sequences.pop(seq_id, None)
        if seq:
            for block_id in seq.block_table:
                self.free_block(block_id)


class RadixTreeNode:
    def __init__(self, token_seq: Tuple[int, ...] = ()) -> None:
        self.token_seq = token_seq
        self.children: Dict[int, RadixTreeNode] = {}  # first token of branch -> child node
        self.cached_on_workers: Set[str] = set()


class RadixTreeRouter:
    """Prefix-Aware Radix Tree Router to route requests to workers with cached KV-state."""

    def __init__(self, workers: List[str]) -> None:
        self.workers = workers
        self.root = RadixTreeNode()

    def record_cached_prefix(self, worker_id: str, tokens: List[int]) -> None:
        """Record that worker holds a given token sequence in its cache."""
        curr = self.root
        curr.cached_on_workers.add(worker_id)
        idx = 0
        while idx < len(tokens):
            first_tok = tokens[idx]
            if first_tok not in curr.children:
                new_node = RadixTreeNode(token_seq=tuple(tokens[idx:]))
                new_node.cached_on_workers.add(worker_id)
                curr.children[first_tok] = new_node
                return
            child = curr.children[first_tok]
            # Match common prefix
            c_seq = child.token_seq
            match_len = 0
            while (
                match_len < len(c_seq)
                and idx + match_len < len(tokens)
                and c_seq[match_len] == tokens[idx + match_len]
            ):
                match_len += 1

            if match_len == len(c_seq):
                child.cached_on_workers.add(worker_id)
                curr = child
                idx += match_len
            else:
                # Split child node
                split_node = RadixTreeNode(token_seq=c_seq[:match_len])
                split_node.cached_on_workers.update(child.cached_on_workers)
                split_node.cached_on_workers.add(worker_id)

                child.token_seq = c_seq[match_len:]
                split_node.children[child.token_seq[0]] = child

                rem_tokens = tokens[idx + match_len :]
                if rem_tokens:
                    rem_node = RadixTreeNode(token_seq=tuple(rem_tokens))
                    rem_node.cached_on_workers.add(worker_id)
                    split_node.children[rem_tokens[0]] = rem_node

                curr.children[first_tok] = split_node
                return

    def find_best_worker(self, prompt_tokens: List[int]) -> Tuple[str, int]:
        """Finds worker with the longest prefix match for incoming prompt tokens."""
        curr = self.root
        idx = 0
        best_worker = self.workers[0]
        max_matched_tokens = 0

        while idx < len(prompt_tokens):
            first_tok = prompt_tokens[idx]
            if first_tok not in curr.children:
                break
            child = curr.children[first_tok]
            c_seq = child.token_seq
            match_len = 0
            while (
                match_len < len(c_seq)
                and idx + match_len < len(prompt_tokens)
                and c_seq[match_len] == prompt_tokens[idx + match_len]
            ):
                match_len += 1

            if match_len > 0 and child.cached_on_workers:
                matched_total = idx + match_len
                if matched_total > max_matched_tokens:
                    max_matched_tokens = matched_total
                    best_worker = next(iter(child.cached_on_workers))

            if match_len == len(c_seq):
                curr = child
                idx += match_len
            else:
                break

        return best_worker, max_matched_tokens


class PagedAttentionSimulator:
    """End-to-end multi-worker LLM serving simulator with PagedAttention and Radix routing."""

    def __init__(self, worker_ids: List[str], num_blocks_per_worker: int = 64) -> None:
        self.workers: Dict[str, BlockManager] = {
            w: BlockManager(num_blocks=num_blocks_per_worker) for w in worker_ids
        }
        self.router = RadixTreeRouter(worker_ids)

    def route_and_allocate(self, seq_id: str, prompt_tokens: List[int]) -> Tuple[str, SequenceContext]:
        worker_id, matched_prefix_len = self.router.find_best_worker(prompt_tokens)
        manager = self.workers[worker_id]
        seq = manager.register_sequence(seq_id, prompt_tokens)
        self.router.record_cached_prefix(worker_id, prompt_tokens)
        return worker_id, seq
