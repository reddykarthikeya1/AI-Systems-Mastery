# Debug Lab Solution & Forensic Post-Mortem

## Incident: BSONObjectTooLarge Error on Unbounded Sensor Array

---

### 🔍 Forensic Root Cause Analysis
`SensorDocument.ingest()` appends every incoming reading to the same
document's array forever, with no ceiling. At one reading per second, a
single document accumulates 86,400 readings a day; within roughly four to
five days it crosses MongoDB's hard 16MB BSON document limit. The schema has
no notion of "this document is full, start a new one" -- it treats one sensor
as one unboundedly-growing document for its entire lifetime.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class BucketedSensorDocument:
    MAX_READINGS_PER_BUCKET = 1000   # comfortably under the 16MB limit

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.buckets = [[]]

    def ingest(self, reading):
        if len(self.buckets[-1]) >= self.MAX_READINGS_PER_BUCKET:
            self.buckets.append([])   # roll over into a new bucket document
        self.buckets[-1].append(reading)
```

This is the standard MongoDB "bucket pattern": one document per time window
(or per N readings), referencing the sensor by a shared key, instead of one
document per sensor for all time.

---

### 🛡️ Production Prevention Invariants
1. **Cap array growth explicitly** (`$push` with `$slice`, or an application-level
   bucket rollover) on any schema with an unbounded embedded array.
2. **Alert on document size approaching the 16MB limit** well before it is hit.
3. **Model time-series data with the bucket pattern**, not a single growing document.
