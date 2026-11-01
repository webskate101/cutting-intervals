import itertools, sys, random
from explore import setup, tau

dims = tuple(int(x) for x in sys.argv[1:-1]); trials = int(sys.argv[-1])
pts, downs, ints = setup(dims)
N = len(ints)
cutsets = list(set(sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs))
cutsets = [c for c in cutsets if c and not any(c != e and c & e == c for e in cutsets)]
show = lambda I: "{" + " ".join("".join(str(c + 1) for c in pts[i]) for i in range(len(pts)) if I >> i & 1) + "}"
disj = [sum(1 << k for k in range(N) if not ints[j] & ints[k]) for j in range(N)]
cut1 = lambda fam: any(fam & c == fam for c in cutsets)

def can_add(fam, j):
    # every disjoint subfamily S of fam with all members disjoint from j: S+{j} 1-cuttable
    def rec(S, cand):
        if not cut1(S): return False
        while cand:
            k = (cand & -cand).bit_length() - 1; cand &= cand - 1
            if not rec(S | 1 << k, cand & disj[k]): return False
        return True
    return rec(1 << j, fam & disj[j])

# print a minimal bad triple
for a, b, c in itertools.combinations(range(N), 3):
    S = (1 << a) | (1 << b) | (1 << c)
    if disj[a] >> b & 1 and disj[a] >> c & 1 and disj[b] >> c & 1 and not cut1(S) \
       and all(cut1(S & ~(1 << x)) for x in (a, b, c)):
        print("bad triple:", show(ints[a]), show(ints[b]), show(ints[c])); break

random.seed(0); best = 0
for t in range(trials):
    order = list(range(N)); random.shuffle(order); fam = 0
    for j in order:
        if can_add(fam, j): fam |= 1 << j
    tt = tau(fam, cutsets, 8)
    if tt > best:
        best = tt; print("tau", tt, "family size", bin(fam).count('1'))
        if tt >= 3: print("  ", " ".join(show(ints[j]) for j in range(N) if fam >> j & 1))
print(dims, "max tau over good families found:", best)
