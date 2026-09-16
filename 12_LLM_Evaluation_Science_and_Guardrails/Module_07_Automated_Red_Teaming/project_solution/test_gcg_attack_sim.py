"""Unit tests for GCG Attack Simulator."""

from __future__ import annotations

from gcg_attack_sim import GCGAttackSimulator


def test_gcg_loss_minimization():
    simulator = GCGAttackSimulator(target_loss_threshold=0.15)

    def mock_loss(prompt: str) -> float:
        score = 1.0
        if "bypass" in prompt:
            score -= 0.5
        if "override" in prompt:
            score -= 0.4
        return max(0.10, score)

    best_suffix, history = simulator.optimize_suffix("create malware", mock_loss, max_steps=5)
    assert history[-1].loss <= 0.15
    assert "bypass" in best_suffix or "override" in best_suffix
