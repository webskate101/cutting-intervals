"""Independent check that a subset Delta of a product of chains is a connected
interval with no bounded splitting.  Brute force over ALL subsets of Delta.
Usage: python verify_counterexample.py k1,k2,.. "abc abc ..." """
import sys, itertools
dims = tuple(int(x) for x in sys.argv[1].split(','))
names = sys.argv[2].replace(',', ' ').replace('{', '').replace('}', '').split()
P = [tuple(int(c) for c in s) for s in names]
n = len(P)
le = lambda p, q: all(a <= b for a, b in zip(p, q))
grid = list(itertools.product(*[range(1, k + 1) for k in dims]))
assert all(p in grid for p in P)
print("order convex:", all(z in P for p in P for r in P for z in grid if le(p, z) and le(z, r)))

def comps(S):
    S = set(S); out = []
    while S:
        x = S.pop(); C = {x}; stack = [x]
        while stack:
            y = stack.pop()
            for z in list(S):
                if le(P[y], P[z]) or le(P[z], P[y]):
                    S.remove(z); C.add(z); stack.append(z)
        out.append(C)
    return out
print("connected:", len(comps(range(n))) == 1)
bounded = lambda C: any(all(le(P[c], P[r]) for c in C) or all(le(P[r], P[c]) for c in C) for r in range(n))
count_down = count_split = 0
for mask in range(1 << n):
    S = [i for i in range(n) if mask >> i & 1]
    if any(le(P[j], P[i]) and not mask >> j & 1 for i in S for j in range(n)):
        continue  # not decreasing
    count_down += 1
    T = [i for i in range(n) if not mask >> i & 1]
    if all(bounded(C) for C in comps(S)) and all(bounded(C) for C in comps(T)):
        count_split += 1
print(f"decreasing subsets: {count_down}, bounded splittings: {count_split}")
print("minimal:", [names[i] for i in range(n) if not any(j != i and le(P[j], P[i]) for j in range(n))])
print("maximal:", [names[i] for i in range(n) if not any(j != i and le(P[i], P[j]) for j in range(n))])
