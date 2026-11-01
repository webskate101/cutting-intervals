"""Brute-force exploration of the connected-intervals conjecture on small grids."""
import itertools, sys

def setup(dims):
    pts = list(itertools.product(*[range(k) for k in dims]))
    idx = {p: i for i, p in enumerate(pts)}
    le = lambda a, b: all(x <= y for x, y in zip(a, b))
    n = len(pts)
    below = [sum(1 << j for j in range(n) if le(pts[j], pts[i])) for i in range(n)]
    above = [sum(1 << j for j in range(n) if le(pts[i], pts[j])) for i in range(n)]
    # downsets: closed under below
    downs = []
    for m in range(1 << n):
        if all(not (m >> i & 1) or (below[i] & ~m) == 0 for i in range(n)):
            downs.append(m)
    # convex sets: intersection of downset and upset; enumerate as L(A) & U(A) style
    ups = [((1 << n) - 1) ^ d for d in downs]
    convex = set(d & u for d in downs for u in ups)
    comp = [below[i] | above[i] for i in range(n)]
    def connected(m):
        if m == 0: return False
        start = (m & -m).bit_length() - 1
        seen = 1 << start; frontier = seen
        while frontier:
            nf = 0
            for i in range(n):
                if frontier >> i & 1: nf |= comp[i] & m
            nf &= ~seen; seen |= nf; frontier = nf
        return seen == m
    ints = sorted(m for m in convex if bin(m).count('1') >= 2 and connected(m))
    return pts, downs, ints

def analyse(dims):
    pts, downs, ints = setup(dims)
    cutsets = []  # for each downset, bitmask over intervals it cuts
    for d in downs:
        c = 0
        for j, I in enumerate(ints):
            if I & d and I & ~d: c |= 1 << j
        if c: cutsets.append(c)
    cutsets = list(set(cutsets))
    # drop dominated cutsets
    cutsets = [c for c in cutsets if not any(c != e and c & e == c for e in cutsets)]
    def one_cuttable(fam):
        return any(fam & c == fam for c in cutsets)
    N = len(ints)
    # minimal 1-uncuttable pairwise-disjoint families: check sizes 2 and 3
    bad2 = set()
    for a, b in itertools.combinations(range(N), 2):
        if ints[a] & ints[b] == 0 and not one_cuttable((1 << a) | (1 << b)):
            bad2.add((a, b))
    helly3 = 0
    for a, b, c in itertools.combinations(range(N), 3):
        if ints[a] & ints[b] or ints[a] & ints[c] or ints[b] & ints[c]: continue
        if (a, b) in bad2 or (a, c) in bad2 or (b, c) in bad2: continue
        if not one_cuttable((1 << a) | (1 << b) | (1 << c)): helly3 += 1
    print(dims, "points", len(pts), "downsets", len(downs), "conn. intervals", N,
          "bad disjoint pairs", len(bad2), "minimal bad disjoint triples", helly3)
    return ints, cutsets, bad2

def tau(fam, cutsets, limit=6):
    rel = list(set(c & fam for c in cutsets if c & fam))
    rel = [c for c in rel if not any(c != e and c & e == c for e in rel)]
    for k in range(1, limit + 1):
        # simple DFS: pick lowest uncovered interval, branch on cutsets covering it
        def dfs(rem, k):
            if rem == 0: return True
            if k == 0: return False
            low = rem & -rem
            return any(dfs(rem & ~c, k - 1) for c in rel if c & low)
        if dfs(fam, k): return k
    return None

if __name__ == "__main__":
    import random
    dims = tuple(int(x) for x in sys.argv[1:])
    ints, cutsets, bad2 = analyse(dims)
    N = len(ints)
    adj = [0] * N
    for a, b in bad2: adj[a] |= 1 << b; adj[b] |= 1 << a
    # random maximal families with no bad disjoint pair; record max tau
    best = 0; bestfam = None
    random.seed(1)
    for trial in range(int(2000)):
        order = list(range(N)); random.shuffle(order)
        fam = 0
        for j in order:
            if not adj[j] & fam: fam |= 1 << j
        t = tau(fam, cutsets)
        if t and t > best:
            best, bestfam = t, fam
    print("max tau found over 'good' families (no bad disjoint pair):", best)
    if bestfam:
        pts = list(itertools.product(*[range(k) for k in dims]))
        print("example family size", bin(bestfam).count('1'))
