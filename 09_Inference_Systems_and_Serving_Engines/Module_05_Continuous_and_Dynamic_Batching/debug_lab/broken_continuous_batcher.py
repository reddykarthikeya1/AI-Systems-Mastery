# Debug Lab: Continuous Batching Scheduler Degrades to Static Batching
# Course 09 - Module 05 Continuous and Dynamic Batching

MAX_BATCH_SIZE = 4


class Request:
    def __init__(self, name, decode_steps_remaining):
        self.name = name
        self.remaining = decode_steps_remaining


def run_scheduler(all_requests):
    """Continuous batching should backfill any freed slot with the next
    waiting request on the very next step, instead of waiting for the whole
    running batch to drain before admitting anyone new."""
    waiting = list(all_requests)
    running = []
    step = 0
    finished_at_step = {}

    while waiting or running:
        step += 1
        # Admit new requests to fill free slots.
        if len(running) == 0:
            while waiting and len(running) < MAX_BATCH_SIZE:
                running.append(waiting.pop(0))

        # Decode one token for every request currently running.
        still_running = []
        for req in running:
            req.remaining -= 1
            if req.remaining <= 0:
                finished_at_step[req.name] = step
            else:
                still_running.append(req)
        running = still_running

    return finished_at_step, step


if __name__ == "__main__":
    # 6 requests, batch capacity 4. Initial batch req_1..req_4 need 2, 3, 4,
    # and 5 decode steps respectively, so req_1's slot frees up long before
    # req_4's does. req_5/req_6 need only 2 steps each and start out waiting.
    requests = [
        Request("req_1", 2), Request("req_2", 3),
        Request("req_3", 4), Request("req_4", 5),
        Request("req_5", 2), Request("req_6", 2),
    ]

    finished_at, total_steps = run_scheduler(requests)

    print("Batch capacity=4. Initial batch req_1..req_4 need 2/3/4/5 steps; "
          "req_5/req_6 (waiting, 2 steps each) should backfill freed slots as they open.")
    print("Expected (true continuous batching): req_1's slot frees at step 2 and is "
          "immediately backfilled, so req_5/req_6 finish by ~step 4 and the whole run "
          "completes in ~5 steps.")
    print(f"Actual finish steps: {finished_at}")
    print(f"Actual total steps to drain all 6 requests: {total_steps}")
