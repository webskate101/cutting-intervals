"""Exact search (SAT + lazily added goodness clauses) for a good family of connected
intervals in a product of chains that is (T-1)-uncuttable, i.e. needs at least T cuts.

Good = every pairwise disjoint subfamily is 1-cuttable.
Usage: python sat_search.py k1,k2,...,kd T [maxsize]
"""
import sys, time
from pysat.solvers import Cadical153
from explore import setup

dims = tuple(int(x) for x in sys.argv[1].split(','))
T = int(sys.argv[2])
maxsize = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
pts, downs, ints = setup(dims)
ints = [I for I in ints if bin(I).count('1') <= maxsize]
N = len(ints)
full = (1 << N) - 1
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i])
                                for i in range(len(pts)) if I >> i & 1) + "}"
cut = [sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs]
cutsets = [c for c in set(cut) if c]
cutsets = [c for c in cutsets if not any(c != e and c & e == c for e in cutsets)]
disj = [sum(1 << q for q in range(N) if not ints[j] & ints[q]) for j in range(N)]
t0 = time.time()

# tau >= T clauses: for every nested chain of T-1 downsets, some member is uncut.
order = sorted(range(len(downs)), key=lambda i: bin(downs[i]).count('1'))
sub = {i: [j for j in order if downs[j] & ~downs[i] == 0 and j != i] for i in order}
unions = set()
def chains(last, depth, u):
    if depth == 0:
        unions.add(u); return
    for j in sub[last]:
        chains(j, depth - 1, u | cut[j])
for i in order:
    chains(i, T - 2, cut[i])
unions = sorted(unions, key=lambda u: -bin(u).count('1'))
maximal = []
for u in unions:
    if not any(u & v == u for v in maximal): maximal.append(u)
print(f"{N} intervals, {len(maximal)} maximal {T-1}-cut patterns ({time.time()-t0:.1f}s)", flush=True)

s = Cadical153()
for u in maximal:
    s.add_clause([j + 1 for j in range(N) if not u >> j & 1])

def cut1(S):
    return any(S & c == S for c in cutsets)

def bad_subfamilies(fam, limit=200):
    """Minimal-ish pairwise disjoint 1-uncuttable subfamilies of fam (pairs first)."""
    out = []
    idx = [j for j in range(N) if fam >> j & 1]
    for a in idx:
        cand = fam & disj[a] & ~((1 << (a + 1)) - 1)
        while cand:
            b = (cand & -cand).bit_length() - 1; cand &= cand - 1
            S = (1 << a) | (1 << b)
            if not cut1(S):
                out.append(S)
                if len(out) >= limit: return out
    if out: return out
    def rec(S, cand):
        if not cut1(S):
            out.append(S); return len(out) >= limit
        while cand:
            q = (cand & -cand).bit_length() - 1; cand &= cand - 1
            if rec(S | 1 << q, cand & disj[q]): return True
        return False
    for a in idx:
        if rec(1 << a, fam & disj[a] & ~((1 << (a + 1)) - 1)): break
    return out

it = 0
while True:
    it += 1
    if not s.solve():
        print(f"UNSAT after {it} rounds ({time.time()-t0:.1f}s): every good family in "
              f"{'x'.join(f'[{d}]' for d in dims)} (interval size <= {maxsize}) is {T-1}-cuttable.")
        break
    model = s.get_model()
    pos = set(l for l in model if l > 0)
    fam = sum(1 << j for j in range(N) if j + 1 in pos)
    bad = bad_subfamilies(fam)
    if not bad:
        F = [show(ints[j]) for j in range(N) if fam >> j & 1]
        print(f"FOUND good family needing >= {T} cuts ({len(F)} members):", " ".join(F))
        break
    for S in bad:
        s.add_clause([-(j + 1) for j in range(N) if S >> j & 1])
    if it % 20 == 0:
        print(f"round {it}: family size {bin(fam).count('1')}, added {len(bad)} clauses "
              f"({time.time()-t0:.1f}s)", flush=True)
