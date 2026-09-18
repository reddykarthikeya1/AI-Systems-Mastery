# Debug Lab: Warp Divergence Latency Estimate Is Too Low
# Course 07 - Module 01 GPU Microarchitecture and Execution Model

def simulate_warp_naive(thread_predicates, cost_if, cost_else):
    costs = [cost_if if p else cost_else for p in thread_predicates]
    return max(costs)


def simulate_warp_simt(thread_predicates, cost_if, cost_else):
    took_if = any(thread_predicates)
    took_else = any(not p for p in thread_predicates)
    total = 0
    if took_if:
        total += cost_if
    if took_else:
        total += cost_else
    return total


if __name__ == "__main__":
    warp_size = 32
    thread_predicates = [(tid % 2 == 0) for tid in range(warp_size)]
    cost_if, cost_else = 4, 6

    estimated_cycles = simulate_warp_naive(thread_predicates, cost_if, cost_else)
    serialized_cycles = simulate_warp_simt(thread_predicates, cost_if, cost_else)

    print(f"Warp of {warp_size} threads: half take the 'if' branch ({cost_if} cycles), half take 'else' ({cost_else} cycles).")
    print(f"Estimated warp completion latency: {estimated_cycles} cycles")
    print(f"Cycles spent on the 'if' path + cycles spent on the 'else' path: {cost_if} + {cost_else} = {serialized_cycles} cycles")
