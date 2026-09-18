"""DEBUG LAB: ProvisionedThroughputExceededException on Single Partition Key

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class DynamoTable:
    """A toy DynamoDB table enforcing the per-partition write-capacity ceiling."""

    WCU_LIMIT_PER_PARTITION = 1000

    def __init__(self) -> None:
        self.partition_usage: dict[str, int] = {}
        self.accepted_writes = 0
        self.throttled_writes = 0

    def write(self, partition_key: str) -> bool:
        used = self.partition_usage.get(partition_key, 0)
        if used >= self.WCU_LIMIT_PER_PARTITION:
            self.throttled_writes += 1
            return False
        self.partition_usage[partition_key] = used + 1
        self.accepted_writes += 1
        return True

def static_partition_key(sensor_id: int) -> str:
    return "TELEMETRY"  # every sensor writes to the same partition key

def reproduce_defect() -> None:
    print("Ingesting a second's worth of readings from 5,000 sensors...")
    table = DynamoTable()
    for sensor_id in range(5000):
        table.write(static_partition_key(sensor_id))

    print(f"Accepted writes: {table.accepted_writes}")
    print(f"Throttled writes (ProvisionedThroughputExceededException): {table.throttled_writes}")
    if table.throttled_writes > 0:
        print("[DEFECT OBSERVED] Every sensor writes to the same static partition "
              "key, so the burst hits the 1,000 WCU per-partition ceiling.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
