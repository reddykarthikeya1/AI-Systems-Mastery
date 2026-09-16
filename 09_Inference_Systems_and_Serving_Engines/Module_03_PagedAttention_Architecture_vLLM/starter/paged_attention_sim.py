from __future__ import annotations


class PagedAttentionBlockManager:
    def __init__(self, num_blocks: int, block_size: int = 16):
        raise NotImplementedError("Implement PagedAttentionBlockManager")

    def allocate_request(self, request_id: str) -> None:
        raise NotImplementedError("Implement allocate_request")

    def append_token(self, request_id: str, token_id: int) -> None:
        raise NotImplementedError("Implement append_token")

    def fork_request(self, parent_id: str, child_id: str) -> None:
        raise NotImplementedError("Implement fork_request")

    def free_request(self, request_id: str) -> None:
        raise NotImplementedError("Implement free_request")
