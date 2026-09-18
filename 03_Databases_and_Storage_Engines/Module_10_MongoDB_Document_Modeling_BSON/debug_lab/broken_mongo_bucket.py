"""DEBUG LAB: BSONObjectTooLarge Error on Unbounded Sensor Array

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

BSON_LIMIT_BYTES = 16 * 1024 * 1024
READING_SIZE_BYTES = 48  # approximate encoded size of one embedded reading subdocument

class SensorDocument:
    """A toy MongoDB document holding one sensor's readings in a single array
    that is never bucketed into a new document once it grows large."""

    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        self.reading_count = 0

    def ingest(self, count: int) -> None:
        self.reading_count += count  # no capping, no rollover into a new bucket document

    def size_bytes(self) -> int:
        return 64 + self.reading_count * READING_SIZE_BYTES

def reproduce_defect() -> None:
    print("Ingesting once-per-second telemetry into a single sensor document...")
    doc = SensorDocument("sensor-42")
    readings_per_day = 86400
    days_of_continuous_ingestion = 5
    doc.ingest(readings_per_day * days_of_continuous_ingestion)

    size = doc.size_bytes()
    print(f"Document size after {days_of_continuous_ingestion} days: {size:,} bytes")
    print(f"BSON document size limit: {BSON_LIMIT_BYTES:,} bytes")
    if size > BSON_LIMIT_BYTES:
        print("[DEFECT OBSERVED] The single sensor document has grown past the 16MB "
              "BSON limit because readings are never bucketed into new documents.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
