# Debug Lab: Forensic Analysis & Solution

## Incident: Running Total Generates Identical Duplicate Numbers on Duplicate Dates

### 🔍 Root Cause Analysis
Window frame specification uses default RANGE frame instead of ROWS frame, causing rows with identical ORDER BY keys to sum together simultaneously.

### 🛠️ The Fix
Change window frame to: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
