# Debug Lab: Forensic Analysis & Solution

## Incident: BSONObjectTooLarge Error on Unbounded Sensor Array

### 🔍 Root Cause Analysis
IoT readings appended continuously into a single document array without capping, eventually breaching the 16MB document size limit.

### 🛠️ The Fix
Implement the Time-Series Bucket Pattern: store at most 500 readings per document bucket and insert a new document when bucket reaches capacity.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
