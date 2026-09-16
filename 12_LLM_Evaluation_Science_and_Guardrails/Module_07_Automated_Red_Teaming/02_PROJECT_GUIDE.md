# Project Guide: Building an Automated Red-Teaming Engine

In this lab, you build an automated red-teaming harness that applies prompt mutation strategies (hypothetical framing, roleplay, reverse-psychology), probes target endpoints, and calculates ASR.

---

## Three-Tier Implementation Path

### Tier 1: Mutation Generation Pipeline (Required)
- Implement `PromptMutator` with multiple mutation strategies.
- Generate diversified attack variations from a seed objective.

### Tier 2: Target Probing & Outcome Evaluation
- Probe target model generate function.
- Evaluate responses using safety judge criteria.

### Tier 3: Attack Success Rate (ASR) Aggregation
- Compute ASR across mutation strategies and seed datasets.
