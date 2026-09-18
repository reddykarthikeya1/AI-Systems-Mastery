# Debug Lab Solution & Forensic Post-Mortem

## Incident: ProvisionedThroughputExceededException on Single Partition Key

---

### 🔍 Forensic Root Cause Analysis
`static_partition_key()` returns the literal string `"TELEMETRY"` for every
sensor, regardless of which of the 5,000 sensors is writing. DynamoDB
distributes write capacity per physical partition, keyed by partition key, and
each partition has a fixed throughput ceiling (`WCU_LIMIT_PER_PARTITION`).
Routing all 5,000 concurrent writes to one partition key means they all
compete for one partition's capacity instead of being spread across the
table's many partitions, so most of them are throttled.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def sharded_partition_key(sensor_id):
    """Spreads writes across many partitions by including the sensor's own
    identity (or a high-cardinality shard suffix) in the partition key."""
    return f"TELEMETRY#{sensor_id}"
```

This is DynamoDB's standard "write sharding" pattern: the partition key must
have enough cardinality that concurrent writers land on different physical
partitions, each with its own WCU budget.

---

### 🛡️ Production Prevention Invariants
1. **Design partition keys for cardinality**, never a constant or low-cardinality
   value on a high-throughput table.
2. **Monitor `ConsumedWriteCapacityUnits` per partition** (via CloudWatch
   contributor insights) to catch hot keys before they throttle.
3. **Load-test with production-realistic key distributions**, not a single
   synthetic key, before launch.
