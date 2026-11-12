"""Treat a bounded-splitting counterexample Delta as a poset in its own right and test
(a) the conclusion of thm:bounded-splitting-three / thm:2d-zig-zag, and
(b) conj:three (good => 3-cuttable), exactly, by SAT."""
import sys, time
from poset_sat import structures, max_tau_at_least
from zigzag import thm_search

names = sys.argv[1].replace(',', ' ').split()
P = [tuple(int(c) for c in s) for s in names]
n = len(P)
le = [[all(a <= b for a, b in zip(p, q)) for q in P] for p in P]
downs, ints = structures(n, le)
print(f"{n} points, {len(downs)} downsets, {len(ints)} connected intervals")
show = lambda I: "{" + ",".join(names[i] for i in range(n) if I >> i & 1) + "}"
t0 = time.time()
fam = thm_search(n, le, downs, ints, 4)
print(f"(a) collection needing >= 4 cuts with D_I, U_I free: "
      f"{'NONE' if fam is None else ' '.join(map(show, fam))} [{time.time()-t0:.0f}s]")
t0 = time.time()
fam = max_tau_at_least(downs, ints, 4)
print(f"(b) good collection needing >= 4 cuts: "
      f"{'NONE' if fam is None else ' '.join(map(show, fam))} [{time.time()-t0:.0f}s]")
