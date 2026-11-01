import itertools, sys, random
from explore import setup, tau
dims = tuple(int(x) for x in sys.argv[1:])
pts, downs, ints = setup(dims); N = len(ints)
cutsets = list(set(sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs))
cutsets = [c for c in cutsets if c and not any(c != e and c & e == c for e in cutsets)]
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i]) for i in range(len(pts)) if I >> i & 1) + "}"
disj = [sum(1 << k for k in range(N) if not ints[j] & ints[k]) for j in range(N)]
cut1 = lambda fam: any(fam & c == fam for c in cutsets)
def good(fam):
    def rec(S, cand):
        if S and not cut1(S): return False
        while cand:
            k = (cand & -cand).bit_length() - 1; cand &= cand - 1
            if not rec(S | 1 << k, cand & disj[k]): return False
        return True
    return rec(0, fam)
best = None  # stays None if no good family with tau >= 3 is found
random.seed(2)
for t in range(400):
    order = list(range(N)); random.shuffle(order); fam = 0
    for j in order:
        if good(fam | 1 << j): fam |= 1 << j
    if tau(fam, cutsets, 8) < 3: continue
    # shrink while tau stays >= 3
    for j in sorted(range(N), key=lambda j: -bin(ints[j]).count('1')):
        if fam >> j & 1 and tau(fam & ~(1 << j), cutsets, 8) >= 3: fam &= ~(1 << j)
    if best is None or bin(fam).count('1') < bin(best).count('1'): best = fam
print(dims, "minimal good family with tau 3, size", bin(best).count('1'), "good:", good(best), "tau:", tau(best, cutsets, 8))
print(" ".join(show(ints[j]) for j in range(N) if best >> j & 1))
