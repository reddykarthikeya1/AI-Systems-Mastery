from __future__ import annotations


class ContinuousBatchScheduler:
    def __init__(self, max_batch_size: int = 4):
        raise NotImplementedError("Implement ContinuousBatchScheduler")

    def add_request(self, request_id: str, prompt_len: int, max_tokens: int) -> None:
        raise NotImplementedError("Implement add_request")

    def step(self) -> dict[str, int]:
        raise NotImplementedError("Implement step")
