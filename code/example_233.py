"""Bounded splitting of the [2]x[3]x[3] interval that has no strict zig-zag cut."""
from zigzag import grid_poset, relations, components, relaxed_cut, zigzag_cut
from poset_sat import structures
n, le, pts = grid_poset((2, 3, 3))
below, above = relations(n, le); comp = [below[i] | above[i] for i in range(n)]
downs, ints = structures(n, le)
idx = {"".join(str(c + 1) for c in p): i for i, p in enumerate(pts)}
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i]) for i in range(n) if I >> i & 1) + "}"
delta = sum(1 << idx[s] for s in "112,113,121,122,123,131,132,133,212,221,222".split(","))
print("strict cut:", zigzag_cut(delta, downs, below, above, comp, n))
S = relaxed_cut(delta, downs, below, above, comp, n)
print("bounded splitting:", show(S))
for C in components(S, comp, n) + components(delta & ~S, comp, n):
    ups = [show(1 << r) for r in range(n) if delta >> r & 1 and C & ~below[r] == 0]
    dns = [show(1 << r) for r in range(n) if delta >> r & 1 and C & ~above[r] == 0]
    print("  component", show(C), "upper", ups, "lower", dns)
