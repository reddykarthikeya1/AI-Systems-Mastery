"""Unit tests for LoRALinear and DPOLossEvaluator."""
from __future__ import annotations

import torch
from lora_and_dpo import DPOLossEvaluator, LoRALinear


def test_lora_initialization_zero_delta():
    in_dim, out_dim, rank = 8, 4, 2
    layer = LoRALinear(in_dim, out_dim, rank=rank, alpha=4.0)

    x = torch.randn(2, in_dim)
    # At step 0, B is zero so output must identically equal base_layer(x)
    with torch.no_grad():
        lora_out = layer(x)
        base_out = layer.base_layer(x)

    assert torch.allclose(lora_out, base_out, atol=1e-6)

    # Base weight must not require grad, but A and B must
    assert not layer.base_layer.weight.requires_grad
    assert layer.lora_A.requires_grad
    assert layer.lora_B.requires_grad


def test_dpo_loss_gradient_direction():
    # Case where policy prefers chosen: policy_chosen > ref_chosen
    pi_chosen = torch.tensor([-1.0])
    pi_rejected = torch.tensor([-4.0])
    ref_chosen = torch.tensor([-2.0])
    ref_rejected = torch.tensor([-2.0])

    loss_good = DPOLossEvaluator.compute_dpo_loss(
        pi_chosen, pi_rejected, ref_chosen, ref_rejected, beta=0.1
    )

    # Case where policy mistakenly prefers rejected
    pi_chosen_bad = torch.tensor([-4.0])
    pi_rejected_bad = torch.tensor([-1.0])

    loss_bad = DPOLossEvaluator.compute_dpo_loss(
        pi_chosen_bad, pi_rejected_bad, ref_chosen, ref_rejected, beta=0.1
    )

    # Good alignment must have strictly lower loss
    assert float(loss_good.item()) < float(loss_bad.item())
