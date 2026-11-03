"""Empirically test proof strategies for 'good => 3-cuttable' on random good families.
H1: for EVERY maximal downset D containing no member, the members inside X \\ D
    are 2-cuttable.
H2: same, but with the specific cuts D u Min(X\\D) and the complement of a maximal
    member-free upset.
Usage: python hypotheses.py (grid k1,k2,... | random n p) trials seed"""
import sys, random, itertools
from explore import setup
from poset_sat import random_poset, structures


def load():
    rng = random.Random(int(sys.argv[-1]))
    if sys.argv[1] == "grid":
        dims = tuple(int(x) for x in sys.argv[2].split(','))
        pts, downs, ints = setup(dims)
        n = len(pts)
        return lambda: (n, downs, ints), rng
    n, p = int(sys.argv[2]), float(sys.argv[3])
    def gen():
        le = random_poset(n, p, rng)
        downs, ints = structures(n, le)
        return n, downs, ints
    return gen, rng


gen, rng = load()
trials = int(sys.argv[-2])
stats = {"families": 0, "tau3": 0, "H1 fail": 0, "H2 fail": 0}
for t in range(trials):
    n, downs, ints = gen()
    N = len(ints)
    if N == 0: continue
    cut = [sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs]
    cutsets = [c for c in set(cut) if c]
    disj = [sum(1 << q for q in range(N) if not ints[j] & ints[q]) for j in range(N)]
    cut1 = lambda S: any(S & c == S for c in cutsets)
    def ok_to_add(fam, j):
        def rec(S, cand):
            if not cut1(S): return False
            while cand:
                q = (cand & -cand).bit_length() - 1; cand &= cand - 1
                if not rec(S | 1 << q, cand & disj[q]): return False
            return True
        return rec(1 << j, fam & disj[j])
    # random good family, random target size
    fam = 0; target = rng.randint(3, max(3, N))
    for j in rng.sample(range(N), N):
        if bin(fam).count('1') >= target: break
        if ok_to_add(fam, j): fam |= 1 << j
    members = [ints[j] for j in range(N) if fam >> j & 1]
    stats["families"] += 1
    def tau_le(memb, kk):
        idx = [i for i, I in enumerate(ints) if I in memb]
        F = sum(1 << i for i in idx)
        rel = list(set(c & F for c in cutsets if c & F))
        return F == 0 or any((F & ~_or(comb)) == 0 for r in range(1, kk + 1)
                             for comb in itertools.combinations(rel, r))
    def _or(c):
        u = 0
        for x in c: u |= x
        return u
    if not tau_le(members, 2): stats["tau3"] += 1
    contains_member = lambda D: any(I & ~D == 0 for I in members)
    free = [D for D in downs if not contains_member(D)]
    maxfree = [D for D in free if not any(D != E and D & E == D for E in free)]
    full = (1 << n) - 1
    ups_free = [full ^ D for D in downs if not any(I & D == 0 for I in members)]  # complements: upsets containing no member
    # H3: for maximal member-free downset D and maximal member-free upset U, the
    # members inside X \ (D u U) are 1-cuttable ("all" pairs vs "some" pair).
    upfree = [U for U in (full ^ E for E in downs) if not any(I & ~U == 0 for I in members)]
    maxup = [U for U in upfree if not any(U != V and U & V == U for V in upfree)]
    res = [tau_le([I for I in members if I & (D | U) == 0], 1) for D in maxfree for U in maxup]
    stats.setdefault("H3 all fail", 0); stats.setdefault("H3 some fail", 0)
    if not all(res): stats["H3 all fail"] += 1
    if not any(res): stats["H3 some fail"] += 1
    # H5: every maximal free D has a partner U that works.
    # H6/H7: the middle members are all cut by D+ = D u Min(X \ D) (for every / some D).
    below_any = lambda x: [d for d in downs]  # unused helper
    def plus(D):
        # D u Min(X \ D): smallest downset containing D and each minimal element of X\D
        ext = [E for E in downs if E & D == D and bin(E).count('1') == bin(D).count('1') + 1]
        out = D
        for E in ext: out |= E
        return out
    def middle(D, U):
        return [I for I in members if I & (D | U) == 0]
    def cut_by(L, memb):
        return all(I & L and I & ~L for I in memb)
    h5 = all(any(tau_le(middle(D, U), 1) for U in maxup) for D in maxfree)
    h6 = all(any(cut_by(plus(D), middle(D, U)) for U in maxup) for D in maxfree)
    h7 = any(cut_by(plus(D), middle(D, U)) for D in maxfree for U in maxup)
    # H8: every (D, U) maximising |D|+|U| works.  H9: every (D, U) with |D| maximum
    # (and then |U| maximum) works.
    sz = lambda x: bin(x).count('1')
    good_pair = lambda D, U: cut_by(plus(D), middle(D, U))
    best = max(sz(D) + sz(U) for D in maxfree for U in maxup)
    h8 = all(good_pair(D, U) for D in maxfree for U in maxup if sz(D) + sz(U) == best)
    mD = max(sz(D) for D in maxfree); mU = max(sz(U) for U in maxup)
    h9 = all(good_pair(D, U) for D in maxfree for U in maxup if sz(D) == mD and sz(U) == mU)
    for key, val in (("H5 fail", h5), ("H6 fail", h6), ("H7 fail", h7), ("H8 fail", h8), ("H9 fail", h9)):
        stats.setdefault(key, 0)
        if not val: stats[key] += 1
    for D in maxfree:
        rest = [I for I in members if I & D == 0]
        if not tau_le(rest, 2):
            stats["H1 fail"] += 1
            break
print(stats)
