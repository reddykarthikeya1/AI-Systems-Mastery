# Debug Lab Solution: Inverted Breach Logic Bug

### The Defect
`BrokenRedTeamer` flags refusals as breaches, which inverts the meaning of Attack Success Rate (ASR).

### The Fix
Ensure refusals are scored as safe ($is\_breach = False$) as shown in `project_solution/automated_red_teamer.py`.
