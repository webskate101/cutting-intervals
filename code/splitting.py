"""Search for a finite connected poset P with no 'bounded splitting': a downset S of P
such that every connected component of S and of P \\ S has an upper or a lower bound
in P.  Usage: python splitting.py n p count seed"""
import sys, random
from poset_sat import random_poset
from zigzag import relations, components

n, p, count, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
checked = 0
for _ in range(count):
    le = random_poset(n, p, rng)
    below, above = relations(n, le)
    comp = [below[i] | above[i] for i in range(n)]
    full = (1 << n) - 1
    if len(components(full, comp, n)) != 1: continue
    checked += 1
    bounded = lambda C: any(C & ~below[r] == 0 or C & ~above[r] == 0 for r in range(n))
    downs = {0}; frontier = [0]; found = False
    while frontier and not found:
        new = []
        for D in frontier:
            if all(bounded(C) for C in components(D, comp, n) + components(full & ~D, comp, n)):
                found = True; break
            for i in range(n):
                if not D >> i & 1 and (below[i] & ~(1 << i)) & ~D == 0:
                    E = D | 1 << i
                    if E not in downs: downs.add(E); new.append(E)
        frontier = new
    if not found:
        print("NO bounded splitting:", [(i, j) for i in range(n) for j in range(n) if i != j and le[i][j]])
        break
print(f"n={n} p={p}: checked {checked} connected posets")
