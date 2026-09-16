"""
Module 24: Columnar In-Memory Mini Query Engine
Run: python try_it_yourself.py
"""


class MiniDataFrame:
    def __init__(self, data):
        self.data = data

    def filter_gt(self, column, threshold):
        indices = [i for i, val in enumerate(self.data[column]) if val > threshold]
        return {col: [self.data[col][i] for i in indices] for col in self.data}


def main():
    print("=" * 60)
    print("  MODULE 24: COLUMNAR DATA ENGINE PLAYGROUND [*]")
    print("=" * 60)

    dataset = {
        "product": ["Monitor", "Mouse", "Keyboard", "Laptop"],
        "price": [250.0, 25.0, 75.0, 1200.0],
        "inventory": [12, 150, 45, 8],
    }

    df = MiniDataFrame(dataset)
    print("Filtering items with price > $50.00:")
    filtered = df.filter_gt("price", 50.0)

    for i in range(len(filtered["product"])):
        print(f"  {filtered['product'][i]}: ${filtered['price'][i]:.2f} (Stock: {filtered['inventory'][i]})")

    print("\n[OK] Columnar filter executed cleanly!")


if __name__ == "__main__":
    main()
