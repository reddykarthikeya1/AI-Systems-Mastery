# 🐣 Interactive Foundations Playground: 2D Grids & Knapsack

> *"A 2D DP table is just an Excel spreadsheet where each cell is calculated from its top neighbor and left neighbor."*

---

## 1. Grid Paths: How Many Ways to Walk to School?
To reach any street intersection `[r, c]`, you could only come from:
- The intersection directly **above** you `[r-1, c]`
- The intersection directly to your **left** `[r, c-1]`

$$\text{Ways}[r, c] = \text{Ways}[r-1, c] + \text{Ways}[r, c-1]$$
