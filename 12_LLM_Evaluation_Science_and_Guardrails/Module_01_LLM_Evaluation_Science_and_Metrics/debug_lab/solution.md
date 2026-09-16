# Debug Lab Solution: Blind Evaluator Bug

### The Defect
`BrokenEvaluator` checks only substring prefix presence without sentence claim decomposition or intersection scoring.

### The Fix
Implement claim decomposition and token overlap scoring as shown in `project_solution/ragas_triad_evaluator.py`.
