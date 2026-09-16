# Debug Lab: Module 02 — Functions & Scopes Traps

## How to Run
```bash
python debug_lab/broken_game.py
```

## Observed Symptoms
1. **Cross-contamination of player inventories**:
   Player 2 starts with Player 1's items: `['Sword', 'Shield']` instead of just `['Shield']`.
2. **Late-binding closure multiplier bug**:
   Instead of multiplying by 0, 1, and 2, all multiplier functions produce `20` (`[20, 20, 20]`).
3. **TypeError on calculating team score**:
   Calling `calculate_team_score([10, 20, 30])` crashes:
   ```
   TypeError: 'int' object is not callable
   ```
