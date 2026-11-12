"""Test the relaxed zig-zag condition on sampled connected intervals of a grid.
mode 'any': some decreasing L works; 'principal': L = L(r) or X minus U(r), r in Delta.
Usage: python relaxed_sample.py k1,k2,.. samples seed mode"""
import sys, random, itertools
from zigzag import grid_poset, relations, components, relaxed_cut
from poset_sat import structures

dims = tuple(int(x) for x in sys.argv[1].split(','))
samples, seed, mode = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
n, le, pts = grid_poset(dims)
below, above = relations(n, le)
comp = [below[i] | above[i] for i in range(n)]
full = (1 << n) - 1
# downsets via closure of random antichains
def down_of(S):
    m = 0
    for i in S: m |= below[i]
    return m
rng = random.Random(seed)
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i]) for i in range(n) if I >> i & 1) + "}"
def principal(delta):
    elems = [i for i in range(n) if delta >> i & 1]
    bounded = lambda C: any(C & ~below[r] == 0 or C & ~above[r] == 0 for r in elems)
    for r in elems:
        for S in (below[r] & delta, delta & ~above[r]):
            if all(bounded(C) for C in components(S, comp, n) + components(delta & ~S, comp, n)):
                return S
    return None
# a pool of downsets for the 'any' search
pool = set()
for _ in range(4000):
    pool.add(down_of(rng.sample(range(n), rng.randint(0, 4))))
pool = list(pool)
tested = fails = 0
while tested < samples:
    A = down_of(rng.sample(range(n), rng.randint(1, 4)))
    B = down_of(rng.sample(range(n), rng.randint(0, 4))) & A
    for delta in components(A & ~B, comp, n):
        if bin(delta).count('1') < 2: continue
        tested += 1
        ok = principal(delta) if mode == "principal" else relaxed_cut(delta, pool + [0, full], below, above, comp, n)
        if ok is None:
            fails += 1
            if fails <= 3: print("fails for", show(delta))
print(dims, mode, "tested", tested, "failures", fails)
