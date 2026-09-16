#!/usr/bin/env python3
"""Module 02: Essential Standard Library Core Demonstration.

This script demonstrates practical usage of math, random, datetime, zoneinfo,
pathlib, and sys modules from Python's standard library.
"""

from __future__ import annotations

import math
import random
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def demo_math_utilities() -> None:
    print("=" * 60)
    print("  1. Standard Library: math")
    print("=" * 60)

    hypotenuse = math.hypot(3.0, 4.0)  # sqrt(3^2 + 4^2) = 5.0
    gcd_val = math.gcd(48, 18)         # Greatest Common Divisor = 6
    log_val = math.log10(1000)         # log10(1000) = 3.0

    print(f"math.hypot(3, 4) : {hypotenuse}")
    print(f"math.gcd(48, 18) : {gcd_val}")
    print(f"math.log10(1000) : {log_val}")
    print(f"math.pi constant : {math.pi:.6f}")


def demo_random_generators() -> None:
    print("\n" + "=" * 60)
    print("  2. Standard Library: random")
    print("=" * 60)

    # Random integer in range [1, 20]
    dice_roll = random.randint(1, 20)
    print(f"D20 Dice Roll: {dice_roll}")

    # Random selection with weights (Weighted Loot Drop Simulation)
    loot_table = ["Common Iron Sword", "Rare Mystic Bow", "Legendary Dragon Armor"]
    drop_weights = [0.80, 0.18, 0.02]  # 80% common, 18% rare, 2% legendary
    loot_drop = random.choices(loot_table, weights=drop_weights, k=1)[0]
    print(f"Loot Drop Result: {loot_drop}")

    # Shuffling a list in-place
    cards = ["Ace", "King", "Queen", "Jack"]
    random.shuffle(cards)
    print(f"Shuffled Deck: {cards}")


def demo_datetime_and_timezones() -> None:
    print("\n" + "=" * 60)
    print("  3. Standard Library: datetime & zoneinfo")
    print("=" * 60)

    # Always use timezone.utc for server / system timestamps
    now_utc = datetime.now(UTC)
    print(f"UTC Timestamp       : {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Convert UTC to specific world timezones cleanly using zoneinfo
    ny_tz = ZoneInfo("America/New_York")
    ny_time = now_utc.astimezone(ny_tz)
    print(f"New York Time       : {ny_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    london_tz = ZoneInfo("Europe/London")
    london_time = now_utc.astimezone(london_tz)
    print(f"London Time         : {london_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")


def demo_pathlib_operations() -> None:
    print("\n" + "=" * 60)
    print("  4. Standard Library: pathlib (Modern Path Handling)")
    print("=" * 60)

    # Path objects replace messy string concatenations with the / operator
    current_dir = Path.cwd()
    sample_file = current_dir / "sample_test_file.tmp"

    print(f"Current Directory : {current_dir.name}")
    print(f"Target File Path  : {sample_file}")

    # Write text and read it back atomically
    sample_file.write_text("Hello from pathlib in Python 3!", encoding="utf-8")
    content = sample_file.read_text(encoding="utf-8")
    print(f"File Contents     : '{content}'")

    # Clean up temporary test file
    sample_file.unlink(missing_ok=True)
    print(f"File cleaned up successfully: {not sample_file.exists()}")


def main() -> None:
    demo_math_utilities()
    demo_random_generators()
    demo_datetime_and_timezones()
    demo_pathlib_operations()
    print("\n[Done] Standard Library Core Demonstration completed successfully!")


if __name__ == "__main__":
    main()
