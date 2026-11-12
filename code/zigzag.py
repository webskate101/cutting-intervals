"""Experiments on generalising thm:2d-zig-zag.

A decreasing set L is a *zig-zag cut* of a connected interval Delta if every
connected component of L & Delta has an upper bound in Delta and every connected
component of Delta \\ L has a lower bound in Delta.  (In 2D the staircase in the
proof of thm:2d-zig-zag is one.)

  python zigzag.py cuts  grid k1,k2,...       -- does every connected interval have a zig-zag cut?
  python zigzag.py cuts  random n p count seed
  python zigzag.py relaxed ...                  -- same, components bounded above OR below
  python zigzag.py thm   grid k1,k2,... T     -- SAT: is there a collection with D_I and U_I free
  python zigzag.py thm   random n p count seed T   (no member inside them) needing >= T cuts?
"""
import sys, itertools, random
from pysat.solvers import Cadical153
from poset_sat import random_poset, structures


def grid_poset(dims):
    pts = list(itertools.product(*[range(k) for k in dims]))
    le = [[all(a <= b for a, b in zip(p, q)) for q in pts] for p in pts]
    return len(pts), le, pts


def relations(n, le):
    below = [sum(1 << j for j in range(n) if le[j][i]) for i in range(n)]
    above = [sum(1 << j for j in range(n) if le[i][j]) for i in range(n)]
    return below, above


def components(m, comp, n):
    out = []
    while m:
        start = (m & -m).bit_length() - 1
        seen = 1 << start; fr = seen
        while fr:
            nf = 0
            for i in range(n):
                if fr >> i & 1: nf |= comp[i] & m
            nf &= ~seen; seen |= nf; fr = nf
        out.append(seen); m &= ~seen
    return out


def zigzag_cut(delta, downs, below, above, comp, n):
    elems = [i for i in range(n) if delta >> i & 1]
    seen = set()
    for D in downs:
        S = D & delta
        if S in seen: continue
        seen.add(S)
        if all(any(C & ~below[r] == 0 for r in elems) for C in components(S, comp, n)) and \
           all(any(C & ~above[r] == 0 for r in elems) for C in components(delta & ~S, comp, n)):
            return S
    return None


def relaxed_cut(delta, downs, below, above, comp, n):
    """Decreasing L such that every component of L & delta and of delta \ L is bounded
    above OR below by an element of delta."""
    elems = [i for i in range(n) if delta >> i & 1]
    bounded = lambda C: any(C & ~below[r] == 0 or C & ~above[r] == 0 for r in elems)
    seen = set()
    for D in downs:
        S = D & delta
        if S in seen: continue
        seen.add(S)
        if all(bounded(C) for C in components(S, comp, n) + components(delta & ~S, comp, n)):
            return S
    return None


def check_cuts(n, le, downs, ints, label):
    below, above = relations(n, le)
    comp = [below[i] | above[i] for i in range(n)]
    finder = relaxed_cut if RELAXED else zigzag_cut
    bad = [I for I in ints if finder(I, downs, below, above, comp, n) is None]
    return bad


def thm_search(n, le, downs, ints, T):
    """Find a collection with D_I, U_I free and tau >= T (None if none exists)."""
    below, above = relations(n, le)
    N = len(ints)
    cut = [sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs]
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
    # members inside L(p) / U(p)
    in_L = [[j for j, J in enumerate(ints) if J & ~below[p] == 0] for p in range(n)]
    in_U = [[j for j, J in enumerate(ints) if J & ~above[p] == 0] for p in range(n)]
    while s.solve():
        pos = set(l for l in s.get_model() if l > 0)
        F = [j for j in range(N) if j + 1 in pos]
        Fs = set(F)
        Uset = [p for p in range(n) if any(j in Fs for j in in_L[p])]
        Dset = [p for p in range(n) if any(j in Fs for j in in_U[p])]
        Um = sum(1 << p for p in Uset); Dm = sum(1 << p for p in Dset)
        viol = None
        for j in F:
            for side, M, wit in (("U", Um, in_L), ("D", Dm, in_U)):
                if ints[j] & ~M == 0:
                    # certificate: j together with one witness for each of its points
                    cert = {j}
                    for p in range(n):
                        if ints[j] >> p & 1:
                            cert.add(next(q for q in wit[p] if q in Fs))
                    viol = cert; break
            if viol: break
        if viol is None:
            return [ints[j] for j in F]
        s.add_clause([-(j + 1) for j in viol])
    return None


def show(I, pts):
    return "{" + ",".join("".join(str(c + 1) for c in pts[i]) for i in range(len(pts)) if I >> i & 1) + "}"


RELAXED = False

if __name__ == "__main__":
    mode, kind = sys.argv[1], sys.argv[2]
    if mode == "relaxed":
        mode, RELAXED = "cuts", True
    if kind == "grid":
        dims = tuple(int(x) for x in sys.argv[3].split(','))
        n, le, pts = grid_poset(dims)
        posets = [(n, le, pts)]; rest = sys.argv[4:]; label = 'x'.join(f'[{d}]' for d in dims)
    else:
        n, p, count, seed = int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        rng = random.Random(seed)
        posets = [(n, random_poset(n, p, rng), [(i,) for i in range(n)]) for _ in range(count)]
        rest = sys.argv[7:]; label = f"{count} random posets n={n} p={p}"
    total_bad = 0
    for n, le, pts in posets:
        downs, ints = structures(n, le)
        if mode == "cuts":
            bad = check_cuts(n, le, downs, ints, label)
            total_bad += len(bad)
            if bad and kind == "grid":
                print("no zig-zag cut for e.g.", show(bad[0], pts), f"({len(bad)} intervals)")
        else:
            fam = thm_search(n, le, downs, ints, int(rest[0]))
            if fam is not None:
                print(f"FOUND in {label}: D_I, U_I free but needs >= {rest[0]} cuts:",
                      " ".join(show(I, pts) for I in fam))
                total_bad += 1
                break
    print(label, mode, "-> failures:", total_bad)
