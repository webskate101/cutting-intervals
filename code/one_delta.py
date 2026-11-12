"""Check one interval of [3]^3 against every downset for a relaxed zig-zag cut."""
from zigzag import grid_poset, relations, components, relaxed_cut
n, le, pts = grid_poset((3, 3, 3))
below, above = relations(n, le); comp = [below[i] | above[i] for i in range(n)]
idx = {"".join(str(c + 1) for c in p): i for i, p in enumerate(pts)}
delta = sum(1 << idx[s] for s in "113,121,122,123,131,211,212,213,221,231,311,321,331".split(","))
downs = {0}; frontier = [0]
while frontier:
    new = []
    for D in frontier:
        for i in range(n):
            if not D >> i & 1 and (below[i] & ~(1 << i)) & ~D == 0:
                E = D | 1 << i
                if E not in downs: downs.add(E); new.append(E)
    frontier = new
print(len(downs), "downsets")
S = relaxed_cut(delta, list(downs), below, above, comp, n)
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i]) for i in range(n) if I >> i & 1) + "}"
print("relaxed cut:", None if S is None else show(S))
if S is not None:
    for C in components(S, comp, n) + components(delta & ~S, comp, n):
        ups = [show(1 << r) for r in range(n) if delta >> r & 1 and C & ~below[r] == 0]
        dns = [show(1 << r) for r in range(n) if delta >> r & 1 and C & ~above[r] == 0]
        print("  component", show(C), "upper bounds in Delta", ups, "lower", dns)
