"""Production reference implementation for CharGPTTrainer."""
from __future__ import annotations

import math

import torch
import torch.nn as nn
from torch.nn import functional as F


class CharTokenizer:
    """Simple character-level tokenizer."""

    def __init__(self, text: str) -> None:
        chars = sorted(set(text))
        self.vocab_size = len(chars)
        self.stoi = {ch: i for i, ch in enumerate(chars)}
        self.itos = dict(enumerate(chars))

    def encode(self, s: str) -> list[int]:
        return [self.stoi[c] for c in s if c in self.stoi]

    def decode(self, indices: list[int]) -> str:
        return "".join([self.itos[i] for i in indices if i in self.itos])


class CausalSelfAttention(nn.Module):
    def __init__(self, n_embd: int, n_head: int, block_size: int) -> None:
        super().__init__()
        self.n_head = n_head
        self.head_dim = n_embd // n_head
        self.c_attn = nn.Linear(n_embd, 3 * n_embd)
        self.c_proj = nn.Linear(n_embd, n_embd)
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, c = x.size()
        q, k, v = self.c_attn(x).chunk(3, dim=2)
        q = q.view(b, t, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(b, t, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(b, t, self.n_head, self.head_dim).transpose(1, 2)

        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        att = att.masked_fill(self.bias[:, :, :t, :t] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(b, t, c)
        return self.c_proj(y)


class TransformerBlock(nn.Module):
    def __init__(self, n_embd: int, n_head: int, block_size: int) -> None:
        super().__init__()
        self.ln_1 = nn.LayerNorm(n_embd)
        self.attn = CausalSelfAttention(n_embd, n_head, block_size)
        self.ln_2 = nn.LayerNorm(n_embd)
        self.mlp = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.GELU(),
            nn.Linear(4 * n_embd, n_embd),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class MiniGPT(nn.Module):
    def __init__(self, vocab_size: int, n_embd: int, n_head: int, block_size: int) -> None:
        super().__init__()
        self.block_size = block_size
        self.wte = nn.Embedding(vocab_size, n_embd)
        self.wpe = nn.Embedding(block_size, n_embd)
        self.block = TransformerBlock(n_embd, n_head, block_size)
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)

    def forward(
        self, idx: torch.Tensor, targets: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        _, t = idx.size()
        pos = torch.arange(0, t, dtype=torch.long, device=idx.device)
        tok_emb = self.wte(idx)
        pos_emb = self.wpe(pos)
        x = tok_emb + pos_emb
        x = self.block(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


def train_toy_gpt(
    corpus: str,
    n_embd: int = 32,
    n_head: int = 2,
    block_size: int = 16,
    steps: int = 30,
) -> tuple[torch.nn.Module, float, float]:
    """Train a character-level toy GPT and return (model, initial_loss, final_loss)."""
    tokenizer = CharTokenizer(corpus)
    data = torch.tensor(tokenizer.encode(corpus), dtype=torch.long)

    model = MiniGPT(tokenizer.vocab_size, n_embd=n_embd, n_head=n_head, block_size=block_size)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)

    initial_loss = 0.0
    final_loss = 0.0

    for step in range(steps):
        # Sample mini-batch
        ix = torch.randint(len(data) - block_size - 1, (4,))
        x = torch.stack([data[i : i + block_size] for i in ix])
        y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])

        _, loss = model(x, y)
        if step == 0:
            initial_loss = float(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step == steps - 1:
            final_loss = float(loss.item())

    return model, initial_loss, final_loss
