from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class ActiveRequest:
    request_id: str
    prompt_len: int
    max_tokens: int
    generated_count: int = 0
    is_finished: bool = False


class ContinuousBatchScheduler:
    """Simulates Orca/vLLM iteration-level continuous batch scheduling."""

    def __init__(self, max_batch_size: int = 4):
        self.max_batch_size = max_batch_size
        self.waiting_queue: list[ActiveRequest] = []
        self.running_batch: list[ActiveRequest] = []
        self.completed_requests: list[ActiveRequest] = []

    def add_request(self, request_id: str, prompt_len: int, max_tokens: int) -> None:
        req = ActiveRequest(request_id=request_id, prompt_len=prompt_len, max_tokens=max_tokens)
        self.waiting_queue.append(req)

    def step(self) -> dict[str, int]:
        """Executes ONE iteration-level decode step across the active batch."""
        # 1. Admit waiting requests if batch capacity exists
        while len(self.running_batch) < self.max_batch_size and self.waiting_queue:
            admitted = self.waiting_queue.pop(0)
            self.running_batch.append(admitted)

        # 2. Step each running request by 1 token
        generated_this_step: dict[str, int] = {}
        for req in list(self.running_batch):
            req.generated_count += 1
            generated_this_step[req.request_id] = req.generated_count

            # Check if request has finished
            if req.generated_count >= req.max_tokens:
                req.is_finished = True
                self.running_batch.remove(req)
                self.completed_requests.append(req)

        return generated_this_step
