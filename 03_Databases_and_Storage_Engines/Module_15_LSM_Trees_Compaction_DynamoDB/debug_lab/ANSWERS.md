# Debug Lab: Forensic Analysis & Solution

## Incident: ProvisionedThroughputExceededException on Single Partition Key

### 🔍 Root Cause Analysis
All telemetry data from 50,000 sensors written to a single static partition key `PK = 'TELEMETRY'`, exceeding DynamoDB's 1,000 WCU per-partition ceiling.

### 🛠️ The Fix
Implement write sharding: salt the partition key with random suffixes `PK = f'TELEMETRY#{random.randint(1, 10)}'`.

### 🛡️ Production Prevention & Invariants
- Establish automated regression tests covering this edge case.
- Monitor metrics and configure alerts before failure thresholds are breached.
