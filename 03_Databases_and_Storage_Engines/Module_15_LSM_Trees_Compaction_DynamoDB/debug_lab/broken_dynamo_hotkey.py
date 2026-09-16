"""DEBUG LAB: ProvisionedThroughputExceededException on Single Partition Key

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: ProvisionedThroughputExceededException on Single Partition Key")
    # Root Cause: All telemetry data from 50,000 sensors written to a single static partition key `PK = 'TELEMETRY'`, exceeding DynamoDB's 1,000 WCU per-partition ceiling.
    raise RuntimeError("Defect triggered: ProvisionedThroughputExceededException on Single Partition Key")

if __name__ == "__main__":
    reproduce_defect()
