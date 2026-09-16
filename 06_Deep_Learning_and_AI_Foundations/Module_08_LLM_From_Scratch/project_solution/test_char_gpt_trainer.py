"""Unit tests for CharGPTTrainer."""
from __future__ import annotations

from char_gpt_trainer import (
    CharTokenizer,
    train_toy_gpt,
)


def test_char_tokenizer() -> None:
    text = "hello world"
    tok = CharTokenizer(text)
    encoded = tok.encode(text)
    decoded = tok.decode(encoded)
    assert decoded == text


def test_toy_gpt_training_convergence() -> None:
    corpus = "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer."
    _, init_loss, final_loss = train_toy_gpt(corpus, n_embd=32, n_head=2, block_size=16, steps=35)

    # Cross-entropy loss must decrease during training
    assert final_loss < init_loss
    assert final_loss < 2.0
