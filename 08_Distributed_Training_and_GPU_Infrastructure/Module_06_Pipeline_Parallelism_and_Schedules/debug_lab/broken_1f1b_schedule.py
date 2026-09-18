# Debug Lab: 1F1B Pipeline Schedule Gives the Last Stage an Extra Warmup Step
# Course 08 - Module 06 Pipeline Parallelism and Schedules

def warmup_microbatch_count(stage_id, num_stages, num_microbatches):
    """Number of forward-only 'warmup' microbatches a stage must run before
    it can start alternating one forward with one backward (1F1B)."""
    count = num_stages - stage_id
    return min(count, num_microbatches)


def total_bubble_steps(num_stages, num_microbatches):
    """Sum of every stage's warmup step count -- the pipeline's total idle
    'bubble' overhead before steady-state 1F1B production begins."""
    return sum(
        warmup_microbatch_count(s, num_stages, num_microbatches) for s in range(num_stages)
    )


if __name__ == "__main__":
    num_stages = 4
    num_microbatches = 8

    per_stage_warmup = [warmup_microbatch_count(s, num_stages, num_microbatches) for s in range(num_stages)]
    last_stage = num_stages - 1

    print(f"num_stages={num_stages}, num_microbatches={num_microbatches}")
    print(f"Warmup forward-pass count per stage (0..{last_stage}): {per_stage_warmup}")
    print(f"Last stage ({last_stage}) warmup count: {per_stage_warmup[last_stage]} (expected: 0 -- "
          f"the last stage produces the loss and should begin 1F1B immediately)")
    print(f"Total bubble steps across all stages: {total_bubble_steps(num_stages, num_microbatches)} "
          f"(expected: {sum(range(num_stages))})")
