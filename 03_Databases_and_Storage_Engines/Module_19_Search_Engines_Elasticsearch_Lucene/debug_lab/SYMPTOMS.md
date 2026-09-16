# Debug Lab: Incident Report & Symptoms

## Incident: Deep Pagination Offset Crashes Elasticsearch Data Nodes
- **Severity:** P1 Production Outage / Data Inconsistency
- **Affected Subsystem:** Module 19 Search Engines Elasticsearch Lucene

### 🚨 Reported Symptoms
The operations team reported unexpected behavior under production conditions:
- Errors observed in application logs.
- Unexpected latency degradation, data inconsistency, or transaction abortion.

### 🔬 Repro Steps
1. Navigate to this module's debug lab:
   ```bash
   cd Module_19_Search_Engines_Elasticsearch_Lucene/debug_lab
   ```
2. Run the repro script:
   ```bash
   python broken_es_search.py
   ```
3. Observe the crash or invariant failure.

### 🎯 Your Objective
1. Inspect `broken_es_search.py` to identify the root cause.
2. Formulate a hypothesis and test your fix.
3. Compare your solution with `ANSWERS.md`.
