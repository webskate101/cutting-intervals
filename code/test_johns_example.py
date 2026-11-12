"""Test conj:bounded-splitting on John's set in [2]x[4]x[4] (comment at end of main.tex)."""
from zigzag import components

names = "113 114 122 123 124 131 132 133 134 141 142 143 213 222 223 231 232".split()
pts = [tuple(int(c) for c in s) for s in names]
n = len(pts)
le = lambda p, q: all(a <= b for a, b in zip(p, q))
below = [sum(1 << j for j in range(n) if le(pts[j], pts[i])) for i in range(n)]
above = [sum(1 << j for j in range(n) if le(pts[i], pts[j])) for i in range(n)]
comp = [below[i] | above[i] for i in range(n)]
full = (1 << n) - 1
show = lambda m: "{" + ",".join(names[i] for i in range(n) if m >> i & 1) + "}"

# Is it an interval (order convex in [2]x[4]x[4]) and connected?
import itertools
grid = list(itertools.product(range(1, 3), range(1, 5), range(1, 5)))
convex = all(not (le(p, z) and le(z, r)) or z in pts for p in pts for r in pts for z in grid)
print("order convex in [2]x[4]x[4]:", convex)
print("connected:", len(components(full, comp, n)) == 1)
print("minimal:", [names[i] for i in range(n) if below[i] == 1 << i])
print("maximal:", [names[i] for i in range(n) if above[i] == 1 << i])

# all downsets of the subposet
downs = {0}; frontier = [0]
while frontier:
    new = []
    for D in frontier:
        for i in range(n):
            if not D >> i & 1 and (below[i] & ~(1 << i)) & ~D == 0:
                E = D | 1 << i
                if E not in downs: downs.add(E); new.append(E)
    frontier = new
print(len(downs), "decreasing subsets")

bounded = lambda C: any(C & ~below[r] == 0 or C & ~above[r] == 0 for r in range(n))
good = [D for D in downs
        if all(bounded(C) for C in components(D, comp, n) + components(full & ~D, comp, n))]
print("bounded splittings:", len(good))
for D in sorted(good, key=lambda d: bin(d).count('1'))[:5]:
    print("  ", show(D))
if not good:
    # report, for the best attempts, which components are unbounded
    def unbounded(D):
        return [C for C in components(D, comp, n) + components(full & ~D, comp, n) if not bounded(C)]
    best = min(downs, key=lambda D: len(unbounded(D)))
    print("fewest unbounded components:", len(unbounded(best)), "e.g. S =", show(best),
          "unbounded:", [show(C) for C in unbounded(best)])

for D in sorted(good, key=lambda d: bin(d).count('1')):
    print("splitting", show(D))
    for side, part in (("S", D), ("complement", full & ~D)):
        for C in components(part, comp, n):
            ups = [names[r] for r in range(n) if C & ~below[r] == 0]
            dns = [names[r] for r in range(n) if C & ~above[r] == 0]
            print(f"   {side} component {show(C)}: upper bounds {ups}, lower bounds {dns}")
# principal cuts?
princ = [r for r in range(n) if below[r] in good or full & ~above[r] in good]
print("principal splittings from r =", [names[r] for r in princ])
