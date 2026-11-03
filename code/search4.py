"""Local search for a good family (every pairwise disjoint subfamily 1-cuttable) of
connected intervals needing >= T cuts.  Usage: python3 search4.py m k T seconds [maxsize]"""
import itertools, random, sys, time
from explore import setup

m, k, T, secs = (int(x) for x in sys.argv[1:5])
maxsize = int(sys.argv[5]) if len(sys.argv) > 5 else 99
pts, downs, ints = setup((m, k))
ints = [I for I in ints if bin(I).count('1') <= maxsize]
N = len(ints)
cut = [sum(1 << j for j, I in enumerate(ints) if I & d and I & ~d) for d in downs]
cut = [c for c in set(cut) if c]
disj = [sum(1 << q for q in range(N) if not ints[j] & ints[q]) for j in range(N)]
show = lambda I: "{" + ",".join("".join(str(c + 1) for c in pts[i])
                                for i in range(len(pts)) if I >> i & 1) + "}"

def cut1(S):
    return any(S & c == S for c in cut)

def violations(fam, j):
    """A pairwise disjoint 1-uncuttable subfamily of fam+{j} containing j, or None."""
    def rec(S, cand):
        if not cut1(S): return S
        while cand:
            q = (cand & -cand).bit_length() - 1; cand &= cand - 1
            r = rec(S | 1 << q, cand & disj[q])
            if r: return r
        return None
    return rec(1 << j, fam & disj[j])

def maximal_restricted(fam):
    rel = set(c & fam for c in cut if c & fam)
    return [c for c in rel if not any(c != e and c & e == c for e in rel)]

def score(fam):
    """Number of (T-1)-subsets of maximal restricted cutsets covering fam (0 => tau >= T)."""
    rel = maximal_restricted(fam)
    return sum(1 for comb in itertools.combinations(rel, T - 1)
               if (fam & ~eval_or(comb)) == 0) if len(rel) <= 40 else 10**6

def eval_or(comb):
    u = 0
    for c in comb: u |= c
    return u

random.seed(int(time.time()))
best = None; t0 = time.time(); restarts = 0
while time.time() - t0 < secs:
    restarts += 1
    fam = 0
    for j in random.sample(range(N), N):
        if not violations(fam, j): fam |= 1 << j
    s = score(fam); temp = 1.0
    for it in range(400):
        j = random.randrange(N)
        if fam >> j & 1: continue
        new = fam | 1 << j
        while True:  # repair: drop a random other member of each bad subfamily
            v = violations(new & ~(1 << j), j)
            if not v: break
            others = [q for q in range(N) if v >> q & 1 and q != j]
            new &= ~(1 << random.choice(others))
        for q in random.sample(range(N), N):  # re-saturate
            if not new >> q & 1 and not violations(new, q): new |= 1 << q
        s2 = score(new)
        if s2 <= s or random.random() < temp * 0.1:
            fam, s = new, s2
        temp *= 0.99
        if s == 0:
            break
    if best is None or s < best[0]:
        best = (s, fam); print(f"restart {restarts}: score {s}", flush=True)
    if s == 0:
        F = [show(ints[q]) for q in range(N) if fam >> q & 1]
        print(f"FOUND good family needing >= {T} cuts, size {len(F)}:", " ".join(F))
        break
print("done", restarts, "restarts; best score", best[0])
