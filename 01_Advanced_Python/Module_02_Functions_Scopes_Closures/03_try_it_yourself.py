"""Module 02: W3-Style Interactive Functions Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

def create_tip_calculator(tax_rate=0.08):
    """Demonstrates a closure: remembers tax_rate."""
    def calculate(bill_amount, tip_percent=15):
        tax = bill_amount * tax_rate
        tip = bill_amount * (tip_percent / 100)
        total = bill_amount + tax + tip
        return {
            "subtotal": bill_amount,
            "tax": round(tax, 2),
            "tip": round(tip, 2),
            "total": round(total, 2)
        }
    return calculate

def main():
    print("=" * 60)
    print("  MODULE 02: INTERACTIVE FUNCTIONS & CLOSURES PLAYGROUND   ")
    print("=" * 60)

    calc = create_tip_calculator(tax_rate=0.08)

    while True:
        try:
            print("\nCalculate a restaurant bill:")
            raw = input("Enter bill amount in dollars (or 'q' to quit): ").strip()
            if raw.lower() == 'q':
                print("Proceed to Module 03!")
                break

            amount = float(raw)
            tip_str = input("Enter tip percentage (default 15): ").strip()
            tip = float(tip_str) if tip_str else 15.0

            summary = calc(amount, tip)
            print("-" * 40)
            print(f"Subtotal:  ${summary['subtotal']:.2f}")
            print(f"Tax (8%):   ${summary['tax']:.2f}")
            print(f"Tip ({tip}%): ${summary['tip']:.2f}")
            print(f"TOTAL:     ${summary['total']:.2f}")
            print("-" * 40)
        except ValueError:
            print("Please enter valid numbers!")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
