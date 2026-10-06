from .models import Problem

def get_problems_31_45() -> list[Problem]:
    problems = []

    # ----------------------------------------------------
    # Problem 31: Same Tree
    # ----------------------------------------------------
    def trace_p31():
        out = [
            "Trees: p = [1, 2, 3], q = [1, 2, 3]",
            "Step 1: Check roots: p.val (1) == q.val (1) -> True",
            "Step 2: Check left subtrees: p.left.val (2) == q.left.val (2) -> True",
            "Step 3: Check right subtrees: p.right.val (3) == q.right.val (3) -> True",
            "Result: True (Both trees are structurally identical with equal values)"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=31,
        slug="p31_same_tree",
        title="Same Tree",
        category="Trees",
        difficulty="Easy",
        statement="Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        brute_force="Serialize both trees with null markers into strings and compare. Time: $O(N)$, Space: $O(N)$.",
        key_insight="Simultaneous DFS traversal: if both nodes are `None`, return `True`; if one is `None` or values differ, return `False`; recursively check both `(p.left, q.left)` and `(p.right, q.right)`.",
        func_name="is_same_tree",
        stub_code="""def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    \"\"\"Checks if two binary trees are identical in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    \"\"\"Checks if two binary trees are identical in O(N) time.\"\"\"
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
""",
        tests_code="""t1 = TreeNode(1, TreeNode(2), TreeNode(3))
t2 = TreeNode(1, TreeNode(2), TreeNode(3))
t3 = TreeNode(1, TreeNode(2), None)
assert is_same_tree(t1, t2) is True
assert is_same_tree(t1, t3) is False
assert is_same_tree(None, None) is True
""",
        time_complexity="$O(N)$ visiting every node at most once.",
        space_complexity="$O(H)$ recursion stack space.",
        follow_up="How to test if two trees are Symmetric Mirror Trees? Compare `(p.left, q.right)` and `(p.right, q.left)` simultaneously.",
        run_trace=trace_p31
    ))

    # ----------------------------------------------------
    # Problem 32: Subtree of Another Tree
    # ----------------------------------------------------
    def trace_p32():
        out = [
            "Root tree: [3, 4, 5, 1, 2], Subtree: [4, 1, 2]",
            "Step 1: Check root node (3) vs subRoot (4) -> values differ (3 != 4)",
            "Step 2: Check left child (4) vs subRoot (4) -> values match!",
            "Step 3: Run is_same_tree on left child: left (1) == 1, right (2) == 2 -> True",
            "Subtree found at node 4: True"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=32,
        slug="p32_subtree_of_another_tree",
        title="Subtree of Another Tree",
        category="Trees",
        difficulty="Easy",
        statement="Given the roots of two binary trees `root` and `subRoot`, return `True` if there is a subtree of `root` with the same structure and node values of `subRoot` and `False` otherwise.",
        brute_force="For every node in `root`, check if the subtree starting there is identical to `subRoot` using `is_same_tree`. Time: $O(N \\cdot M)$, Space: $O(H)$.",
        key_insight="Traverse `root` with DFS. If `is_same_tree(root, subRoot)` is true, return `True`; otherwise, search recursively in `root.left` or `root.right`.",
        func_name="is_subtree",
        stub_code="""def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    \"\"\"Checks if sub_root is a subtree of root.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    \"\"\"Checks if sub_root is a subtree of root.\"\"\"
    def is_same(p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return is_same(p.left, q.left) and is_same(p.right, q.right)

    if not sub_root:
        return True
    if not root:
        return False
    if is_same(root, sub_root):
        return True
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
""",
        tests_code="""root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))
sub = TreeNode(4, TreeNode(1), TreeNode(2))
assert is_subtree(root, sub) is True
root_extra = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2, TreeNode(0))), TreeNode(5))
assert is_subtree(root_extra, sub) is False
assert is_subtree(None, None) is True
""",
        time_complexity="$O(N \\cdot M)$ where $N$ and $M$ are node counts.",
        space_complexity="$O(H)$ recursion call stack.",
        follow_up="How to achieve $O(N + M)$ strictly linear time? Serialize both trees using pre-order traversal with distinct null and delimiter tokens, then run KMP (Knuth-Morris-Pratt) string search.",
        run_trace=trace_p32
    ))

    # ----------------------------------------------------
    # Problem 33: Lowest Common Ancestor of a BST
    # ----------------------------------------------------
    def trace_p33():
        out = [
            "BST Root: 6, p = 2, q = 8",
            "Check root 6:",
            "  p.val (2) < 6 and q.val (8) > 6",
            "  Since p is in left subtree and q is in right subtree, paths diverge!",
            "Lowest Common Ancestor is node 6."
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=33,
        slug="p33_lowest_common_ancestor_of_a_bst",
        title="Lowest Common Ancestor of a BST",
        category="Trees",
        difficulty="Medium",
        statement="Given a Binary Search Tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.",
        brute_force="Find root-to-node paths for both nodes and compare paths to find divergence point. Time: $O(N)$, Space: $O(H)$.",
        key_insight="Exploit BST ordering property: if both values are less than `curr.val`, LCA must be in left subtree; if both are greater, LCA must be in right subtree. The moment they split (or one equals `curr.val`), `curr` is the LCA!",
        func_name="lowest_common_ancestor",
        stub_code="""def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    \"\"\"Finds LCA in a BST in O(H) time and O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    \"\"\"Finds LCA in a BST in O(H) time and O(1) space.\"\"\"
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return root
""",
        tests_code="""r = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))), TreeNode(8, TreeNode(7), TreeNode(9)))
assert lowest_common_ancestor(r, TreeNode(2), TreeNode(8)).val == 6
assert lowest_common_ancestor(r, TreeNode(2), TreeNode(4)).val == 2
assert lowest_common_ancestor(r, TreeNode(3), TreeNode(5)).val == 4
""",
        time_complexity="$O(H)$ where $H$ is BST height ($O(\\log N)$ balanced).",
        space_complexity="$O(1)$ iterative traversal.",
        follow_up="What if the tree is an arbitrary Binary Tree (not a BST)? Use post-order DFS: return node if it matches $p$ or $q$; if both left and right return non-null, current node is LCA.",
        run_trace=trace_p33
    ))

    # ----------------------------------------------------
    # Problem 34: Binary Tree Level Order Traversal
    # ----------------------------------------------------
    def trace_p34():
        out = [
            "Tree: [3, 9, 20, null, null, 15, 7]",
            f"{'Level':<6} | {'Queue before level':<25} | {'Extracted Level Values':<25}",
            "-" * 60,
            f"{'0':<6} | {'[3]':<25} | {'[3]':<25}",
            f"{'1':<6} | {'[9, 20]':<25} | {'[9, 20]':<25}",
            f"{'2':<6} | {'[15, 7]':<25} | {'[15, 7]':<25}",
            "Result: [[3], [9, 20], [15, 7]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=34,
        slug="p34_binary_tree_level_order_traversal",
        title="Binary Tree Level Order Traversal",
        category="Trees",
        difficulty="Medium",
        statement="Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
        brute_force="Calculate depth of tree, then for each depth $d$, traverse from root collecting nodes at depth $d$. Time: $O(N^2)$, Space: $O(N)$.",
        key_insight="Use a FIFO Queue (BFS). In each iteration of the outer loop, record `level_size = len(queue)` and process exactly that many nodes to group them by layer.",
        func_name="level_order",
        stub_code="""def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    \"\"\"Performs level-order BFS traversal in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""from collections import deque

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    \"\"\"Performs level-order BFS traversal in O(N) time.\"\"\"
    if not root:
        return []
        
    res = []
    q = deque([root])
    
    while q:
        level_size = len(q)
        current_level = []
        for _ in range(level_size):
            node = q.popleft()
            current_level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(current_level)
        
    return res
""",
        tests_code="""root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert level_order(root) == [[3], [9, 20], [15, 7]]
assert level_order(TreeNode(1)) == [[1]]
assert level_order(None) == []
""",
        time_complexity="$O(N)$ visiting every node exactly once.",
        space_complexity="$O(N)$ queue holds at most $N/2$ nodes at bottom level.",
        follow_up="How to output zigzag level order traversal (alternating left-right and right-left)? Reverse alternate level lists or append to a double-ended queue using a parity flag.",
        run_trace=trace_p34
    ))

    # ----------------------------------------------------
    # Problem 35: Validate Binary Search Tree
    # ----------------------------------------------------
    def trace_p35():
        out = [
            "Tree: [5, 1, 4, null, null, 3, 6]",
            "DFS bounds checking (low, high):",
            "  Root node 5: valid in (-inf, inf)",
            "  Left child 1: valid in (-inf, 5)",
            "  Right child 4: valid in (5, inf)?",
            "    4 is NOT > 5! Invalid BST violation detected!",
            "Result: False"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=35,
        slug="p35_validate_binary_search_tree",
        title="Validate Binary Search Tree",
        category="Trees",
        difficulty="Medium",
        statement="Given the `root` of a binary tree, determine if it is a valid binary search tree (BST). A valid BST requires all left subtree values to be strictly less than node value, and all right subtree values strictly greater.",
        brute_force="Only checking `node.left.val < node.val < node.right.val` locally fails because a node deep in the left subtree could violate the root's value.",
        key_insight="Pass valid value boundaries `(low, high)` down the DFS recursion. When going left, update `high = node.val`; when going right, update `low = node.val`.",
        func_name="is_valid_bst",
        stub_code="""def is_valid_bst(root: Optional[TreeNode]) -> bool:
    \"\"\"Validates BST in O(N) time by propagating valid range bounds.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_valid_bst(root: Optional[TreeNode]) -> bool:
    \"\"\"Validates BST in O(N) time by propagating valid range bounds.\"\"\"
    def validate(node, low=float("-inf"), high=float("inf")):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        
    return validate(root)
""",
        tests_code="""valid_t = TreeNode(2, TreeNode(1), TreeNode(3))
assert is_valid_bst(valid_t) is True
invalid_t = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
assert is_valid_bst(invalid_t) is False
assert is_valid_bst(TreeNode(1, TreeNode(1))) is False # Strict inequality
assert is_valid_bst(None) is True
""",
        time_complexity="$O(N)$ visiting every node once.",
        space_complexity="$O(H)$ recursion call stack space.",
        follow_up="Could this be verified using in-order traversal? Yes, an in-order traversal of a valid BST must produce a strictly increasing sequence with $prev < curr$.",
        run_trace=trace_p35
    ))

    # ----------------------------------------------------
    # Problem 36: Kth Smallest Element in a BST
    # ----------------------------------------------------
    def trace_p36():
        out = [
            "BST: [3, 1, 4, null, 2], k = 1",
            "In-order traversal sequence (Left -> Root -> Right):",
            "  1. Visit 1 (Smallest: count = 1 == k) -> Target reached!",
            "Kth smallest value: 1"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=36,
        slug="p36_kth_smallest_element_in_a_bst",
        title="Kth Smallest Element in a BST",
        category="Trees",
        difficulty="Medium",
        statement="Given the `root` of a binary search tree, and an integer `k`, return the $k^{\\text{th}}$ smallest value (1-indexed) of all the values of the nodes in the tree.",
        brute_force="Dump all node values into an array, sort it, and return index $k-1$. Time: $O(N \\log N)$, Space: $O(N)$.",
        key_insight="In-order traversal (`Left -> Root -> Right`) of a BST yields keys in strictly sorted ascending order. Stop early as soon as the $k^{\\text{th}}$ node is visited.",
        func_name="kth_smallest",
        stub_code="""def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    \"\"\"Finds kth smallest element in BST using in-order traversal.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    \"\"\"Finds kth smallest element in BST using in-order traversal.\"\"\"
    stack = []
    curr = root
    
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
        
    return -1
""",
        tests_code="""t1 = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
assert kth_smallest(t1, 1) == 1
t2 = TreeNode(5, TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4)), TreeNode(6))
assert kth_smallest(t2, 3) == 3
""",
        time_complexity="$O(H + k)$ time where $H$ is tree height.",
        space_complexity="$O(H)$ stack space.",
        follow_up="What if the BST is modified frequently (often searched and updated)? Store the count of nodes in the left subtree at each node (Order Statistic Tree), enabling $O(H)$ lookups.",
        run_trace=trace_p36
    ))

    # ----------------------------------------------------
    # Problem 37: Construct Binary Tree from Preorder and Inorder Traversal
    # ----------------------------------------------------
    def trace_p37():
        preorder = [3, 9, 20, 15, 7]
        inorder = [9, 3, 15, 20, 7]
        out = [
            f"Preorder: {preorder}, Inorder: {inorder}",
            "Step 1: First element of preorder is root = 3",
            "Step 2: Find index of 3 in inorder -> index 1",
            "  Left subtree inorder: [9] (size 1) -> preorder: [9]",
            "  Right subtree inorder: [15, 20, 7] (size 3) -> preorder: [20, 15, 7]",
            "Step 3: Recursively construct left child (9) and right child (20 with children 15, 7)",
            "Result: Reconstructed root 3"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=37,
        slug="p37_construct_binary_tree_from_preorder_and_inorder_traversal",
        title="Construct Binary Tree from Preorder and Inorder Traversal",
        category="Trees",
        difficulty="Medium",
        statement="Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.",
        brute_force="Recursively search for root in `inorder` using linear scans: $O(N^2)$ time.",
        key_insight="The first element of `preorder` is always the root. Locating this root in `inorder` splits elements into left and right subtrees. Cache `inorder` index locations in a hash map for $O(1)$ lookups, yielding $O(N)$ total time.",
        func_name="build_tree",
        stub_code="""def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    \"\"\"Reconstructs binary tree in O(N) time using index map.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    \"\"\"Reconstructs binary tree in O(N) time using index map.\"\"\"
    in_map = {val: idx for idx, val in enumerate(inorder)}
    pre_idx = 0
    
    def helper(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre_idx
        if left > right:
            return None
            
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        
        mid = in_map[root_val]
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root
        
    return helper(0, len(inorder) - 1)
""",
        tests_code="""t = build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
assert t.val == 3
assert t.left.val == 9
assert t.right.val == 20
assert t.right.left.val == 15
assert build_tree([-1], [-1]).val == -1
assert build_tree([], []) is None
""",
        time_complexity="$O(N)$ linear time to build $N$ nodes.",
        space_complexity="$O(N)$ for hash map and recursion stack.",
        follow_up="Can a binary tree be uniquely constructed from Preorder and Postorder traversals? Not in general (unless every non-leaf node has exactly two children).",
        run_trace=trace_p37
    ))

    # ----------------------------------------------------
    # Problem 38: Binary Tree Maximum Path Sum
    # ----------------------------------------------------
    def trace_p38():
        out = [
            "Tree: [-10, 9, 20, null, null, 15, 7]",
            "Post-order traversal computing max gains:",
            "  Node 15: gain = 15, max path through 15 = 15",
            "  Node 7:  gain = 7,  max path through 7 = 7",
            "  Node 20: max path through 20 = 20 + 15 + 7 = 42 (New Global Max!)",
            "           gain to parent = 20 + max(15, 7) = 35",
            "  Node 9:  gain = 9,  max path through 9 = 9",
            "  Node -10: max path through -10 = -10 + 9 + 35 = 34",
            "Global Maximum Path Sum: 42"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=38,
        slug="p38_binary_tree_maximum_path_sum",
        title="Binary Tree Maximum Path Sum",
        category="Trees",
        difficulty="Hard",
        statement="A path in a binary tree is a sequence of nodes where each pair of adjacent nodes has an edge connecting them. Return the maximum path sum of any non-empty path.",
        brute_force="Find all pairs of nodes and sum values along the path between them. Time: $O(N^2)$, Space: $O(N)$.",
        key_insight="Post-order Tree DP: at each node $N$, compute $\\text{left\\_gain} = \\max(0, \\text{dfs}(N.\\text{left}))$ and $\\text{right\\_gain} = \\max(0, \\text{dfs}(N.\\text{right}))$. The local peak path is $N.\\text{val} + \\text{left\\_gain} + \\text{right\\_gain}$. Return $N.\\text{val} + \\max(\\text{left\\_gain}, \\text{right\\_gain})$ to the caller.",
        func_name="max_path_sum",
        stub_code="""def max_path_sum(root: Optional[TreeNode]) -> int:
    \"\"\"Computes maximum path sum in O(N) time and O(H) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def max_path_sum(root: Optional[TreeNode]) -> int:
    \"\"\"Computes maximum path sum in O(N) time and O(H) space.\"\"\"
    max_sum = float("-inf")
    
    def gain(node: Optional[TreeNode]) -> int:
        nonlocal max_sum
        if not node:
            return 0
            
        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)
        
        current_path_sum = node.val + left_gain + right_gain
        max_sum = max(max_sum, current_path_sum)
        
        return node.val + max(left_gain, right_gain)
        
    gain(root)
    return int(max_sum)
""",
        tests_code="""root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_path_sum(root) == 42
assert max_path_sum(TreeNode(-3)) == -3
assert max_path_sum(TreeNode(1, TreeNode(2), TreeNode(3))) == 6
""",
        time_complexity="$O(N)$ visiting every node once.",
        space_complexity="$O(H)$ recursion call stack space.",
        follow_up="What if all values in the tree are negative? Clamping gains to 0 allows the algorithm to pick the single largest negative node rather than accumulating negative sums.",
        run_trace=trace_p38
    ))

    # ----------------------------------------------------
    # Problem 39: Implement Trie (Prefix Tree)
    # ----------------------------------------------------
    def trace_p39():
        out = [
            "Commands: insert('apple'), search('apple'), search('app'), startsWith('app')",
            "1. insert('apple'):",
            "   root -> 'a' -> 'p' -> 'p' -> 'l' -> 'e' (is_end = True)",
            "2. search('apple'): path found and is_end is True -> True",
            "3. search('app'): path found but is_end is False -> False",
            "4. startsWith('app'): prefix path exists -> True"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=39,
        slug="p39_implement_trie",
        title="Implement Trie (Prefix Tree)",
        category="Tries",
        difficulty="Medium",
        statement="A trie (pronounced 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement `insert`, `search`, and `starts_with` methods.",
        brute_force="Store strings in a list: `insert` is $O(1)$, but `search` and `starts_with` require $O(N \\cdot L)$ scans across all words.",
        key_insight="Each node contains a map of child nodes `children: dict[str, TrieNode]` and boolean `is_end`. Traversal follows character edges in $O(L)$ time independent of the number of words stored.",
        func_name="trie",
        stub_code="""class Trie:
    def __init__(self):
        raise NotImplementedError
    def insert(self, word: str) -> None:
        raise NotImplementedError
    def search(self, word: str) -> bool:
        raise NotImplementedError
    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError
""",
        solution_code="""class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True
""",
        tests_code="""t = Trie()
t.insert("apple")
assert t.search("apple") is True
assert t.search("app") is False
assert t.starts_with("app") is True
t.insert("app")
assert t.search("app") is True
""",
        time_complexity="$O(L)$ for each operation where $L$ is word length.",
        space_complexity="$O(N \\cdot L)$ in worst case with no shared prefixes.",
        follow_up="How to optimize memory in memory-constrained environments? Use a Radix Tree (Patricia Trie) which compacts non-branching paths into single multi-character edges.",
        run_trace=trace_p39
    ))

    # ----------------------------------------------------
    # Problem 40: Design Add and Search Words Data Structure
    # ----------------------------------------------------
    def trace_p40():
        out = [
            "Words added: 'bad', 'dad', 'mad'",
            "Search '.ad':",
            "  char '.' -> branch across all root children: 'b', 'd', 'm'",
            "  Branch 'b': matches 'a' -> 'd' (is_end = True) -> Matched!",
            "Result: True"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=40,
        slug="p40_design_add_and_search_words_data_structure",
        title="Design Add and Search Words Data Structure",
        category="Tries",
        difficulty="Medium",
        statement="Design a data structure that supports adding new words and finding if a string matches any previously added string, where `.` can represent any letter.",
        brute_force="Maintain a list and test with regular expressions on every search query. Time: $O(N \\cdot L)$ per search.",
        key_insight="Store words in a Trie. For exact characters, traverse the specific child node. When encountering `.`, branch DFS across all child nodes at the current level.",
        func_name="word_dictionary",
        stub_code="""class WordDictionary:
    def __init__(self):
        raise NotImplementedError
    def add_word(self, word: str) -> None:
        raise NotImplementedError
    def search(self, word: str) -> bool:
        raise NotImplementedError
""",
        solution_code="""class WordNode:
    def __init__(self):
        self.children: dict[str, WordNode] = {}
        self.is_end: bool = False

class WordDictionary:
    def __init__(self):
        self.root = WordNode()

    def add_word(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = WordNode()
            curr = curr.children[ch]
        curr.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: WordNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            ch = word[idx]
            if ch != '.':
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], idx + 1)
            else:
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
        return dfs(self.root, 0)
""",
        tests_code="""wd = WordDictionary()
wd.add_word("bad")
wd.add_word("dad")
wd.add_word("mad")
assert wd.search("pad") is False
assert wd.search("bad") is True
assert wd.search(".ad") is True
assert wd.search("b..") is True
""",
        time_complexity="$O(L)$ for `add_word`; $O(26^L)$ worst-case for search with all dots, $O(L)$ average case.",
        space_complexity="$O(N \\cdot L)$ to store words in the Trie.",
        follow_up="How to prevent worst-case exponential slowdown on searches like `\"....\"`? Group words by length in separate Tries or hash maps.",
        run_trace=trace_p40
    ))

    # ----------------------------------------------------
    # Problem 41: Word Search II
    # ----------------------------------------------------
    def trace_p41():
        out = [
            "Board: [['o','a','a','n'],['e','t','a','e'],['i','h','k','r'],['i','f','l','v']]",
            "Words: ['oath', 'pea', 'eat', 'rain']",
            "1. Insert words into Trie: ['oath', 'pea', 'eat', 'rain']",
            "2. Backtrack DFS starting from board[0][0]='o':",
            "   Trie path: 'o' -> 'a' -> 't' -> 'h' (Matched word 'oath'!)",
            "3. Prune 'oath' from Trie to prevent duplicate matches.",
            "Found words: ['oath', 'eat']"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=41,
        slug="p41_word_search_ii",
        title="Word Search II",
        category="Tries",
        difficulty="Hard",
        statement="Given an $m \\times n$ `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from sequentially adjacent cells.",
        brute_force="Run standard Word Search I for each word in `words`. Time: $O(W \\cdot M \\cdot N \\cdot 4^L)$.",
        key_insight="Build a Trie of all target words. Run DFS on the board once, traversing the Trie simultaneously. Prune leaf nodes from the Trie when a word is discovered to optimize subsequent searches.",
        func_name="find_words",
        stub_code="""def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    \"\"\"Finds all words on board using Trie-guided backtracking DFS.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    \"\"\"Finds all words on board using Trie-guided backtracking DFS.\"\"\"
    trie: dict = {}
    for word in words:
        curr = trie
        for ch in word:
            curr = curr.setdefault(ch, {})
        curr["$"] = word
        
    rows, cols = len(board), len(board[0])
    res = []
    
    def dfs(r: int, c: int, parent: dict):
        ch = board[r][c]
        curr_node = parent[ch]
        
        if "$" in curr_node:
            res.append(curr_node.pop("$"))
            
        board[r][c] = "#"  # Mark visited
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in curr_node:
                dfs(nr, nc, curr_node)
        board[r][c] = ch   # Backtrack
        
        # Leaf pruning optimization
        if not curr_node:
            parent.pop(ch)
            
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in trie:
                dfs(r, c, trie)
                
    return res
""",
        tests_code="""b = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
w = ["oath","pea","eat","rain"]
assert sorted(find_words(b, w)) == sorted(["eat", "oath"])
b2 = [["a","b"],["c","d"]]
assert find_words(b2, ["abcd"]) == []
""",
        time_complexity="$O(M \\cdot N \\cdot 4^L)$ where $L$ is maximum word length.",
        space_complexity="$O(\\sum L)$ space to store all words in Trie.",
        follow_up="Why is leaf pruning crucial? Once a leaf word is found, pruning that path prevents future DFS explorations from retreading dead-end branches.",
        run_trace=trace_p41
    ))

    # ----------------------------------------------------
    # Problem 42: Kth Largest Element in an Array
    # ----------------------------------------------------
    def trace_p42():
        nums, k = [3, 2, 1, 5, 6, 4], 2
        import heapq
        heap = []
        out = [
            f"Input: nums = {nums}, k = {k}",
            f"{'Step':<5} | {'num':<5} | {'Min-Heap of size k (<= 2)':<25} | {'Action':<15}",
            "-" * 55
        ]
        for i, num in enumerate(nums):
            if len(heap) < k:
                heapq.heappush(heap, num)
                action = "Push into heap"
            elif num > heap[0]:
                heapq.heappushpop(heap, num)
                action = f"Replace top {heap[0]} with {num}"
            else:
                action = "Ignore (< top)"
            out.append(f"{i+1:<5} | {num:<5} | {str(heap):<25} | {action:<15}")
        out.append(f"Top of min-heap is {k}th largest: {heap[0]}")
        return "\n".join(out)

    problems.append(Problem(
        id=42,
        slug="p42_kth_largest_element_in_an_array",
        title="Kth Largest Element in an Array",
        category="Heap / Priority Queue",
        difficulty="Medium",
        statement="Given an integer array `nums` and an integer `k`, return the $k^{\\text{th}}$ largest element in the array. Note that it is the $k^{\\text{th}}$ largest element in sorted order, not the $k^{\\text{th}}$ distinct element.",
        brute_force="Sort the entire array in descending order and return `nums[k-1]`. Time: $O(N \\log N)$, Space: $O(1)$ or $O(N)$.",
        key_insight="Maintain a **Min-Heap of size $k$**. As elements are processed, push to heap and pop smallest when size exceeds $k$. At the end, the root of the min-heap holds the $k^{\\text{th}}$ largest element.",
        func_name="find_kth_largest",
        stub_code="""def find_kth_largest(nums: list[int], k: int) -> int:
    \"\"\"Finds kth largest element using min-heap in O(N log k) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    \"\"\"Finds kth largest element using min-heap in O(N log k) time.\"\"\"
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
""",
        tests_code="""assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
assert find_kth_largest([1], 1) == 1
""",
        time_complexity="$O(N \\log k)$ maintaining a size-$k$ heap.",
        space_complexity="$O(k)$ auxiliary space for the heap.",
        follow_up="Can this be solved in $O(N)$ average time? Yes, using QuickSelect (Hoare's selection algorithm) with randomized partitioning.",
        run_trace=trace_p42
    ))

    # ----------------------------------------------------
    # Problem 43: Find Median from Data Stream
    # ----------------------------------------------------
    def trace_p43():
        out = [
            "Stream operations: addNum(1), addNum(2), findMedian() -> 1.5, addNum(3), findMedian() -> 2.0",
            "State breakdown:",
            "  1. addNum(1): small(max-heap)=[-1], large(min-heap)=[] -> median = 1.0",
            "  2. addNum(2): small=[-1], large=[2] -> sizes equal, median = (1+2)/2 = 1.5",
            "  3. addNum(3): small=[-2, -1], large=[3] -> size 3, small has extra -> median = 2.0"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=43,
        slug="p43_find_median_from_data_stream",
        title="Find Median from Data Stream",
        category="Heap / Priority Queue",
        difficulty="Hard",
        statement="The median is the middle value in an ordered integer list. Design a data structure that supports adding numbers from a data stream and finding the median of all elements so far.",
        brute_force="Maintain a sorted list via insertion sort. `addNum` takes $O(N)$ time; `findMedian` takes $O(1)$ time.",
        key_insight="Use two heaps: a **Max-Heap** `small` for lower half and a **Min-Heap** `large` for upper half. Maintain size balance such that `0 <= len(small) - len(large) <= 1`. Then median is either root of `small` or the average of roots in $O(1)$.",
        func_name="median_finder",
        stub_code="""class MedianFinder:
    def __init__(self):
        raise NotImplementedError
    def add_num(self, num: int) -> None:
        raise NotImplementedError
    def find_median(self) -> float:
        raise NotImplementedError
""",
        solution_code="""import heapq

class MedianFinder:
    def __init__(self):
        self.small: list[int] = []  # Max-heap (store negated numbers)
        self.large: list[int] = []  # Min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        
        # Ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Maintain size invariant: len(small) == len(large) or len(small) == len(large) + 1
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
""",
        tests_code="""mf = MedianFinder()
mf.add_num(1)
mf.add_num(2)
assert mf.find_median() == 1.5
mf.add_num(3)
assert mf.find_median() == 2.0
""",
        time_complexity="$O(\\log N)$ for `add_num`; $O(1)$ for `find_median`.",
        space_complexity="$O(N)$ memory to store stream elements.",
        follow_up="What if all integers in stream are bounded in range $[0, 100]$? Use a frequency count array of size 101; `add_num` takes $O(1)$ and median calculation takes $O(100) = O(1)$ scans.",
        run_trace=trace_p43
    ))

    # ----------------------------------------------------
    # Problem 44: Combination Sum
    # ----------------------------------------------------
    def trace_p44():
        candidates = [2, 3, 6, 7]
        target = 7
        out = [
            f"Input: candidates = {candidates}, target = {target}",
            "Backtracking exploration tree:",
            "  Path [2, 2, 2]: remaining = 1 (< 2 -> backtrack)",
            "  Path [2, 2, 3]: remaining = 0 -> Matched [2, 2, 3]!",
            "  Path [2, 3]: remaining = 2 (< 3 for branch -> backtrack)",
            "  Path [7]: remaining = 0 -> Matched [7]!",
            "Unique combinations summing to 7: [[2, 2, 3], [7]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=44,
        slug="p44_combination_sum",
        title="Combination Sum",
        category="Backtracking",
        difficulty="Medium",
        statement="Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. The same number may be chosen unlimited times.",
        brute_force="Generate all possible multisets up to target length and check sums. Exponential: $O(2^N)$ or worse.",
        key_insight="Depth-First Search (DFS) Backtracking: at index $i$, either include `candidates[i]` (staying at index $i$ to allow reuse) or advance to $i+1$ (exclude `candidates[i]`). Prune when `current_sum > target`.",
        func_name="combination_sum",
        stub_code="""def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    \"\"\"Finds all unique combinations that sum to target using backtracking.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    \"\"\"Finds all unique combinations that sum to target using backtracking.\"\"\"
    res: list[list[int]] = []
    
    def backtrack(start: int, comb: list[int], remain: int):
        if remain == 0:
            res.append(list(comb))
            return
        if remain < 0:
            return
            
        for i in range(start, len(candidates)):
            comb.append(candidates[i])
            backtrack(i, comb, remain - candidates[i])
            comb.pop()
            
    backtrack(0, [], target)
    return res
""",
        tests_code="""assert sorted(combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
assert sorted(combination_sum([2, 3, 5], 8)) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert combination_sum([2], 1) == []
""",
        time_complexity="$O(N^{\\frac{T}{M}})$ where $T$ is target and $M$ is minimal candidate value.",
        space_complexity="$O(\\frac{T}{M})$ recursion stack depth.",
        follow_up="What if each number can be used at most once and duplicates exist in candidates (Combination Sum II)? Sort candidates and skip adjacent duplicates: `if i > start and candidates[i] == candidates[i-1]: continue`.",
        run_trace=trace_p44
    ))

    # ----------------------------------------------------
    # Problem 45: Word Search
    # ----------------------------------------------------
    def trace_p45():
        board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
        word = "ABCCED"
        out = [
            f"Board: {board}",
            f"Target word: '{word}'",
            "DFS search steps:",
            "  Start at (0, 0) 'A' -> matched char 0",
            "  Move right to (0, 1) 'B' -> matched char 1",
            "  Move right to (0, 2) 'C' -> matched char 2",
            "  Move down to (1, 2) 'C' -> matched char 3",
            "  Move down to (2, 2) 'E' -> matched char 4",
            "  Move left to (2, 1) 'D' -> matched char 5 (Word complete!)",
            "Result: True"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=45,
        slug="p45_word_search",
        title="Word Search",
        category="Backtracking",
        difficulty="Medium",
        statement="Given an $m \\times n$ grid of characters `board` and a string `word`, return `True` if `word` exists in the grid. The word can be constructed from sequentially adjacent cells horizontally or vertically. The same cell may not be used more than once.",
        brute_force="Generate all self-avoiding paths of length $L$ in the grid: $O(M \\cdot N \\cdot 4^L)$.",
        key_insight="Explore with Backtracking DFS. In-place mark visited cell by temporarily setting `board[r][c] = '#'` and restoring it on backtracking. Terminate immediately upon full word match.",
        func_name="exist",
        stub_code="""def exist(board: list[list[str]], word: str) -> bool:
    \"\"\"Checks if word exists on board using DFS backtracking.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def exist(board: list[list[str]], word: str) -> bool:
    \"\"\"Checks if word exists on board using DFS backtracking.\"\"\"
    rows, cols = len(board), len(board[0])
    
    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
            
        temp = board[r][c]
        board[r][c] = "#"
        
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
                 
        board[r][c] = temp
        return found
        
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
""",
        tests_code="""b = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
assert exist(b, "ABCCED") is True
assert exist(b, "SEE") is True
assert exist(b, "ABCB") is False
""",
        time_complexity="$O(M \\cdot N \\cdot 3^L)$ because after the initial step we do not turn backwards.",
        space_complexity="$O(L)$ recursion call stack space where $L$ is word length.",
        follow_up="How to prune searches before starting? Count character frequencies in the board vs `word`. If the board lacks sufficient frequency for any character, return `False` immediately.",
        run_trace=trace_p45
    ))

    return problems
