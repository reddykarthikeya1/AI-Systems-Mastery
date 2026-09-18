"""DEBUG LAB: Deadlock in Concurrent B+ Tree Node Split

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class BPlusNode:
    def __init__(self, keys: list[int]) -> None:
        self.keys = keys

class ToyBPlusTree:
    """A toy tree with one leaf, used to model a lock-coupling violation."""

    def __init__(self) -> None:
        self.child = BPlusNode([10, 20, 30, 40])
        self.sibling: BPlusNode | None = None

    def concurrent_split(self) -> BPlusNode:
        """A concurrent writer splits the leaf, moving the upper half of the
        keys into a brand-new sibling node."""
        mid = len(self.child.keys) // 2
        sibling = BPlusNode(self.child.keys[mid:])
        self.child.keys = self.child.keys[:mid]
        self.sibling = sibling
        return sibling

    def search_buggy(self, key: int) -> bool:
        # The parent latch is released and a reference to "the child" is
        # captured here -- before re-validating against a concurrent split:
        target_node = self.child
        # ...a split happens on another connection in this exact window...
        self.concurrent_split()
        # ...only now does this traversal acquire a latch and search, on a
        # reference that the split has already invalidated:
        return key in target_node.keys

def reproduce_defect() -> None:
    print("Searching for key 40 while another connection splits the same leaf...")
    tree = ToyBPlusTree()
    found = tree.search_buggy(40)
    still_in_tree = 40 in tree.child.keys or 40 in (tree.sibling.keys if tree.sibling else [])

    print(f"search_buggy(40) found the key: {found}")
    print(f"Key 40 actually still present somewhere in the tree: {still_in_tree}")
    if not found and still_in_tree:
        print("[DEFECT OBSERVED] The traversal silently lost key 40 -- it moved to "
              "the new sibling during the split, but the stale reference captured "
              "before the split was searched instead.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
