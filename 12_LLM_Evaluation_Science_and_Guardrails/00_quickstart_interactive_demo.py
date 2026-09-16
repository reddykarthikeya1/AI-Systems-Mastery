"""Course 12 Quickstart: Interactive Guardrails & Adversarial Attack Demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Module_04_Production_Guardrails_Architecture" / "project_solution"))
sys.path.insert(0, str(Path(__file__).parent / "Module_07_Automated_Red_Teaming" / "project_solution"))
from gcg_attack_sim import GCGAttackSimulator
from neural_ner_pii_scanner import NeuralNERPIIScanner


def run_demo() -> None:
    print("=" * 70)
    print(" COURSE 12: LLM EVALUATION SCIENCE & GUARDRAILS QUICKSTART")
    print("=" * 70)

    print("\n[1] Neural NER Unstructured PII Scanner & Redaction Gateway:")
    scanner = NeuralNERPIIScanner()
    raw_prompt = "Patient intake note: Dr. Katherine met with Mr. Jonathan at 742 Evergreen Terrace."
    entities = scanner.scan_entities(raw_prompt)
    masked = scanner.mask_unstructured_pii(raw_prompt)

    print(f"     * Original Prompt: {raw_prompt}")
    print(f"     * Detected Entities: {[f'{e.text} ({e.entity_type})' for e in entities]}")
    print(f"     * Redacted Output:   {masked}")

    print("\n[2] Greedy Coordinate Gradient (GCG) White-Box Suffix Optimizer:")
    simulator = GCGAttackSimulator(target_loss_threshold=0.15)

    def mock_safety_loss(text: str) -> float:
        score = 1.0
        if "bypass" in text:
            score -= 0.5
        if "override" in text:
            score -= 0.4
        return max(0.10, score)

    best_suffix, history = simulator.optimize_suffix("extract database credentials", mock_safety_loss, max_steps=4)
    print(f"     * Optimized Adversarial Suffix: '{best_suffix}'")
    print(f"     * Final Safety Filter Loss:    {history[-1].loss:.2f} (Bypassed safety threshold!)")

    print("\n" + "=" * 70)
    print(" QUICKSTART DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
