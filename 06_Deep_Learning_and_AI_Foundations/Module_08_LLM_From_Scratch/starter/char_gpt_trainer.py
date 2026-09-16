"""Starter template for CharGPTTrainer."""
from __future__ import annotations

import torch


class CharTokenizer:
    """Simple character-level tokenizer."""

    def __init__(self, text: str) -> None:
        raise NotImplementedError("Implement CharTokenizer.__init__")

    def encode(self, s: str) -> list[int]:
        raise NotImplementedError("Implement CharTokenizer.encode")

    def decode(self, indices: list[int]) -> str:
        raise NotImplementedError("Implement CharTokenizer.decode")


def train_toy_gpt(
    corpus: str,
    n_embd: int = 32,
    n_head: int = 2,
    block_size: int = 16,
    steps: int = 30,
) -> tuple[torch.nn.Module, float, float]:
    """Train a character-level toy GPT and return (model, initial_loss, final_loss)."""
    raise NotImplementedError("Implement train_toy_gpt")
