"""Unit tests for TrieAndUnionFindEngine."""
from trie_and_union_find_engine import DisjointSetUnion, PrefixTrie


def test_trie_operations():
    trie = PrefixTrie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("banana")

    assert trie.search("apple")
    assert trie.search("app")
    assert not trie.search("appl")
    assert trie.starts_with("appl")
    assert trie.starts_with("ban")
    assert not trie.starts_with("cat")

def test_trie_wildcard_search():
    trie = PrefixTrie()
    trie.insert("bad")
    trie.insert("dad")
    trie.insert("mad")

    assert not trie.wildcard_search("pad")
    assert trie.wildcard_search("bad")
    assert trie.wildcard_search(".ad")
    assert trie.wildcard_search("b..")

def test_dsu_operations():
    dsu = DisjointSetUnion[int]()
    for i in range(1, 6):
        dsu.add(i)

    assert dsu.num_components() == 5
    assert dsu.union(1, 2)
    assert dsu.union(2, 3)
    assert dsu.connected(1, 3)
    assert not dsu.connected(1, 4)
    assert dsu.num_components() == 3

    # Redundant union returns False
    assert not dsu.union(1, 3)

def test_trie_empty_and_subwords():
    trie = PrefixTrie()
    assert not trie.search("anything")
    assert not trie.starts_with("a")
    trie.insert("")
    assert trie.search("")

def test_dsu_isolated_and_cycles():
    dsu = DisjointSetUnion[str]()
    dsu.add("X")
    assert dsu.num_components() == 1
    assert dsu.connected("X", "X")
    assert not dsu.connected("X", "Y")
def test_trie_prefix_and_wildcard_edge_cases():
    trie = PrefixTrie()
    assert not trie.search("any")
    assert not trie.starts_with("a")
    
    trie.insert("apple")
    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert trie.wildcard_search("a..le")
    assert not trie.wildcard_search("a...e.")


def test_dsu_redundant_and_components_edge_cases():
    dsu = DisjointSetUnion[int]()
    for i in range(5):
        dsu.add(i)
    assert dsu.num_components() == 5
    
    assert dsu.union(0, 1) is True
    assert dsu.num_components() == 4
    # Redundant union
    assert dsu.union(0, 1) is False
    assert dsu.num_components() == 4
    assert dsu.connected(0, 1) is True
    assert dsu.connected(0, 2) is False

