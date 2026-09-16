# Debug Lab Solution: Positional Bias Vulnerability

### The Defect
`BrokenJudge` performs only a single evaluation pass, allowing position bias to dictate benchmark outcomes.

### The Fix
Implement swap-pair dual evaluation and tie resolution as shown in `project_solution/llm_judge_calibrator.py`.
