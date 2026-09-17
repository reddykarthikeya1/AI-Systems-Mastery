"""Reference Solution — Problem 01: detect_jailbreak_heuristics

Topic: NeMo Guardrails and Llama Guard
"""

from __future__ import annotations

def detect_jailbreak_heuristics(prompt: str) -> dict[str, bool | float]:
    lowered = prompt.lower()
    canary_tokens = [
        "ignore previous instructions", "disregard all previous", "you are now in developer mode",
        "dan mode", "do anything now", "bypass safety", "reveal your system prompt"
    ]
    matches = sum(1 for tok in canary_tokens if tok in lowered)
    is_threat = (matches > 0) or (len(prompt) > 4000)
    confidence = min(1.0, matches * 0.5) if matches > 0 else 0.0
    return {"is_threat": is_threat, "threat_confidence": confidence, "match_count": matches}

