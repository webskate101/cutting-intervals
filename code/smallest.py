"""Smallest counterexamples to conj:bounded-splitting.
  python smallest.py grid k1,k2,..   -- smallest connected intervals of the grid with no bounded splitting
  python smallest.py shrink "abc ..." -- delete points greedily (any subposet, connected) while
                                        no bounded splitting exists"""
import sys, itertools
from splitsearch import grid, all_downsets, Sub, connected_pieces, show

def no_splitting(delta, below, above):
    c, _ = Sub(delta, below, above).count_splittings(cap=1)
    return c == 0

if sys.argv[1] == "grid":
    dims = tuple(int(x) for x in sys.argv[2].split(','))
    pts, below, above = grid(dims)
    downs = all_downsets(len(pts), below)
    seen = set(); found = []
    for A in downs:
        for B in downs:
            if B & ~A or B == A: continue
            for d in connected_pieces(A & ~B, below, above):
                if d not in seen:
                    seen.add(d)
                    if no_splitting(d, below, above): found.append(d)
    sizes = sorted(set(bin(d).count('1') for d in found))
    print(f"{'x'.join(map(str, dims))}: {len(seen)} connected intervals, {len(found)} without a bounded splitting")
    if found:
        m = sizes[0]
        small = [d for d in found if bin(d).count('1') == m]
        print(f"  smallest size {m} ({len(small)} of them), e.g.:")
        for d in small[:4]: print("   ", show(d, pts))
else:
    names = sys.argv[2].replace(',', ' ').split()
    P = [tuple(int(c) for c in s) for s in names]
    n = len(P)
    le = lambda p, q: all(a <= b for a, b in zip(p, q))
    below = [sum(1 << j for j in range(n) if le(P[j], P[i])) for i in range(n)]
    above = [sum(1 << j for j in range(n) if le(P[i], P[j])) for i in range(n)]
    cur = (1 << n) - 1
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if cur >> i & 1:
                d = cur & ~(1 << i)
                sub = Sub(d, below, above)
                if len(sub.components(d)) == 1 and no_splitting(d, below, above):
                    cur = d; changed = True; break
    print(f"minimal subposet without a bounded splitting: {bin(cur).count('1')} points:",
          "{" + ",".join(names[i] for i in range(n) if cur >> i & 1) + "}")
