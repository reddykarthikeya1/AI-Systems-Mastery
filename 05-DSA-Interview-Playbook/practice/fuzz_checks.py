"""Randomized cross-checks against brute-force references (see run() for the covered problems).

Used by run_tests.py --fuzz and --stub. Each check feeds random inputs to the
candidate function and compares with an independent brute-force implementation.
"""
import copy, functools, glob, importlib.util, itertools, collections, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = {"dir": os.environ.get("DSA_SRC_DIR") or os.path.join(HERE, "solutions")}
ONLY = os.environ.get("DSA_ONLY", "")


def load(n):
    f = glob.glob(os.path.join(SOURCE["dir"], f"p{n:02d}_*.py"))[0]
    s = importlib.util.spec_from_file_location(f"p{n}", f)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


R = random.Random(7)
res = {}
def T(n, fn, gen, ref, cmp=lambda a, b: a == b, iters=300):
    if ONLY and str(n) != ONLY:
        return
    m = load(n)
    f = fn(m) if callable(fn) else getattr(m, fn)
    bad = 0
    ex = None
    for _ in range(iters):
        args = gen()
        try:
            a = f(*copy.deepcopy(args))
        except Exception as e:
            a = ("EXC", repr(e)[:60])
        b = ref(*args)
        if not cmp(a, b):
            bad += 1
            ex = ex or (args, a, b)
    res[n] = (fn, bad, ex)


ri = lambda lo, hi, n: [R.randint(lo, hi) for _ in range(n)]
S = lambda: "".join(R.choice("abc") for _ in range(R.randint(0, 7)))


def ref_trap(h):
    return sum(max(0, min(max(h[: i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))


T(12, "trap_rain_water", lambda: (ri(0, 6, R.randint(1, 12)),), ref_trap)


def ref_lsub(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for c in s[i:]:
            if c in seen:
                break
            seen.add(c)
        best = max(best, len(seen))
    return best


T(14, "length_of_longest_substring", lambda: ("".join(R.choice("abc") for _ in range(R.randint(0, 10))),), ref_lsub)


def ref_mw(s, t):
    c = collections.Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            cc = collections.Counter(s[i:j])
            if all(cc[k] >= v for k, v in c.items()) and (best == "" or j - i < len(best)):
                best = s[i:j]
    return best


T(16, "min_window", lambda: ("".join(R.choice("abc") for _ in range(R.randint(1, 9))), "".join(R.choice("abc") for _ in range(R.randint(1, 3)))), ref_mw, lambda a, b: isinstance(a, str) and len(a) == len(b))


def ref_hist(h):
    return max(min(h[i:j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h) + 1))


T(19, "largest_rectangle_area", lambda: (ri(0, 6, R.randint(1, 9)),), ref_hist)


def gen21():
    n = R.randint(1, 9)
    a = sorted(R.sample(range(30), n))
    k = R.randint(0, n - 1)
    return (a[k:] + a[:k], R.randint(0, 30))


T(21, "search_rotated", gen21, lambda a, t: a.index(t) if t in a else -1)


def gen22():
    n = R.randint(1, 9)
    a = sorted(R.sample(range(30), n))
    k = R.randint(0, n - 1)
    return (a[k:] + a[:k],)


T(22, "find_min", gen22, lambda a: min(a))
T(42, "find_kth_largest", lambda: (lambda a: (a, R.randint(1, len(a))))(ri(-5, 9, R.randint(1, 10))), lambda a, k: sorted(a, reverse=True)[k - 1])


def ref_cs(c, t):
    out = set()

    def go(i, rem, cur):
        if rem == 0:
            out.add(tuple(cur))
            return
        if rem < 0 or i == len(c):
            return
        go(i, rem - c[i], cur + [c[i]])
        go(i + 1, rem, cur)

    go(0, t, [])
    return out


T(44, "combination_sum", lambda: (sorted(R.sample(range(1, 8), R.randint(1, 4))), R.randint(1, 12)), ref_cs, lambda a, b: {tuple(x) for x in a} == b, 200)
T(46, "subsets", lambda: (R.sample(range(10), R.randint(0, 5)),), lambda a: {tuple(sorted(x)) for r in range(len(a) + 1) for x in itertools.combinations(a, r)}, lambda a, b: {tuple(sorted(x)) for x in a} == b and len(a) == len(b), 100)


def ref_isl(g):
    g = [r[:] for r in g]
    n = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == "1":
                n += 1
                st = [(i, j)]
                while st:
                    x, y = st.pop()
                    if 0 <= x < len(g) and 0 <= y < len(g[0]) and g[x][y] == "1":
                        g[x][y] = "0"
                        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return n


def gen47():
    r, c = R.randint(1, 5), R.randint(1, 5)
    return ([[R.choice("01") for _ in range(c)] for _ in range(r)],)


T(47, "num_islands", gen47, ref_isl)


def ref_cs2(n, pre):
    g = collections.defaultdict(list)
    ind = [0] * n
    for a, b in pre:
        g[b].append(a)
        ind[a] += 1
    q = [i for i in range(n) if ind[i] == 0]
    seen = 0
    while q:
        x = q.pop()
        seen += 1
        for y in g[x]:
            ind[y] -= 1
            if ind[y] == 0:
                q.append(y)
    return seen == n


T(50, "can_finish", lambda: (lambda n: (n, [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(0, 6))]))(R.randint(1, 6)), ref_cs2)


def ref_nd(times, n, k):
    d = {i: float("inf") for i in range(1, n + 1)}
    d[k] = 0
    for _ in range(n):
        for u, v, w in times:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    m = max(d.values())
    return -1 if m == float("inf") else m


T(53, "network_delay_time", lambda: (lambda n: ([[R.randint(1, n), R.randint(1, n), R.randint(1, 9)] for _ in range(R.randint(0, 8))], n, R.randint(1, n)))(R.randint(2, 6)), ref_nd)


def ref_rob(a):
    return max((sum(a[i] for i in c) for r in range(len(a) + 1) for c in itertools.combinations(range(len(a)), r) if all(y - x > 1 for x, y in zip(c, c[1:]))), default=0)


T(56, "rob", lambda: (ri(0, 9, R.randint(0, 9)),), ref_rob)


def ref_rob2(a):
    if len(a) == 1:
        return a[0]
    return max((sum(a[i] for i in c) for r in range(len(a) + 1) for c in itertools.combinations(range(len(a)), r) if all(y - x > 1 for x, y in zip(c, c[1:])) and not (0 in c and len(a) - 1 in c)), default=0)


T(57, "rob_circular", lambda: (ri(0, 9, R.randint(1, 9)),), ref_rob2)


def ref_cc(coins, amt):
    @functools.lru_cache(None)
    def go(r):
        if r == 0:
            return 0
        return min([go(r - c) + 1 for c in coins if c <= r] + [float("inf")])

    b = go(amt)
    return -1 if b == float("inf") else b


T(58, "coin_change", lambda: (R.sample(range(1, 8), R.randint(1, 3)), R.randint(0, 20)), ref_cc)
T(59, "length_of_lis", lambda: (ri(0, 8, R.randint(1, 9)),), lambda a: max((len(c) for r in range(len(a) + 1) for c in itertools.combinations(a, r) if all(x < y for x, y in zip(c, c[1:]))), default=0))


def ref_wb(s, w):
    @functools.lru_cache(None)
    def go(i):
        return i == len(s) or any(s.startswith(x, i) and go(i + len(x)) for x in w)

    return go(0)


T(60, "word_break", lambda: ("".join(R.choice("ab") for _ in range(R.randint(1, 8))), ["".join(R.choice("ab") for _ in range(R.randint(1, 3))) for _ in range(R.randint(1, 3))]), ref_wb)


def ref_dec(s):
    @functools.lru_cache(None)
    def go(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        r = go(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i : i + 2]) <= 26:
            r += go(i + 2)
        return r

    return go(0)


T(62, "num_decodings", lambda: ("".join(R.choice("0123456789") for _ in range(R.randint(1, 8))),), ref_dec)


def ref_lcs(a, b):
    @functools.lru_cache(None)
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        return go(i + 1, j + 1) + 1 if a[i] == b[j] else max(go(i + 1, j), go(i, j + 1))

    return go(0, 0)


T(64, "longest_common_subsequence", lambda: (S(), S()), ref_lcs)


def ref_ed(a, b):
    @functools.lru_cache(None)
    def go(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j), go(i, j + 1), go(i + 1, j + 1))

    return go(0, 0)


T(65, "min_distance", lambda: (S(), S()), ref_ed)
T(66, "can_partition", lambda: (ri(1, 9, R.randint(1, 8)),), lambda a: any(sum(c) * 2 == sum(a) for r in range(len(a) + 1) for c in itertools.combinations(a, r)))


def ref_jump(a):
    @functools.lru_cache(None)
    def go(i):
        return i >= len(a) - 1 or any(go(i + k) for k in range(1, a[i] + 1))

    return go(0)


T(67, "can_jump", lambda: (ri(0, 4, R.randint(1, 8)),), ref_jump)


def gi():
    return [[s, s + R.randint(0, 5)] for s in ri(0, 12, R.randint(1, 7))]


def ref_mi(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


T(69, "merge_intervals", lambda: (gi(),), ref_mi)


def ref_eo(iv):
    best = 0
    for r in range(len(iv) + 1):
        for c in itertools.combinations(sorted(iv), r):
            if all(a[1] <= b[0] for a, b in zip(c, c[1:])):
                best = max(best, r)
    return len(iv) - best


T(70, "erase_overlap_intervals", lambda: ([[s, s + R.randint(1, 5)] for s in ri(0, 10, R.randint(1, 7))],), ref_eo)
T(72, "min_meeting_rooms", lambda: ([[s, s + R.randint(1, 5)] for s in ri(0, 10, R.randint(1, 7))],), lambda iv: max((sum(1 for s, e in iv if s <= t < e) for t in range(0, 30)), default=0))
T(73, "hamming_weight", lambda: (R.randint(0, 2**31),), lambda n: bin(n).count("1"))
T(74, "count_bits", lambda: (R.randint(0, 40),), lambda n: [bin(i).count("1") for i in range(n + 1)])
T(75, "missing_number", lambda: (lambda n: (R.sample(range(n + 1), n),))(R.randint(1, 10)), lambda a: (set(range(len(a) + 1)) - set(a)).pop())
T(10, "three_sum", lambda: (ri(-4, 4, R.randint(0, 9)),), lambda a: {tuple(sorted(c)) for c in itertools.combinations(a, 3) if sum(c) == 0}, lambda a, b: {tuple(sorted(x)) for x in a} == b and len(a) == len(b))
T(13, "max_profit", lambda: (ri(0, 9, R.randint(0, 8)),), lambda p: max([0] + [p[j] - p[i] for i in range(len(p)) for j in range(i + 1, len(p))]))
T(11, "max_area", lambda: (ri(0, 8, R.randint(2, 9)),), lambda h: max(min(h[i], h[j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h))))
T(63, "unique_paths", lambda: (R.randint(1, 6), R.randint(1, 6)), lambda m, n: math.comb(m + n - 2, m - 1))
T(20, "binary_search", lambda: (lambda a: (a, R.randint(0, 25)))(sorted(R.sample(range(25), R.randint(0, 9)))), lambda a, t: a.index(t) if t in a else -1)
T(55, "climb_stairs", lambda: (R.randint(1, 20),), lambda n: (lambda f: f(f, n))(lambda f, k: 1 if k <= 1 else f(f, k - 1) + f(f, k - 2)))



"""Appended to practice/fuzz_checks.py: brute-force cross-checks for 38 more Core 75 problems.

Each check builds inputs with plain Python values, converts them with the *solution module's own* helpers
(from_list, TreeNode), runs the candidate, converts the result back, and compares with an independent oracle.
"""


# ---- helpers for structures -------------------------------------------------------------------------------------
def gt(depth=3):
    """Random binary tree as nested tuples (val, left, right) or None."""
    if depth == 0 or R.random() < 0.25:
        return None
    return (R.randint(0, 6), gt(depth - 1), gt(depth - 1))


def gbst(vals):
    """Random BST (nested tuples) over the sorted distinct `vals`."""
    if not vals:
        return None
    i = R.randrange(len(vals))
    return (vals[i], gbst(vals[:i]), gbst(vals[i + 1:]))


def build(m, t):
    return None if t is None else m.TreeNode(t[0], build(m, t[1]), build(m, t[2]))


def to_t(node):
    return None if node is None else (node.val, to_t(node.left), to_t(node.right))


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def preorder(t):
    return [] if t is None else [t[0]] + preorder(t[1]) + preorder(t[2])


def depth(t):
    return 0 if t is None else 1 + max(depth(t[1]), depth(t[2]))


def mirror(t):
    return None if t is None else (t[0], mirror(t[2]), mirror(t[1]))


def subtrees(t):
    return [] if t is None else [t] + subtrees(t[1]) + subtrees(t[2])


def levels(t):
    out, cur = [], [t] if t else []
    while cur:
        out.append([n[0] for n in cur])
        cur = [c for n in cur for c in (n[1], n[2]) if c]
    return out


def distinct_tree():
    vals = R.sample(range(20), R.randint(0, 7))
    def rec(vs):
        if not vs:
            return None
        i = R.randrange(len(vs))
        return (vs[i], rec(vs[:i]), rec(vs[i + 1:]))
    return rec(vals)


def mk(fn_name, wrap):
    """Return a loader callable: m -> wrapped candidate (so T() can convert inputs with the module's helpers)."""
    return lambda m: wrap(m, getattr(m, fn_name))


# ---- arrays, strings, hashing ----------------------------------------------------------------------------------
T(1, mk("two_sum", lambda m, f: lambda a, t: (lambda r: bool(r) and len(r) == 2 and r[0] != r[1] and a[r[0]] + a[r[1]] == t)(f(a, t))),
  lambda: (ri(-5, 5, R.randint(2, 8)), R.randint(-6, 6)), lambda a, t: any(a[i] + a[j] == t for i in range(len(a)) for j in range(i + 1, len(a))))
T(2, "contains_duplicate", lambda: (ri(0, 6, R.randint(0, 8)),), lambda a: len(set(a)) != len(a))
T(3, "is_anagram", lambda: (S(), S()), lambda s, t: sorted(s) == sorted(t))
T(4, "group_anagrams", lambda: (["".join(R.choice("abc") for _ in range(R.randint(0, 3))) for _ in range(R.randint(0, 7))],),
  lambda w: sorted(tuple(sorted(x for x in w if "".join(sorted(x)) == k)) for k in {"".join(sorted(x)) for x in w}),
  lambda a, b: sorted(tuple(sorted(g)) for g in a) == b)


def top_k_ok(nums, k):
    c = collections.Counter(nums)
    return sorted(c.values(), reverse=True)[:k]


T(5, mk("top_k_frequent", lambda m, f: lambda a, k: (lambda r: sorted((collections.Counter(a)[x] for x in r), reverse=True) if len(set(r)) == len(r) else None)(f(a, k))),
  lambda: (lambda a: (a, R.randint(1, max(1, len(set(a))))))(ri(0, 5, R.randint(1, 10))), top_k_ok)
T(6, "product_except_self", lambda: (ri(-3, 3, R.randint(2, 6)),), lambda a: [math.prod(a[:i] + a[i + 1:]) for i in range(len(a))])


def ref_lc(a):
    s, best = set(a), 0
    for x in s:
        n = 0
        while x + n in s:
            n += 1
        best = max(best, n)
    return best


T(8, "longest_consecutive", lambda: (ri(0, 9, R.randint(0, 9)),), ref_lc)
T(9, "is_palindrome", lambda: ("".join(R.choice("aAb ,") for _ in range(R.randint(0, 8))),),
  lambda s: (lambda c: c == c[::-1])("".join(ch.lower() for ch in s if ch.isalnum())))


def ref_cr(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            sub = s[i:j]
            if len(sub) - max(collections.Counter(sub).values()) <= k:
                best = max(best, len(sub))
    return best


T(15, "character_replacement", lambda: (S(), R.randint(0, 3)), ref_cr)


def ref_vp(s):
    prev = None
    while prev != s:
        prev, s = s, s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


T(17, "is_valid_parentheses", lambda: ("".join(R.choice("()[]{}") for _ in range(R.randint(0, 8))),), ref_vp)
T(18, "daily_temperatures", lambda: (ri(60, 75, R.randint(1, 9)),),
  lambda t: [next((j - i for j in range(i + 1, len(t)) if t[j] > t[i]), 0) for i in range(len(t))])

# ---- linked lists (inputs and outputs converted with the module's own helpers) ------------------------------------
sl = lambda: sorted(ri(0, 9, R.randint(0, 5)))
T(23, mk("reverse_list", lambda m, f: lambda a: m.to_list(f(m.from_list(a)))), lambda: (ri(0, 9, R.randint(0, 7)),), lambda a: a[::-1])
T(24, mk("merge_two_lists", lambda m, f: lambda a, b: m.to_list(f(m.from_list(a), m.from_list(b)))), lambda: (sl(), sl()), lambda a, b: sorted(a + b))
T(28, mk("merge_k_lists", lambda m, f: lambda ls: m.to_list(f([m.from_list(x) for x in ls]))),
  lambda: ([sl() for _ in range(R.randint(0, 4))],), lambda ls: sorted(x for l in ls for x in l))


def after_remove(m, f):
    def go(a, n):
        return m.to_list(f(m.from_list(a), n))
    return go


T(26, mk("remove_nth_from_end", after_remove), lambda: (lambda a: (a, R.randint(1, len(a))))(ri(0, 9, R.randint(1, 7))),
  lambda a, n: a[:len(a) - n] + a[len(a) - n + 1:])


def reorder_wrap(m, f):
    def go(a):
        head = m.from_list(a)
        f(head)
        return m.to_list(head)
    return go


def ref_reorder(a):
    out, lo, hi = [], 0, len(a) - 1
    while lo <= hi:
        out.append(a[lo]); lo += 1
        if lo <= hi:
            out.append(a[hi]); hi -= 1
    return out


T(25, mk("reorder_list", reorder_wrap), lambda: (ri(0, 9, R.randint(1, 8)),), ref_reorder)


def cycle_wrap(m, f):
    def go(a, pos):
        nodes = [m.ListNode(v) for v in a]
        for x, y in zip(nodes, nodes[1:]):
            x.next = y
        if pos is not None and nodes:
            nodes[-1].next = nodes[pos]
        return f(nodes[0] if nodes else None)
    return go


T(27, mk("has_cycle", cycle_wrap), lambda: (lambda a: (a, R.choice([None] + list(range(len(a))))))(ri(0, 9, R.randint(0, 6))),
  lambda a, pos: bool(a) and pos is not None)

# ---- trees -----------------------------------------------------------------------------------------------------
T(30, mk("max_depth", lambda m, f: lambda t: f(build(m, t))), lambda: (gt(4),), depth)
T(29, mk("invert_tree", lambda m, f: lambda t: to_t(f(build(m, t)))), lambda: (gt(3),), mirror)
T(34, mk("level_order", lambda m, f: lambda t: f(build(m, t))), lambda: (gt(4),), levels)
T(35, mk("is_valid_bst", lambda m, f: lambda t: f(build(m, t))), lambda: (gt(3),),
  lambda t: (lambda xs: all(a < b for a, b in zip(xs, xs[1:])))(inorder(t)))
T(36, mk("kth_smallest", lambda m, f: lambda t, k: f(build(m, t), k)),
  lambda: (lambda t: (t, R.randint(1, len(inorder(t)))))(gbst(sorted(R.sample(range(30), R.randint(1, 8))))), lambda t, k: inorder(t)[k - 1])
T(31, mk("is_same_tree", lambda m, f: lambda a, b: f(build(m, a), build(m, b))),
  lambda: (lambda a: (a, a if R.random() < 0.5 else gt(3)))(gt(3)), lambda a, b: a == b)
T(32, mk("is_subtree", lambda m, f: lambda t, s: f(build(m, t), build(m, s))),
  lambda: (lambda t: (t, R.choice(subtrees(t) + [(R.randint(0, 6), None, None)])))(gt(3) or (1, None, None)), lambda t, s: s in subtrees(t))


def check_build_tree():
    f = getattr(load(37), "build_tree")
    bad, ex = 0, None
    for _ in range(300):
        t = distinct_tree()
        got = to_t(f(preorder(t), inorder(t)))
        if got != t:
            bad += 1
            ex = ex or ((preorder(t), inorder(t)), got, t)
    res[37] = ("build_tree", bad, ex)


if not ONLY or ONLY == "37":
    check_build_tree()


def ref_mps(t):
    nodes, adj = [], collections.defaultdict(list)
    def walk(x, parent):
        if x is None:
            return
        i = len(nodes); nodes.append(x[0])
        if parent is not None:
            adj[parent].append(i); adj[i].append(parent)
        walk(x[1], i); walk(x[2], i)
    walk(t, None)
    best = -10**9
    def dfs(u, seen, total):
        nonlocal best
        best = max(best, total)
        for v in adj[u]:
            if v not in seen:
                dfs(v, seen | {v}, total + nodes[v])
    for s in range(len(nodes)):
        dfs(s, {s}, nodes[s])
    return best


def gt_neg(depth=3):
    if depth == 0 or R.random() < 0.25:
        return None
    return (R.randint(-6, 6), gt_neg(depth - 1), gt_neg(depth - 1))


T(38, mk("max_path_sum", lambda m, f: lambda t: f(build(m, t))), lambda: ((lambda t: t if t else (1, None, None))(gt_neg(3)),), ref_mps)


def lca_wrap(m, f):
    def go(t, p, q):
        def find(node, v):
            while node.val != v:
                node = node.left if v < node.val else node.right
            return node
        root = build(m, t)
        return f(root, find(root, p), find(root, q)).val
    return go


def ref_lca(t, p, q):
    while True:
        v = t[0]
        if p < v and q < v:
            t = t[1]
        elif p > v and q > v:
            t = t[2]
        else:
            return v


T(33, mk("lowest_common_ancestor", lca_wrap),
  lambda: (lambda vals: (gbst(vals), R.choice(vals), R.choice(vals)))(sorted(R.sample(range(30), R.randint(2, 8)))), ref_lca)

# ---- backtracking, graphs, intervals, DP -----------------------------------------------------------------------
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def ref_exist(board, word):
    rows, cols = len(board), len(board[0])
    def go(r, c, i, used):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        return any(0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in used and go(r + dr, c + dc, i + 1, used | {(r + dr, c + dc)}) for dr, dc in DIRS)
    return any(go(r, c, 0, {(r, c)}) for r in range(rows) for c in range(cols))


T(45, "exist", lambda: ([[R.choice("ab") for _ in range(3)] for _ in range(3)], "".join(R.choice("ab") for _ in range(R.randint(1, 5)))), ref_exist)


def ref_pa(h):
    rows, cols = len(h), len(h[0])
    def reach(starts):
        seen, stack = set(starts), list(starts)
        while stack:
            r, c = stack.pop()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen and h[nr][nc] >= h[r][c]:
                    seen.add((nr, nc)); stack.append((nr, nc))
        return seen
    pac = reach([(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)])
    atl = reach([(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)])
    return sorted(pac & atl)


T(49, "pacific_atlantic", lambda: (lambda w, h: ([ri(0, 3, w) for _ in range(h)],))(R.randint(2, 4), R.randint(2, 4)),
  ref_pa, lambda a, b: sorted(tuple(x) for x in a) == b)


def components(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    return len({find(i) for i in range(n)})


gedges = lambda: (lambda n: (n, [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(0, n + 1)) if n > 1]))(R.randint(1, 7))
T(51, "count_components", gedges, components)
T(52, "valid_tree", gedges, lambda n, e: len(e) == n - 1 and components(n, e) == 1)


def ref_cs4(nums, target):
    def go(t):
        return 1 if t == 0 else sum(go(t - x) for x in nums if x <= t)
    return go(target)


T(61, "combination_sum_4", lambda: (R.sample(range(1, 5), R.randint(1, 3)), R.randint(1, 8)), ref_cs4)


def gdisjoint():
    pts = sorted(R.sample(range(0, 30), R.choice([0, 2, 4, 6])))
    return [[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)]


T(68, "insert_interval", lambda: (gdisjoint(), sorted(R.sample(range(0, 30), 2))), lambda iv, new: ref_mi(iv + [new]))
T(71, "can_attend_meetings", lambda: ([[s, s + R.randint(1, 5)] for s in ri(0, 12, R.randint(0, 5))],),
  lambda iv: all(a[1] <= b[0] for a, b in zip(sorted(iv), sorted(iv)[1:])))


# ---- classes ---------------------------------------------------------------------------------------------------
def check_codec():
    m = load(7)
    bad, ex = 0, None
    for _ in range(300):
        strs = ["".join(R.choice("a#:,0123456789 ") for _ in range(R.randint(0, 5))) for _ in range(R.randint(0, 5))]
        c = m.Codec()
        got = c.decode(c.encode(strs))
        if got != strs:
            bad += 1
            ex = ex or (strs, got, strs)
    res[7] = ("Codec.encode/decode", bad, ex)


def check_median():
    m = load(43)
    bad, ex = 0, None
    for _ in range(300):
        mf, seen = m.MedianFinder(), []
        for x in ri(-9, 9, R.randint(1, 9)):
            mf.add_num(x)
            seen.append(x)
            s = sorted(seen)
            want = s[len(s) // 2] if len(s) % 2 else (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
            if mf.find_median() != want:
                bad += 1
                ex = ex or (list(seen), mf.find_median(), want)
                break
    res[43] = ("MedianFinder", bad, ex)


if not ONLY or ONLY == "7":
    check_codec()
if not ONLY or ONLY == "43":
    check_median()


def run(only=None, source_dir=None):
    """Return {problem: (function, mismatches, example)}; empty dict entries mean no check exists."""
    if source_dir:
        SOURCE["dir"] = source_dir
    return {n: v for n, v in res.items() if only is None or n == only}
