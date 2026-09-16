# Debug Lab: Forensic Analysis & Solution

## Incident: Sequential Scan on 5,000,000 JSONB Document Catalog

### 🔍 Root Cause Analysis
Query uses text extraction operator `data->>'status' = 'active'` which bypasses the GIN index created with jsonb_path_ops.

### 🛠️ The Fix
Rewrite query to use JSONB containment: `data @> '{"status": "active"}'` or create an expression index on `((data->>'status'))`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
