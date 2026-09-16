"""Module 22: Standalone Interactive Demo - PagedAttention & Continuous Batching."""

from project_solution.llm_inference_engine import (
    ContinuousBatchScheduler,
    InferenceRequest,
    PagedAttentionBlockManager,
    SpeculativeDecoder,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 22: DISTRIBUTED LLM SERVING (vLLM PAGEDATTENTION & CONTINUOUS BATCHING)")
    print("=" * 80)

    # ---------------------------------------------------------
    # Step 1: PagedAttention Block Table Simulation
    # ---------------------------------------------------------
    print("\n--- 1. PagedAttention Virtual-to-Physical GPU Memory Paging ---")
    block_size = 4
    total_blocks = 16
    block_mgr = PagedAttentionBlockManager(num_gpu_blocks=total_blocks, block_size=block_size)

    print(f" Total Physical GPU Blocks: {total_blocks} (Block Size: {block_size} tokens/block)")
    print(f" Initial Free Blocks:       {block_mgr.num_free_blocks()}")

    req_alpha = "req_user_query_1"
    # Prompt is 7 tokens -> requires ceil(7/4) = 2 blocks
    block_mgr.ensure_blocks_for_length(req_alpha, total_tokens=7)
    print(f"\n Allocated prompt for '{req_alpha}' (7 tokens):")
    print(f"   Mapped Physical Blocks: {block_mgr.block_tables[req_alpha]}")
    print(f"   Remaining Free Blocks:  {block_mgr.num_free_blocks()}")
    print(f"   GPU Memory In-Use:      {block_mgr.get_memory_utilization() * 100:.1f}%")

    # Sequence grows to 10 tokens -> requires 3 blocks
    block_mgr.ensure_blocks_for_length(req_alpha, total_tokens=10)
    print("\n Sequence grew to 10 tokens (crossed block boundary):")
    print(f"   Updated Physical Blocks: {block_mgr.block_tables[req_alpha]}")
    print(f"   Remaining Free Blocks:   {block_mgr.num_free_blocks()}")

    block_mgr.free_blocks(req_alpha)
    print("\n Sequence finished -> Memory freed:")
    print(f"   Free Blocks Restored:    {block_mgr.num_free_blocks()} (Utilization: {block_mgr.get_memory_utilization() * 100:.1f}%)")

    # ---------------------------------------------------------
    # Step 2: Continuous Iteration-Level Batching
    # ---------------------------------------------------------
    print("\n--- 2. Continuous Iteration-Level Batching Simulation ---")
    scheduler = ContinuousBatchScheduler(
        block_manager=PagedAttentionBlockManager(num_gpu_blocks=32, block_size=4),
        max_batch_size=4,
    )

    # Add initial requests
    r1 = InferenceRequest("req_long", "Explain distributed consensus...", ["p1", "p2", "p3", "p4"], max_new_tokens=8)
    r2 = InferenceRequest("req_short", "What is 2+2?", ["p1", "p2"], max_new_tokens=3)
    scheduler.add_request(r1)
    scheduler.add_request(r2)

    print(" Initial Batch Loaded: [req_long (8 tokens), req_short (3 tokens)]")
    print(" Commencing Autoregressive Generation Steps:")

    for step_num in range(1, 10):
        # Dynamically inject new arriving request midway at step 3!
        if step_num == 3:
            r3 = InferenceRequest("req_dynamic_midway", "Summarize paper...", ["p1", "p2", "p3"], max_new_tokens=4)
            scheduler.add_request(r3)
            print(f"\n >>> [STEP {step_num}] NEW REQUEST ARRIVED: 'req_dynamic_midway' queued dynamically!")

        tokens_generated = scheduler.step()
        running_ids = [r.req_id for r in scheduler.running_batch]
        finished_ids = [r.req_id for r in scheduler.finished_requests if r.finish_step == scheduler.current_step]

        print(f" [Step {step_num:02d}] Active: {running_ids} | Output Tokens: {tokens_generated}")
        if finished_ids:
            print(f"           *** COMPLETED & EVICTED: {finished_ids} (GPU blocks immediately reclaimed)")

        if scheduler.is_idle():
            print("\n All requests completed with ZERO GPU idling!")
            break

    # ---------------------------------------------------------
    # Step 3: Speculative Decoding Verification
    # ---------------------------------------------------------
    print("\n--- 3. Speculative Decoding Multi-Token Verification ---")
    draft_tokens = ["the", "future", "of", "artificial"]
    draft_probs = [0.95, 0.90, 0.88, 0.70]
    target_probs = [0.94, 0.92, 0.85, 0.40]  # Discrepancy on 4th token

    accepted, count = SpeculativeDecoder.verify_tokens(draft_tokens, draft_probs, target_probs)
    print(f" Draft Model Speculated: {draft_tokens}")
    print(f" Target Model Probabilities vs Draft: {target_probs} vs {draft_probs}")
    print(f" Accepted in 1 Target Forward Pass: {accepted} ({count}/{len(draft_tokens)} tokens accepted)")
    print(f" Effective Generation Speedup:      {count}x faster than standard autoregression!")

    print("=" * 80)


if __name__ == "__main__":
    main()
