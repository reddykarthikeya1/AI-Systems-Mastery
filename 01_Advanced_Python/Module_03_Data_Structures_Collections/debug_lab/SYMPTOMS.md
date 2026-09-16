# Debug Lab: Module 03 — Data Structures Traps

## How to Run
```bash
python debug_lab/broken_matching_engine.py
```

## Observed Symptoms
1. **RuntimeError on dictionary eviction**:
   ```
   RuntimeError: dictionary changed size during iteration
   ```
2. **Mutating cloned portfolio corrupts original portfolio**:
   Modifying `cloned["trader_1"][0]["qty"]` inadvertently changes `original["trader_1"][0]["qty"]` to `999`.
3. **TypeError inserting records into set**:
   ```
   TypeError: unhashable type: 'dict'
   ```
