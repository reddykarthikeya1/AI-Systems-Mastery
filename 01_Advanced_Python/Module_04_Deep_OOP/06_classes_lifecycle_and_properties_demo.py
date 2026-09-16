#!/usr/bin/env python3
"""Module 04: Classes, Lifecycle & Properties Demonstration.

This script demonstrates __new__ vs __init__, class vs instance attributes,
@classmethod alternate constructors, @staticmethod, and @property validation.
"""

from __future__ import annotations


class Product:
    """Represents an e-commerce product with strict price properties."""

    store_name: str = "Global Marketplace"  # Class Variable

    def __init__(self, product_id: str, name: str, price: float) -> None:
        self.product_id = product_id  # Instance Variable
        self.name = name              # Instance Variable
        self.price = price            # Invokes @price.setter

    @property
    def price(self) -> float:
        """Getter for product price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Setter enforcing positive pricing rules."""
        if value <= 0:
            raise ValueError(f"Price must be greater than zero. Received: {value}")
        self._price = round(value, 2)

    @classmethod
    def from_formatted_string(cls, entry: str) -> Product:
        """Class method acting as an alternate factory constructor.

        Expected format: "ID-101: Laptop Pro : 1299.99"
        """
        parts = [p.strip() for p in entry.split(":")]
        if len(parts) != 3:
            raise ValueError(f"Invalid format '{entry}'. Expected 'ID:Name:Price'.")
        return cls(product_id=parts[0], name=parts[1], price=float(parts[2]))

    @staticmethod
    def is_valid_sku(sku: str) -> bool:
        """Static utility method checking SKU format."""
        return sku.startswith("SKU-") and len(sku) >= 8


def main() -> None:
    print("=" * 60)
    print("  1. Creating Products & Property Validation")
    print("=" * 60)

    p1 = Product("P-001", "Mechanical Keyboard", 120.50)
    print(f"Product: {p1.name} | Price: ${p1.price:.2f} | Store: {p1.store_name}")

    # Testing setter validation
    try:
        p1.price = -50.0
    except ValueError as e:
        print(f"[BLOCKED] Validation caught invalid price: {e}")

    print("\n" + "=" * 60)
    print("  2. Class Method Factory Constructors")
    print("=" * 60)
    p2 = Product.from_formatted_string("P-002 : Ultra-Wide Monitor : 450.00")
    print(f"Instantiated from string: {p2.product_id} - {p2.name} (${p2.price:.2f})")

    print("\n" + "=" * 60)
    print("  3. Static Method Utility")
    print("=" * 60)
    print(f"Is 'SKU-10928' valid? : {Product.is_valid_sku('SKU-10928')}")
    print(f"Is 'ITEM-12' valid?   : {Product.is_valid_sku('ITEM-12')}")


if __name__ == "__main__":
    main()
