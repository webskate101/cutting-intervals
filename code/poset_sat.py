"""Exact test, on random finite posets, of: every good collection of connected
intervals (every pairwise disjoint subfamily 1-cuttable) is (T-1)-cuttable.
Usage: python poset_sat.py n_points T n_posets edge_prob seed"""
import sys, random, time
from pysat.solvers import Cadical153


def random_poset(n, p, rng):
    le = [[i == j for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p: le[i][j] = True
    for k in range(n):  # transitive closure
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]: le[i][j] = True
    return le


def structures(n, le):
    below = [sum(1 << j for j in range(n) if le[j][i]) for i in range(n)]
    above = [sum(1 << j for j in range(n) if le[i][j]) for i in range(n)]
    comp = [below[i] | above[i] for i in range(n)]
    downs = [m for m in range(1 << n)
             if all(not (m >> i & 1) or (below[i] & ~m) == 0 for i in range(n))]
    def convex(m):
        return all(not (m >> i & 1) or not (m >> j & 1) or
                   (above[i] & below[j] & ~m) == 0 for i in range(n) for j in range(n))
    def connected(m):
        start = (m & -m).bit_length() - 1
        seen = 1 << start; fr = seen
        while fr:
            nf = 0
            for i in range(n):
                if fr >> i & 1: nf |= comp[i] & m
            nf &= ~seen; seen |= nf; fr = nf
        return seen == m
    ints = [m for m in range(1, 1 << n) if bin(m).count('1') >= 2 and convex(m) and connected(m)]
    return downs, ints


def max_tau_at_least(downs, ints, T):
    """Return a good family needing >= T cuts, or None."""
    N = len(ints)
    cut = [sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs]
    cutsets = [c for c in set(cut) if c]
    cutsets = [c for c in cutsets if not any(c != e and c & e == c for e in cutsets)]
    disj = [sum(1 << q for q in range(N) if not ints[j] & ints[q]) for j in range(N)]
    sub = {i: [j for j in range(len(downs)) if j != i and downs[j] & ~downs[i] == 0]
           for i in range(len(downs))}
    unions = set()
    def chains(last, depth, u):
        if depth == 0: unions.add(u); return
        for j in sub[last]: chains(j, depth - 1, u | cut[j])
    for i in range(len(downs)): chains(i, T - 2, cut[i])
    maximal = []
    for u in sorted(unions, key=lambda u: -bin(u).count('1')):
        if not any(u & v == u for v in maximal): maximal.append(u)
    s = Cadical153()
    for u in maximal:
        s.add_clause([j + 1 for j in range(N) if not u >> j & 1])
    cut1 = lambda S: any(S & c == S for c in cutsets)
    while s.solve():
        pos = set(l for l in s.get_model() if l > 0)
        fam = sum(1 << j for j in range(N) if j + 1 in pos)
        bad = []
        def rec(S, cand):
            if not cut1(S): bad.append(S); return len(bad) >= 100
            while cand:
                q = (cand & -cand).bit_length() - 1; cand &= cand - 1
                if rec(S | 1 << q, cand & disj[q]): return True
            return False
        for a in range(N):
            if fam >> a & 1 and rec(1 << a, fam & disj[a] & ~((1 << (a + 1)) - 1)): break
        if not bad:
            return [ints[j] for j in range(N) if fam >> j & 1]
        for S in bad:
            s.add_clause([-(j + 1) for j in range(N) if S >> j & 1])
    return None


if __name__ == "__main__":
    n, T, count = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    p, seed = float(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed); t0 = time.time()
    for trial in range(count):
        le = random_poset(n, p, rng)
        downs, ints = structures(n, le)
        fam = max_tau_at_least(downs, ints, T)
        if fam is not None:
            rel = [(i, j) for i in range(n) for j in range(n) if i != j and le[i][j]]
            print(f"COUNTEREXAMPLE poset n={n}, relations {rel}")
            print("  family:", [[i for i in range(n) if I >> i & 1] for I in fam])
            break
    else:
        print(f"no good family needing >= {T} cuts in {count} random posets "
              f"(n={n}, p={p}) [{time.time()-t0:.0f}s]")
