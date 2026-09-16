"""Module 22: Distributed LLM Serving & PagedAttention Continuous Batching Engine.

Reference implementation of PagedAttention virtual block memory management,
iteration-level continuous batching, sequence preemption, and speculative decoding verification.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import enum
from collections import deque
from dataclasses import dataclass, field

# ============================================================================
# 1. PagedAttention Block Table & GPU Memory Allocator
# ============================================================================

class RequestStatus(enum.StrEnum):
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    PREEMPTED = "PREEMPTED"


@dataclass
class PhysicalBlock:
    block_id: int
    ref_count: int = 0


class PagedAttentionBlockManager:
    """Manages virtual-to-physical block mapping for Key-Value (KV) cache pages."""

    def __init__(self, num_gpu_blocks: int, block_size: int = 16) -> None:
        self.num_gpu_blocks = num_gpu_blocks
        self.block_size = block_size

        # Free list of physical blocks
        self.free_block_pool: deque[int] = deque(range(num_gpu_blocks))

        # Block table mapping: req_id -> List[physical_block_id]
        self.block_tables: dict[str, list[int]] = {}

    def num_free_blocks(self) -> int:
        return len(self.free_block_pool)

    def allocate_next_block(self, req_id: str) -> int | None:
        """Allocates a free physical block from the GPU memory pool to a sequence."""
        if not self.free_block_pool:
            return None  # Out of GPU memory (triggers preemption)

        block_id = self.free_block_pool.popleft()
        if req_id not in self.block_tables:
            self.block_tables[req_id] = []
        self.block_tables[req_id].append(block_id)
        return block_id

    def ensure_blocks_for_length(self, req_id: str, total_tokens: int) -> bool:
        """Ensures enough physical blocks are allocated to hold the specified token count."""
        needed_blocks = (total_tokens + self.block_size - 1) // self.block_size
        current_blocks = len(self.block_tables.get(req_id, []))

        while current_blocks < needed_blocks:
            new_block = self.allocate_next_block(req_id)
            if new_block is None:
                return False  # Failed to allocate needed block
            current_blocks += 1

        return True

    def free_blocks(self, req_id: str) -> None:
        """Returns all physical blocks allocated to a sequence back to the free pool."""
        allocated = self.block_tables.pop(req_id, [])
        for blk in allocated:
            self.free_block_pool.append(blk)

    def get_memory_utilization(self) -> float:
        """Returns the fraction of GPU KV blocks currently allocated."""
        used = self.num_gpu_blocks - len(self.free_block_pool)
        return used / float(self.num_gpu_blocks)


# ============================================================================
# 2. Continuous Batching Scheduler
# ============================================================================

@dataclass
class InferenceRequest:
    req_id: str
    prompt: str
    prompt_tokens: list[str]
    max_new_tokens: int
    generated_tokens: list[str] = field(default_factory=list)
    status: RequestStatus = RequestStatus.WAITING
    arrival_step: int = 0
    finish_step: int | None = None

    @property
    def total_tokens(self) -> int:
        return len(self.prompt_tokens) + len(self.generated_tokens)


class ContinuousBatchScheduler:
    """Iteration-level continuous batching scheduler with zero tail-latency idling."""

    def __init__(
        self,
        block_manager: PagedAttentionBlockManager,
        max_batch_size: int = 8,
    ) -> None:
        self.block_manager = block_manager
        self.max_batch_size = max_batch_size

        self.waiting_queue: deque[InferenceRequest] = deque()
        self.running_batch: list[InferenceRequest] = []
        self.finished_requests: list[InferenceRequest] = []
        self.current_step: int = 0

    def add_request(self, req: InferenceRequest) -> None:
        req.arrival_step = self.current_step
        req.status = RequestStatus.WAITING
        self.waiting_queue.append(req)

    def step(self) -> dict[str, str]:
        """Executes one continuous batch decoding step across all running sequences.

        Returns: Mapping of req_id -> newly_generated_token
        """
        self.current_step += 1
        new_tokens: dict[str, str] = {}

        # 1. Admit waiting requests if capacity allows (Prefill stage)
        while self.waiting_queue and len(self.running_batch) < self.max_batch_size:
            candidate = self.waiting_queue[0]
            # Check if block manager can accommodate candidate's prompt
            needed_initial_tokens = candidate.total_tokens + 1
            needed_blocks = (needed_initial_tokens + self.block_manager.block_size - 1) // self.block_manager.block_size

            if self.block_manager.num_free_blocks() >= needed_blocks:
                req = self.waiting_queue.popleft()
                self.block_manager.ensure_blocks_for_length(req.req_id, req.total_tokens)
                req.status = RequestStatus.RUNNING
                self.running_batch.append(req)
            else:
                break  # Not enough memory to admit new prompt

        # 2. Autoregressive token generation step (Decode stage)
        retained_batch: list[InferenceRequest] = []

        for req in self.running_batch:
            # Check if sequence needs a new block for the next token
            next_total_tokens = req.total_tokens + 1
            success = self.block_manager.ensure_blocks_for_length(req.req_id, next_total_tokens)

            if not success:
                # GPU Out of Memory: Preempt this request
                req.status = RequestStatus.PREEMPTED
                self.block_manager.free_blocks(req.req_id)
                self.waiting_queue.appendleft(req)  # Re-queue for later resumption
                continue

            # Simulate autoregressive token generation
            token_idx = len(req.generated_tokens) + 1
            token_val = f"tok_{token_idx}"
            req.generated_tokens.append(token_val)
            new_tokens[req.req_id] = token_val

            # Check termination
            if len(req.generated_tokens) >= req.max_new_tokens:
                req.status = RequestStatus.FINISHED
                req.finish_step = self.current_step
                self.block_manager.free_blocks(req.req_id)
                self.finished_requests.append(req)
            else:
                retained_batch.append(req)

        self.running_batch = retained_batch
        return new_tokens

    def is_idle(self) -> bool:
        return len(self.waiting_queue) == 0 and len(self.running_batch) == 0


# ============================================================================
# 3. Speculative Decoding Token Verification Engine
# ============================================================================

class SpeculativeDecoder:
    """Simulates draft-model speculation and target-model parallel verification."""

    @staticmethod
    def verify_tokens(
        draft_tokens: list[str],
        draft_probs: list[float],
        target_probs: list[float],
    ) -> tuple[list[str], int]:
        """Verifies draft tokens via speculative sampling acceptance criteria.

        Returns: (accepted_tokens, accepted_count)
        """
        accepted: list[str] = []

        for token, p_draft, p_target in zip(draft_tokens, draft_probs, target_probs, strict=False):
            if p_draft <= 0:
                break
            # Acceptance probability: min(1.0, P_target / P_draft)
            ratio = min(1.0, p_target / p_draft)
            # Deterministic acceptance test (simulating random uniform sample <= ratio)
            if ratio >= 0.8:
                accepted.append(token)
            else:
                # Reject token and stop speculative chain
                break

        return accepted, len(accepted)
