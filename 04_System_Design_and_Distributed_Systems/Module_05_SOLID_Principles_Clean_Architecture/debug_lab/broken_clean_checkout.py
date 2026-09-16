#!/usr/bin/env python3
"""DEBUG LAB: Inventory Over-Reservation Rollback Failure on Payment Exception

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def process_checkout(order_id: str, payment_gateway, inventory_service):
    inventory_service.reserve(order_id)
    # Payment fails:
    raise ValueError('Payment declined: insufficient funds')
    # Inventory was reserved but never released!


def reproduce_defect():
    print("Executing defective simulation for Module_05_SOLID_Principles_Clean_Architecture...")
    class MockInv: 
        def reserve(self, oid): self.reserved = True
        def release(self, oid): self.reserved = False
    inv = MockInv()
    try:
        process_checkout('ord_1', None, inv)
    except ValueError:
        assert inv.reserved is True, 'Inventory remained locked!'
        raise RuntimeError('Inventory remained locked after payment decline!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
