#!/usr/bin/env python3
"""DEBUG LAB: Overselling Limited Stock Under High Concurrency Race Condition

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

class DefectiveInventory:
    def __init__(self, stock: int):
        self.stock = stock
    
    def buy(self) -> bool:
        if self.stock > 0:
            import time
            time.sleep(0.001)  # Simulates thread switch
            self.stock -= 1
            return True
        return False


def reproduce_defect():
    print("Executing defective simulation for Module_20_Flash_Sale_Inventory_Reservation_Amazon...")
    inv = DefectiveInventory(1)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(lambda _: inv.buy(), range(5)))
    if sum(results) > 1:
        raise AssertionError(f'Oversold! Sold {sum(results)} units from stock of 1!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
