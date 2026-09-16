# Beginner's Guide: Navigating Data Structures & Algorithms

Welcome! Whether you are writing your first recursion tree or preparing for a Staff Engineer algorithmic screen, this guide will orient you.

## The Mental Model
1. **Time Complexity is Work Done**: Count the fundamental operations as input size $N$ scales to infinity.
2. **Space Complexity is Working Memory**: Distinguish between auxiliary memory (your extra buffers/recursion stack) and input allocation.
3. **Hardware Counts**: An $O(N)$ array scan is often 10x faster in wall-clock time than an $O(N)$ linked list traversal due to CPU L1/L2 cache prefetching.

## Standard Directory Structure
Every module folder contains:
1. `01_README.md`: Theory, mathematical proofs, diagrams, and code walkthroughs.
2. `02_PROJECT_GUIDE.md`: Specification for the hands-on reference implementation.
3. `03_SELF_ASSESSMENT_AND_CHALLENGES.md`: Graded multiple-choice questions, trace challenges, and interview scenarios.
4. `04_TROUBLESHOOTING_AND_EDGE_CASES.md`: Common pitfalls (off-by-one errors, recursion limits, integer overflows).
5. `starter/`: Scaffold code for hands-on practice.
6. `project_solution/`: Tested reference implementation.
7. `debug_lab/`: Buggy scenarios to hone debugging skills.
