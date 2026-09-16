#!/usr/bin/env python3
"""DEBUG LAB: Dual-Write Inconsistency: Database Committed but Message Broker Publish Failed

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def naive_dual_write(db_conn, message_broker, order_id: str):
    db_conn.commit()  # DB write succeeds
    # Message broker drops connection:
    raise ConnectionResetError('Kafka publish failed! Database committed but message never sent.')


def reproduce_defect():
    print("Executing defective simulation for Module_23_Distributed_Transactions_Sagas_Outbox...")
    class MockDB: 
        def commit(self): pass
    naive_dual_write(MockDB(), None, 'ord_1')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
