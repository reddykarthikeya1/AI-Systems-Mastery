"""Module 06: W3-Style Interactive Error Handling Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

def safe_divide():
    print("\n--- Crash-Proof Division Calculator ---")
    while True:
        raw_a = input("Enter numerator (or 'q' to quit): ").strip()
        if raw_a.lower() == 'q':
            break
        raw_b = input("Enter denominator: ").strip()

        try:
            val_a = float(raw_a)
            val_b = float(raw_b)
            ans = val_a / val_b
        except ValueError:
            print("[X] Error: Both inputs must be valid numbers!")
        except ZeroDivisionError:
            print("[X] Error: Mathematical division by zero is impossible!")
        else:
            print(f"[OK] Success: {val_a} / {val_b} = {ans:.4f}")
        finally:
            print("--- Calculation attempt recorded ---")

def main():
    print("=" * 60)
    print("  MODULE 06: INTERACTIVE ERROR HANDLING PLAYGROUND [SEC]")
    print("=" * 60)
    safe_divide()
    print("\nGreat job! Proceed to Module 07.")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
