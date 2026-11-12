"""tau of the family of all connected intervals of Delta that are unbounded in Delta
(no upper and no lower bound in Delta).  Delta has no bounded splitting iff this
family is 1-uncuttable."""
import sys, itertools
from poset_sat import structures

names = sys.argv[1].replace(',', ' ').split()
P = [tuple(int(c) for c in s) for s in names]
n = len(P)
le = [[all(a <= b for a, b in zip(p, q)) for q in P] for p in P]
downs, ints = structures(n, le)
below = [sum(1 << j for j in range(n) if le[j][i]) for i in range(n)]
above = [sum(1 << j for j in range(n) if le[i][j]) for i in range(n)]
bounded = lambda C: any(C & ~below[r] == 0 or C & ~above[r] == 0 for r in range(n))
fam = [I for I in ints if not bounded(I)]
show = lambda I: "{" + ",".join(names[i] for i in range(n) if I >> i & 1) + "}"
print(len(fam), "unbounded connected intervals")
cut = lambda D: sum(1 << j for j, I in enumerate(fam) if I & D and I & ~D)
cs = list(set(cut(D) for D in downs))
full = (1 << len(fam)) - 1
for k in (1, 2, 3):
    if any(sum_ == full for sum_ in (
            (lambda comb: (lambda u: u)(__import__('functools').reduce(lambda a, b: a | b, comb, 0)))(comb)
            for comb in itertools.combinations(cs, k))):
        print("tau =", k); break
else:
    print("tau >= 4")
mins = [I for I in fam if not any(J != I and J & ~I == 0 for J in fam)]
print("inclusion-minimal unbounded intervals:", " ".join(map(show, mins)))
