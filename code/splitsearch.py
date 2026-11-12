"""Systematic search for counterexamples to conj:bounded-splitting, i.e. a finite
connected interval Delta (in a product of chains) with no decreasing set S such that
every component of S and of Delta \\ S has an upper or a lower bound in Delta.

  python splitsearch.py exhaustive k1,k2,...            -- every connected interval
  python splitsearch.py local k1,k2,... seconds seed     -- local search, fewest splittings

An interval is represented as Delta = A \\ B with B subset A downsets of the grid.
"Hardness" of Delta = number of bounded splittings (counted up to CAP).
"""
import sys, itertools, random, time

CAP = 50


def grid(dims):
    pts = list(itertools.product(*[range(1, k + 1) for k in dims]))
    n = len(pts)
    le = lambda p, q: all(a <= b for a, b in zip(p, q))
    below = [sum(1 << j for j in range(n) if le(pts[j], pts[i])) for i in range(n)]
    above = [sum(1 << j for j in range(n) if le(pts[i], pts[j])) for i in range(n)]
    return pts, below, above


def all_downsets(n, below, universe=None):
    universe = (1 << n) - 1 if universe is None else universe
    strict = [below[i] & ~(1 << i) & universe for i in range(n)]
    downs = {0}; frontier = [0]
    while frontier:
        new = []
        for D in frontier:
            free = universe & ~D
            while free:
                i = (free & -free).bit_length() - 1; free &= free - 1
                if strict[i] & ~D == 0:
                    E = D | 1 << i
                    if E not in downs: downs.add(E); new.append(E)
        frontier = new
    return downs


class Sub:
    """The subposet Delta of the grid, with fast component / bound tests."""
    def __init__(self, delta, below, above):
        self.delta = delta
        self.idx = [i for i in range(len(below)) if delta >> i & 1]
        self.below = {i: below[i] & delta for i in self.idx}
        self.above = {i: above[i] & delta for i in self.idx}
        self.adj = {i: self.below[i] | self.above[i] for i in self.idx}

    def components(self, m):
        out = []
        while m:
            seen = m & -m; fr = seen
            while fr:
                nf = 0
                while fr:
                    i = (fr & -fr).bit_length() - 1; fr &= fr - 1
                    nf |= self.adj[i]
                nf &= m & ~seen; seen |= nf; fr = nf
            out.append(seen); m &= ~seen
        return out

    def bounded(self, C):
        ub = lb = self.delta
        c = C
        while c and (ub or lb):
            i = (c & -c).bit_length() - 1; c &= c - 1
            ub &= self.above[i]; lb &= self.below[i]
        return bool(ub or lb)

    def is_splitting(self, S):
        return all(self.bounded(C) for C in self.components(S)) and \
               all(self.bounded(C) for C in self.components(self.delta & ~S))

    def count_splittings(self, cap=CAP):
        """Number of bounded splittings (stops at cap); BFS over relative downsets."""
        strict = {i: self.below[i] & ~(1 << i) for i in self.idx}
        seen = {0}; frontier = [0]; count = 0; total = 0
        while frontier:
            new = []
            for D in frontier:
                total += 1
                if self.is_splitting(D):
                    count += 1
                    if count >= cap: return count, None
                free = self.delta & ~D
                while free:
                    i = (free & -free).bit_length() - 1; free &= free - 1
                    if strict[i] & ~D == 0:
                        E = D | 1 << i
                        if E not in seen: seen.add(E); new.append(E)
            frontier = new
        return count, total


def show(m, pts):
    return "{" + ",".join("".join(map(str, pts[i])) for i in range(len(pts)) if m >> i & 1) + "}"


def connected_pieces(delta, below, above):
    return [C for C in Sub(delta, below, above).components(delta) if C & (C - 1)]


def exhaustive(dims):
    pts, below, above = grid(dims)
    n = len(pts)
    downs = sorted(all_downsets(n, below), key=lambda d: bin(d).count('1'))
    seen = set(); results = []; t0 = time.time()
    for A in downs:
        for B in downs:
            if B & ~A or B == A: continue
            for delta in connected_pieces(A & ~B, below, above):
                if delta in seen: continue
                seen.add(delta)
                c, tot = Sub(delta, below, above).count_splittings()
                if c < CAP: results.append((c, tot, delta))
                if c == 0:
                    print("COUNTEREXAMPLE:", show(delta, pts), flush=True)
    results.sort(key=lambda r: (r[0], r[0] / (r[1] or 1)))
    print(f"{'x'.join(map(str, dims))}: {len(seen)} connected intervals "
          f"({time.time()-t0:.0f}s); fewest bounded splittings:")
    for c, tot, delta in results[:8]:
        print(f"  {c:3d} of {tot:6d} downsets  |Delta|={bin(delta).count('1'):2d}  {show(delta, pts)}")
    return pts, results


def local(dims, seconds, seed):
    """Simulated annealing on Delta = A minus B, minimising #bounded splittings."""
    pts, below, above = grid(dims)
    n = len(pts); full = (1 << n) - 1
    rng = random.Random(seed)
    strict_b = [below[i] & ~(1 << i) for i in range(n)]
    strict_a = [above[i] & ~(1 << i) for i in range(n)]
    def moves(D):
        # downsets differing from D by one element
        out = []
        for i in range(n):
            if D >> i & 1:
                if strict_a[i] & D == 0: out.append(D & ~(1 << i))
            elif strict_b[i] & ~D == 0:
                out.append(D | 1 << i)
        return out
    def score(A, B):
        pieces = connected_pieces(A & ~B, below, above)
        if not pieces: return 10**9, None
        best = None
        for delta in pieces:
            c, tot = Sub(delta, below, above).count_splittings()
            # fewer splittings is better; break ties by more downsets (harder)
            key = c * 10**6 - (tot or 0)
            if best is None or key < best[0]: best = (key, delta, c, tot)
        return best[0], best
    t0 = time.time(); overall = None; restarts = 0
    while time.time() - t0 < seconds:
        restarts += 1
        # random start: A = L(random antichain-ish), B = L(random) & A
        A = 0
        for i in rng.sample(range(n), rng.randint(2, 5)): A |= below[i]
        B = 0
        for i in rng.sample(range(n), rng.randint(1, 4)): B |= below[i]
        B &= A
        cur, info = score(A, B); temp = 3.0
        for it in range(300):
            if rng.random() < 0.5:
                cand = [(a, B) for a in moves(A) if B & ~a == 0]
            else:
                cand = [(A, b) for b in moves(B) if b & ~A == 0]
            if not cand: continue
            A2, B2 = rng.choice(cand)
            s2, info2 = score(A2, B2)
            if s2 <= cur or rng.random() < pow(2.718, -(s2 - cur) / (temp * 10**6)):
                A, B, cur, info = A2, B2, s2, info2
            temp *= 0.985
            if info and info[2] == 0: break
        if info and (overall is None or info[0] < overall[0]):
            overall = info
            print(f"restart {restarts}: {info[2]} splittings of {info[3]} downsets, "
                  f"|Delta|={bin(info[1]).count('1')}: {show(info[1], pts)}", flush=True)
        if info and info[2] == 0:
            print("COUNTEREXAMPLE FOUND"); break
    print(f"done: {restarts} restarts in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    mode = sys.argv[1]; dims = tuple(int(x) for x in sys.argv[2].split(','))
    if mode == "exhaustive":
        exhaustive(dims)
    else:
        local(dims, int(sys.argv[3]), int(sys.argv[4]))
