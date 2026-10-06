"""Randomized cross-checks against brute-force references (34 problems).

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
    f = getattr(load(n), fn)
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



def run(only=None, source_dir=None):
    """Return {problem: (function, mismatches, example)}; empty dict entries mean no check exists."""
    if source_dir:
        SOURCE["dir"] = source_dir
    return {n: v for n, v in res.items() if only is None or n == only}
