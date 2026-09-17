from __future__ import annotations

from continuous_batcher import ContinuousBatchScheduler


def test_continuous_batching_lifecycle():
    scheduler = ContinuousBatchScheduler(max_batch_size=2)

    # Req 1 needs only 2 tokens, Req 2 needs 5 tokens, Req 3 needs 2 tokens
    scheduler.add_request("req_1", prompt_len=10, max_tokens=2)
    scheduler.add_request("req_2", prompt_len=10, max_tokens=5)
    scheduler.add_request("req_3", prompt_len=10, max_tokens=2)

    # Step 1: req_1 and req_2 admitted
    s1 = scheduler.step()
    assert "req_1" in s1 and "req_2" in s1
    assert len(scheduler.running_batch) == 2

    # Step 2: req_1 reaches max_tokens=2 and finishes!
    _ = scheduler.step()
    assert len(scheduler.completed_requests) == 1
    assert scheduler.completed_requests[0].request_id == "req_1"

    # Step 3: req_3 must be admitted immediately into the freed slot
    s3 = scheduler.step()
    assert "req_3" in s3
    assert "req_2" in s3
