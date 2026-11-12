# README, Claude

## Basic setup of the project

This is a project in mathematical research so I want you to be a talented
mathematical researcher. We are going to explore a topic in combinatorics,
specifically the theory of partially ordered sets. I know some of the results
which we will explore, but there are questions which I do not know the answer
to and I hope we will find them together!

RULE 1: Everything you write should be in the folder `cutting-intervals/`.

To start with, there are two files, this one, and `main.tex`.

RULE 2: All mathematical results should go in `main.tex` and at each stage you should
ensure that the LaTeX compiles cleanly with `pdflatex`. We will both add mathematics
to the file as we proceed.

RULE 3: You may add text at the end of `main.tex` but you MUST get confirmation from
me before changing any previously-existing text in `main.tex`. However you
may delete "% Claude" comments in `main.tex` when you have responded to them.

RULE 4: Use this file, `README-CLAUDE.md`, for discussion, suggestions, and reports on ideas. Keep a log of our discussions in this file.



## Discussion log

### 2026-11-01: First lemma (interval as a difference of sets)

**Request:** prove "Every interval is the set theoretic difference of an
increasing set and a decreasing set."

**Claude:** That statement is false as written. If `U` is increasing and `D` is
decreasing, then `X \ D` is increasing, so `U \ D = U ∩ (X \ D)` is *increasing*.
Any non-increasing interval is a counterexample, e.g. `{0}` in the chain `0 < 1`.

What I put in `main.tex` instead (Lemma 1, with proof): for `I ⊆ X` these are equivalent:
1. `I` is an interval;
2. `I = L1 \ L2` with `L2 ⊆ L1` both decreasing (take `L1 = ↓I`, `L2 = ↓I \ I`);
3. `I = U1 \ U2` with `U2 ⊆ U1` both increasing (dually, `U1 = ↑I`, `U2 = ↑I \ I`);
4. `I = U ∩ L` with `U` increasing and `L` decreasing.

The only step with real content is showing `↓I \ I` is decreasing, which is where
order convexity gets used. I also added notation for `↓A` and `↑A`, and an
Example recording the counterexample. If you meant a different statement, e.g.
"an increasing set minus an *increasing* set", tell me and I'll change it.

**Possible next directions:** the decompositions in (2) and (3) are canonical:
`↓I` is the smallest decreasing `L1` that works, and `↓I \ I` is then forced.
"Cutting" an interval might mean splitting it as `I = I' ⊔ I''` with `I'` a
decreasing subset of `I` and `I''` an increasing subset of `I`; these cuts
correspond to the decreasing subsets of `I` and form a distributive lattice. Is
that the idea you have in mind?

### 2026-11-01: Notation and simplifying Lemma 1

**Request:** drop the arrow notation and use `L(x) = {y : y ≤ x}`, `U(x) = {y : y ≥ x}`,
with `L(A)`, `U(A)` defined analogously. Drop the `L2 ⊆ L1` condition.

**Claude:** Done. `L(A)` and `U(A)` are now defined as the unions of the `L(a)` and
`U(a)` over `a ∈ A`, and are noted to be the smallest decreasing and increasing sets
containing `A`. The proof of Lemma 1 now uses them. Removing the containment
conditions doesn't affect the proof: (2)⇒(4) and (3)⇒(4) never used them, and the
witnesses built in (1)⇒(2) and (1)⇒(3) happen to satisfy them anyway.

Small notation point: Lemma 1(4) still writes `U` and `L` for an arbitrary
increasing or decreasing set, alongside the operators `U(·)` and `L(·)`. The
parentheses tell them apart, but if you'd rather avoid the overlap we could
rename the generic sets.

### 2026-11-01: Examples of n-uncuttable collections

**Request:** give examples of n-uncuttable collections, using only finite posets.

**Claude:** Added to `main.tex`:
- **Trivial cases (Lemma 2):** intervals with ≤ 1 element can never be cut. An
  interval with ≥ 2 elements is cut by `L(x)` for any minimal `x` in it. So a
  collection of `N` intervals of size ≥ 2 is always `N`-cuttable, and the real
  question is how far below `N` the number of cuts can go.
- **Chains (Example 1):** in `1 < 2 < ... < n+2`, the `n+1` covering pairs
  `{j, j+1}` are `n`-uncuttable, because each initial segment cuts only one of
  them. The same holds for any `n+1` intervals in a chain that meet at most in
  shared endpoints.
- **Antichains (Example 2):** on an `m`-element antichain, all pairs are
  `n`-cuttable iff `m ≤ 2^n`. The argument encodes each point by its 0/1 membership
  in `L_1, ..., L_n` (a binary encoding with pigeonhole). This shows a collection can
  be `n`-uncuttable even though every two of its members are `n`-cuttable.

**Possible questions to pursue:**
1. *Chains:* I believe a collection in a chain is `n`-uncuttable iff it contains
   `n+1` intervals as in Example 1. Each interval `I` gives the half-open range
   `[min I, max I)` of initial segments that cut it, and this is the Gallai
   piercing/packing duality for intervals of a line. I haven't added it to
   `main.tex` yet; shall I?
2. *General posets:* the antichain example shows this duality fails in general. No
   two pairs need separate cuts, yet about `log2 m` cuts are needed. Is the number of
   cuts needed bounded by a function of the packing number (the largest
   subcollection in which each decreasing set cuts at most one member), perhaps
   together with the width of `X`? For an antichain the width is `m`, so `log2 m`
   is consistent with a bound like `f(packing) · log(width)`.
3. Which posets, or which kinds of collections (e.g. all intervals of size 2, or
   all intervals of `X`), give the largest gap between the number of cuts needed
   and the trivial bound `N`?

### 2026-11-01: Rules added to the setup

**Request:** re-read the setup, which now has numbered RULE headings, including a
new Rule 3: Claude may add text at the end of `main.tex` but must get confirmation
before changing any existing text.

**Claude:** Acknowledged. From now on I only append to the end of `main.tex`. Any
change to existing text, including typo fixes, notation changes or correcting a
false statement, I'll propose here or in chat and wait for your go-ahead. I asked
how to treat `% Claude, ...` request comments placed mid-file (see chat).

### 2026-11-01: Rule 3 clarified

**Change:** Rule 3 now allows Claude to delete `% Claude` comments in `main.tex`
once it has responded to them.

**Claude:** Understood. When you leave a `% Claude, ...` request, I'll write the
response and then delete the comment. Two `% Claude:` comments I wrote myself are
still in `main.tex`: the note about the false original statement of Lemma 1 and the
marker before the examples. They aren't requests from you, so I'll leave them
unless you confirm I can remove them.

### 2026-11-01: Example in products of chains

**Request:** we'll focus on posets that are cartesian products of chains; give an
example of that kind.

**Claude:** Appended Example 3 to the end of `main.tex`, for `X = [k_1] × ... × [k_d]`
and `N = Σ (k_i − 1)`:
- **(a)** The collection of all covering pairs `{x, x + e_i}` needs exactly `N` cuts.
  The upper bound uses the coordinate cuts `{x : x_i ≤ t}`. For the lower bound,
  take a maximal chain in `X`: a decreasing set cuts at most one of its `N`
  consecutive pairs, which is Example 1 applied inside `X`.
- **(b)** In `[m] × [m]`, the pairs from the anti-diagonal antichain need exactly
  `⌈log2 m⌉` cuts. This works because `S ↦ L(S)` lets decreasing sets pick out any
  subset of an antichain, so Example 2 carries over.

**Follow-up (Theorem 1, appended):** the coordinate cuts handle *every*
collection. Two distinct points differ in some coordinate, `a_i < b_i`, and then
`{x : x_i ≤ a_i}` separates them. So every collection of intervals of size `≥ 2`
in `[k_1] × ... × [k_d]` is `N`-cuttable, and by (a) the collection of all such
intervals needs exactly `N` cuts.

**Possible questions for products of chains:**
1. Every collection needs at most `N` cuts, and antichain pairs need only about
   `log2 m`. For a given collection `I`, what determines the minimum number of cuts?
   Natural lower bounds: the number of steps in the longest "chain of covering-type
   pairs" in `I` (as in (a)), and `log2` of the size of a "separating antichain" (as
   in (b)). Is the minimum always within a constant factor of the larger of these?
2. Note that Theorem 1 only uses that the intervals have at least two points, not
   that they are convex. The convexity of `I` doesn't seem to matter until we look
   at collections that aren't just pairs. Is there a natural problem where it does
   matter, e.g. cuts with extra conditions, or counting how *many* times each
   interval is cut?

### 2026-11-01: The conjecture on connected intervals

**Request:** read the Conjecture (Section "Connected Intervals") and give thoughts.

**Restatement.** Call a family *good* if every pairwise disjoint subfamily is
1-cuttable. The conjecture says that in `[k_1] × ... × [k_d]`, every good family of
connected intervals is `n(d)`-cuttable, with `n(d)` independent of the `k_i`. It is a
Gallai/Helly-type statement: "packing number 1 ⇒ bounded piercing number".

**Why both hypotheses are needed.**
- *Connected:* Example 3(b). Pairs from the anti-diagonal are disconnected. Every
  disjoint subfamily `{a_j, b_j}` is cut by `L({a_1, a_2, ...})`, yet `⌈log2 m⌉`
  cuts are needed. So without connectivity there is no bound.
- *Disjoint:* `{1,2}, {2,3}` in a chain is 1-uncuttable, but its only disjoint
  subfamilies are single intervals. So we must have `n(d) ≥ 2`.

**Why connectivity helps.** In a product of chains, if `x ≤ y` are both in an
interval `I`, then the box `[x, y]` is contained in `I`, and a box is connected
through covering pairs. So a connected interval is connected in the Hasse diagram,
and `L` cuts `I` iff `L` cuts some covering pair inside `I`. This is where order
convexity finally matters (Theorem 1 didn't use it).

**d = 1 is true, with `n(1) = 2` sharp.** Sketch: in a chain, `{x ≤ k}` cuts `I`
iff `k ∈ [min I, max I − 1]`. On a line, the number of points needed to hit every
interval in a family equals the largest number of pairwise disjoint intervals in
it (Gallai). So if a family needs 3 cuts, it contains `I_1, I_2, I_3` with
`max I_1 ≤ min I_2` and `max I_2 ≤ min I_3`. Then `I_1, I_3` are disjoint and no
single cut handles both. Sharpness: `{1,2}, {2,3}`.

**Computer experiments** (`code/`, brute force on small products):
- Random greedy search over maximal good families. The largest cut number found
  is 2 for chains and `[2]×[3]`, and 3 for `[3]×[3]`, `[3]×[4]`, `[4]×[4]` and
  `[2]^3`. So `n(2) ≥ 3`, and the data so far is consistent with a small constant.
  The search is random, not exhaustive.
- A 5-interval witness in `[3]×[3]` (writing `ij` for `(i,j)`):
  `{12,13}, {11,12,21}, {21,31}, {31,32}, {13,23,32,33}`. Consecutive members
  overlap *cyclically*, so it is a 5-cycle going round the grid. The only disjoint
  subfamilies are pairs, each 1-cuttable, but 3 cuts are needed. It looks like the
  odd-cycle obstruction for circular-arc families, which is new behaviour compared
  with chains.
- **Pairs aren't enough to test goodness.** In `[3]×[3]` the disjoint triple
  `{12,13}, {21,31}, {23,32,33}` is 1-uncuttable although each pair in it is
  1-cuttable. So "good" can't be checked on pairs alone, and the conjecture really
  does need subcollections of arbitrary size.

**Proposed next steps** (pending your choice):
1. Write up `d = 1` (`n(1) = 2`) as a theorem, and the `[3]×[3]` 5-cycle as an
   example showing `n(2) ≥ 3`.
2. Larger or exhaustive search in `d = 2` for a good family needing 4 cuts. Longer
   odd cycles in bigger grids are the natural candidates.
3. Look for a proof in `d = 2`. One idea: a decreasing set in `[k]×[k]` is a
   staircase, and a good family might be forced to lie close to a single
   staircase, which would then let a bounded number of shifted staircases cut it.

### 2026-11-01: d = 1 theorem, pentagon example, related work

**(a) Added to the end of `main.tex`:**
- **Theorem 2** (`d = 1`): in a chain, every 2-uncuttable collection contains two
  disjoint intervals that no single set cuts together, and 2 can't be replaced by 1.
  The proof is a greedy argument (the usual proof of Gallai's theorem for
  intervals), written directly in terms of the cuts `L_t`.
- **Example 4** (the "pentagon"): the 5-cycle of intervals in `[3]×[3]`, with a
  hand proof that it is 2-uncuttable but every disjoint subcollection is
  1-cuttable. So if `n(2)` exists, `n(2) ≥ 3`. The proof doesn't rely on the
  computer search.

**(b) Related work.** I'm citing from memory, so check the references before
relying on them. I don't know of this exact conjecture in the literature.
1. *Gallai-type theorems / perfect graphs:* for intervals on a line, the minimum
   number of points hitting all intervals equals the maximum number of pairwise
   disjoint ones. Theorem 2 is essentially this.
2. *Piercing vs packing for "relatives of intervals":* Gyárfás & Lehel (1970s–80s)
   on `d`-intervals and boxes. Tardos (Combinatorica 1995) showed `τ ≤ 2ν` for
   2-intervals. Kaiser (Discrete Comput. Geom. 1997) showed `τ ≤ (d² − d)ν` for
   `d`-intervals. These are the closest in spirit: bounds depending only on `d`,
   with topological proofs.
3. *Axis-parallel boxes:* boxes in the plane do *not* have `τ` bounded by a function
   of `ν` alone. But for rectangles that all meet a fixed diagonal line, or more
   generally a monotone curve, there are constant-factor bounds. I recall Correa,
   Feuilloley, Pérez-Lantero & Soto (DCG ~2015) and work of Chudnovsky, Spirkl &
   Zerbib. This seems especially relevant, because a decreasing set in `[k]×[k]`
   is a staircase, i.e. a monotone curve. Our "cut by a staircase" is like
   "stabbed by a monotone curve".
4. *Hadwiger–Debrunner `(p,q)` problem / Alon–Kleitman (1992):* the general principle
   that a local intersection condition gives bounded piercing. The pentagon and the
   bad triple show our local condition must involve whole disjoint subcollections,
   not just pairs, which is closer to `(p,q)` than to Helly.
5. *Dimension theory of posets (Trotter's book, 1992):* the antichain example is the
   statement that the *2-dimension* (Boolean dimension of the embedding into `2^n`)
   of an `m`-antichain is `⌈log2 m⌉`. The 2-dimension of a poset is the least
   number of decreasing sets needed to separate the non-comparable pairs, which is
   closely related to our cut number for collections of pairs.
6. *Abstract convexity (van de Vel, Theory of Convex Structures, 1993):* order
   convexity is a standard convexity structure, with known Helly/Radon numbers. It
   may be relevant to the bad triple, the failure of a pairwise reduction.

I can do a literature search to confirm these references and look for anything
closer, especially on stabbing families of connected sets by monotone curves.

*(Note: example numbers in this log were corrected to match the compiled PDF: Chains = Ex. 1, Antichains = Ex. 2, Products of chains = Ex. 3, Pentagon = Ex. 4.)*

### 2026-11-01: Simpler proof of Theorem 2

**Change (by John):** replaced Claude's greedy proof with a direct one. Take `I_1`
with the smallest `max`, and use the two cuts `L(max I_1 − 1)` and `L(max I_1)`.
Anything they both miss is disjoint from `I_1` and lies entirely above it.

**Claude:** The proof is correct and better than mine. It finds the disjoint pair
directly, without going through a third interval. Suggested tightenings (not
applied; Rule 3):
1. *Notation:* the first paragraph and the sharpness paragraph use `L_t`, but the
   new argument uses `L(s)`, `L(t)`. Since `L(t) = {1, ..., t}` by our Definition,
   I suggest using `L(t)` throughout and dropping `L_t`.
2. "Since `L(s)` and `L(t)` do not cut `I`" should be "do not cut every member of `I`".
3. "If `min I_2 ≤ s` then `L(s)` cuts `I_2`" also uses `s < max I_1 ≤ max I_2`, by
   the choice of `I_1`. Worth saying.
4. "the only possibility is `min I_2 = t`, and so `L(t)` cuts `I_2`" uses
   `max I_2 > t`, which holds because `|I_2| ≥ 2`.
5. The final claim that `{I_1, I_2}` is 1-uncuttable needs one line: `L(u)` cuts
   `I_1` only if `u < max I_1`, and cuts `I_2` only if `u ≥ min I_2 > max I_1`.
6. Delete the commented-out greedy proof?

**Decision (John):** apply 1, 2 and 6. Points 3–5 are obvious to the reader, so
omit them. **Claude:** Done. `L_t` → `L(t)` throughout the proof, "cut every
member of `I`", and the commented-out greedy proof removed. Compiles cleanly.

### 2026-11-02: New lemmas and a shorter proof for the pentagon

**Change (by John):** added Lemma `lem:incomparabale-sets-separate` (a connected set
inside the union of two incomparable sets lies in one of them) and Lemma
`lem:cup-cap-cuts` (if `L_1, L_2` cut a collection of connected intervals, so do
`L_1 ∩ L_2, L_1 ∪ L_2`). Used them to shorten the 2-uncuttability proof in the
pentagon example by assuming `L_1 ⊆ L_2`.

**Claude:** Both lemmas are correct, and the uncrossing idea is a good one. Review
(nothing changed; Rule 3):
1. *Gap in the pentagon proof.* "But `L_1` must also cut `B`" isn't justified, and
   `L_2` *can* cut `B` and `D` together (e.g. `{11,21,31}`). Suggested fix: "Since
   `21 ∈ L_1 ⊆ L_2`, if `L_2` cut `B` then `12 ∉ L_2 ⊇ L_1`, and neither set could
   cut `A`. So `L_1` cuts `B`."
2. *Typos.* Lemma `cup-cap-cuts`: "`L_2` and `L_2`" → "`L_1` and `L_2`";
   "does not cuit `E`" → "does not cut `I`"; "must belong to one of them" → "must
   be contained in one of them". Lemma `incomparable-sets-separate`: "`x1`" →
   "`x_1`", "comparablie" → "comparable".
3. *Small points.* In Lemma `incomparable-sets-separate`, `x_{k+1}` exists because
   incomparable sets are disjoint (`x ≤ x`), so `b ∉ A` and `k < n`. Also, "the sets
   `L_1, ..., L_n` cut `I`" is used but never defined; one sentence near the
   definition of `n`-cuttable would fix that. Lemma `cup-cap-cuts` uses only
   connectedness, not convexity.
4. *Suggested corollary (new text, to append):* if `L_1, ..., L_n` cut a collection
   of connected sets in a finite poset, then some **nested** `L'_1 ⊆ ... ⊆ L'_n`
   also cut it. Proof: repeatedly replace a non-nested pair by its intersection and
   union. This strictly increases `Σ |L_i|²` (by `2·|L_1 \ L_2|·|L_2 \ L_1|`), so it
   terminates. Consequence: in the conjecture we may always assume the cuts form a
   chain. In `[k]×[k]` that means nested staircases, which should make the `d = 2`
   case much easier to think about.

**Follow-up (John):** added a justification for point 1 and fixed the typos. Asked
Claude to give line numbers when reporting typos from now on.
**Claude:** Will do. The new justification is correct ("if `L_1` didn't cut `B`, then
`B ⊆ L_1 ⊆ L_2`", since `11, 21 ∈ L_1`). One wording point: at `main.tex:353–354`,
"But this can only happen if `L_1` excludes `12`" reads as if "this" means
`B ⊆ L_1`. It means "`L_1` cutting `B`". Suggest: "…`B ⊆ L_1 ⊆ L_2`. Since
`21 ∈ L_1`, cutting `B` requires `12 ∉ L_1`, so `L_1 = {11, 21}` …".
The corollary on nested cuts is still pending your OK.

### 2026-11-02: Nested cuts

**Claude:** Appended Theorem `thm:nested-cuts` (compiled as Theorem 2.7). In a finite
poset, if a collection of connected intervals is `n`-cuttable, it is cut by a chain
`L_1 ⊆ ... ⊆ L_n` of decreasing sets. The proof picks a cutting `n`-tuple
maximising `Σ |L_i|²` and uncrosses any non-nested pair with Lemma `cup-cap-cuts`.
Uncrossing raises the sum by `2pq`. Leftover typo: `main.tex:271` "does not cut
`$E$`" should be "`$I$`". There's no `corollary` environment, so it is stated as a
theorem; adding one would mean changing the preamble.

**Follow-up (John):** keep it as a theorem; added a `corollary` environment for future use.

### 2026-11-02: Second attempt at the conjecture (d = 2)

Terminology: a collection is **good** if every pairwise disjoint subcollection is
1-cuttable. The conjecture says good ⇒ `n(d)`-cuttable.

**1. Reformulation via linear extensions (proof sketch, not yet in `main.tex`).**
For connected intervals in any finite poset,
`τ(I) = min over linear extensions σ of ν_σ(I)`. Here `τ` is the least `n` with
`I` `n`-cuttable, and `ν_σ` is the largest number of members whose σ-windows
`[first_σ I, last_σ I)` are pairwise disjoint. Reason: by Theorem `nested-cuts` the
optimal cuts can be taken nested, so they are prefixes of one linear extension σ.
For fixed σ, a prefix of length `t` cuts `I` iff `t` lies in the window, so this is
the `d = 1` problem and Gallai applies. So the conjecture asks for a σ with no long
run of σ-separated members.

**2. Exact computations** (`code/sat_search.py`, SAT solver with goodness clauses
added lazily; UNSAT is a proof for that poset). "Every good family is 3-cuttable"
holds in:
`[3]×[3]` (3 is attained by the pentagon), `[4]×[4]`, `[4]×[5]`, `[2]×[2]×[3]`,
`[2]×[2]×[4]`, `[2]×[3]×[3]`, `[2]^4`. `[5]×[5]` is still running.
`code/poset_sat.py`: the same holds in 1,130 random posets with 8–13
elements. (Families needing 3 cuts are common there, so the test isn't vacuous.)

**Conjecture′ (stronger).** In *every* finite poset, a good collection of connected
intervals is 3-cuttable. This would give `n(d) = 3` for all `d ≥ 2`, independent
of `d`. The evidence suggests the reason is order-theoretic, not geometric.

**3. A proof strategy that survived every test** (`code/hypotheses.py`). Call a
decreasing set *free* if it contains no member, and likewise for increasing sets.
*Target lemma:* if `I` is good, there are a maximal free decreasing set `D` and a
maximal free increasing set `U` such that every member inside `X \ (D ∪ U)` meets
`P = Min(X \ D)`.
The lemma implies Conjecture′, using the three cuts `D`, `D ∪ P` and `X \ U`:
- `D` cuts every member meeting `D` (`D` is free).
- `X \ U` cuts every member meeting `U` (`U` is free).
- `D ∪ P` cuts every member in the middle, because such a member meets `P` and a
  connected set with `≥ 2` points can't lie inside the antichain `P`.
In `d = 1` this is exactly John's proof of Theorem 2 (`D = L(max I_1 − 1)`,
`P = {max I_1}`).
Tested on 940 random good families (grids and random posets):
- The target lemma never failed.
- "*Every* pair `(D, U)` works" fails.
- "*Every* maximal free `D` has a partner `U`" fails, rarely.
- "The members avoiding an arbitrary maximal free `D` are 2-cuttable" fails, rarely.
So a proof has to choose `D` and `U` carefully. I don't yet know the right
extremal choice.
Caveat: in the random-poset runs the sampled families were all 2-cuttable, so the
real test of the lemma is the grid runs.

**Suggested next steps:** (a) find the right choice of `(D, U)` and prove the target
lemma, perhaps by an extremal choice (e.g. maximise `|D| + |U|`) plus goodness
applied to `{I_p, K}` or `{I_p, K, J_q}`, where `I_p ⊆ D ∪ {p}` and `J_q ⊆ U ∪ {q}`
are the witnesses to maximality; (b) write up the linear-extension reformulation.
*Update:* the obvious extremal choices fail. Maximising `|D| + |U|`, or maximising
`|D|` and `|U|` separately, breaks the target lemma in a few percent of grid
families (17 of 490). The right choice of `(D, U)` is still open.

### 2026-11-02: Write-up

Appended section "Investigation and Next Steps" to `main.tex`. It contains the linear-extension theorem (with proof), the exact computations, Conjecture `conj:three`, Theorem `thm:three-cuts` (the target lemma implies 3 cuts, with proof), Conjecture `conj:target`, the strategies that failed, and next steps. Numbers corrected: 1,130 random posets with 8–13 points; 940 families for the strategy tests. `[5]x[5]` still running.

### 2026-11-11: Review of `thm:2d-zig-zag`; higher dimensions; free sets

**Request (John, comment at `main.tex:793`):** look at the new material (commit
212cab2), especially `thm:2d-zig-zag`: (1) a version in 3+ dimensions? (2) 3 as a
boundary; (3) connections to free sets and `thm:three-cuts`.

**Review.** The lemmas and the theorem are correct apart from one small gap.
- *Gap, `main.tex:788–790`:* for `i = 0` the point `(x_0, y_0)` is not in `Δ`, so
  "`(x_0,y_0) ∈ D`, contrary to fact" doesn't give a contradiction. Fix: use
  `q_0 = (x_0+1, y_0) ∈ Δ` instead. `J ⊆ U(q_0)` gives `q_0 ∈ D`, contradicting
  `Δ ∩ D = ∅`. (For `i ≥ 1`, `(x_{2i}, y_{2i}) ∈ Δ` is fine.)
- *Typos:* `main.tex:671` "interals"; `:674` missing full stop; `:679` "the set of
  `$x\in…$`" should be `$p\in…$`; `:686` "So supppose `D∩U=∅`" (also it is a
  conclusion, so "Hence `D∩U=∅`"); `:745` "agument"; `:775` "`$l>x_0$`" should be
  "`$l>0$`".

**(1) Higher dimensions.** The proof splits into a general part and one 2-D fact.
The 2-D fact is that the staircase `L = ∪ L(p_i)` splits `Δ` into pieces, each
bounded by a point of `Δ`. The argument only needs each piece of `L ∩ Δ` and of
`Δ \ L` to be bounded *above or below* by a point of `Δ`. A member `J` inside a
piece bounded below by `s ∈ Δ` gives `s ∈ D`, which is also a contradiction. So
call a decreasing set `S` of a poset `P` a **bounded splitting** if every connected
component of `S` and of `P \ S` has an upper or a lower bound in `P`. Then:

*Theorem A (any finite poset, proof = John's).* Let `D_I = {p : U(p) contains a
member}`, `U_I = {p : L(p) contains a member}`, `Δ = X \ (D_I ∪ U_I)`. If `I` is
3-uncuttable and `Δ` (as a poset in its own right) has a bounded splitting, then
some member lies inside `D_I` or inside `U_I`.

*Conjecture (bounded splitting).* Every finite poset has a bounded splitting.
- Evidence (`code/zigzag.py`, `code/relaxed_sample.py`, `code/splitting.py`): true
  for *every* interval of `[3]×[3]`, `[4]×[4]`, `[2]×[3]×[3]`, `[2]×[2]×[4]` and
  `[2]^4` (exhaustive); for 3,000 sampled intervals of `[3]^3`, 800 of `[3]×[3]×[4]`
  and 1,000 of `[2]^3×[3]`; for 353 random connected posets with 12–18 elements;
  and for every interval of 580 random posets with 10–13 elements. With Theorem A, the
  exhaustive checks *prove* John's theorem for `[2]×[3]×[3]`, `[2]×[2]×[4]` and
  `[2]^4` (computer-assisted).
- John's *strict* version (each piece of `L ∩ Δ` bounded above and each piece of
  `Δ \ L` bounded below) **fails in 3-D**. The interval
  `{112,113,121,122,123,131,132,133,212,221,222}` in `[2]×[3]×[3]` has no such cut.
  So the relaxation is needed.
- Principal cuts (`L = L(r)` or `X \ U(r)` with `r ∈ Δ`) are not enough either.
  `{113,121,122,123,131,211,212,213,221,231,311,321,331}` in `[3]^3` needs a
  5-generator cut: `{113,121,122,131,211,212,311}`.

**(2) Is 3 a boundary?** Theorem A uses exactly three cuts: `D_I`, `X \ U_I` and
the splitting. Its proof never mentions dimension, which fits the data from
2026-11-02 (good ⇒ 3-cuttable in every poset tested, any dimension). I agree this
is more evidence that 3 is the right number, and that dimension isn't.

**(3) Free sets.** `X \ U_I` is the union of all *free principal* downsets `L(p)`,
and `D_I` is the union of all `L(p)` with `U(p)` not free. Both proofs have the
same shape: two outer cuts kill everything meeting a free region, and one middle
cut handles `Δ`.
- *`thm:three-cuts`:* maximal free `D`, `U`; middle cut `D ∪ Min(X \ D)`. It needs
  a hypothesis about members in `Δ` and a careful choice of `(D, U)`.
- *`thm:2d-zig-zag` / Theorem A:* canonical `D_I`, `U_I`; middle cut a bounded
  splitting. It needs `D_I`, `U_I` free. This is automatic in the contrapositive.

What is missing to reach the conjecture is the link to **goodness**:
- If `I_0 ⊆ U_I`, choose for each minimal `a` of `I_0` a member `I_a ⊆ L(a)`. Then
  `{I_0} ∪ {I_a}` is 1-uncuttable, because a cut of `I_0` contains some such `a`
  and hence all of `I_a`. And `I_a ∩ I_0 ⊆ {a}`. So 3-uncuttable ⇒ a 1-uncuttable
  "star". Goodness forbids this only if the star is pairwise disjoint.
- Goodness alone can't give freeness of `D_I`, `U_I`. `{r,p}, {p,p'}` with
  `r < p < p'` is good but `{p,p'} ⊆ U_I`. So a proof of the conjecture has to use
  3-uncuttability again to make the star disjoint. Strict versions
  `U°_I = {p : some member ⊆ L(p) \ {p}}` (and `D°_I`) remove the overlaps with `I_0`.
  Good ⇒ `D°_I ∩ U_I = ∅ = D_I ∩ U°_I`, because a point in both gives a disjoint
  1-uncuttable pair. The remaining problem is overlaps among the `I_a` themselves.

**Suggested next steps:** (a) prove the bounded-splitting conjecture, which is now
a self-contained statement about finite posets; (b) make the star disjoint, e.g.
by choosing `I_0` extremal, or by rerunning the argument with `D°_I`, `U°_I`.

**Follow-up (John):** append Theorem A, the conjecture and the 3-D example to
`main.tex`, in a new section. **Claude:** Added `\section{Bounded Splittings and
Higher Dimensions}` at the end. It contains `def:bounded-splitting`,
`thm:bounded-splitting-three` (Theorem A, with proof), a remark showing that
`thm:2d-zig-zag` is its 2-D case (the remark uses `q_0` for `i = 0`, which avoids the
gap noted above), `conj:bounded-splitting` with the computational evidence,
`ex:no-strict-zig-zag` (`[2]×[3]×[3]`), and the `[3]^3` non-principal example. I
deleted John's answered `% Claude` comment (Rule 3). Compiles cleanly (10 pages).

### 2026-11-12: John's test case for `conj:bounded-splitting`

**Request (comment at end of `main.tex`):** test the conjecture on
`Δ = {113,114,122,123,124,131,132,133,134,141,142,143,213,222,223,231,232}`
in `[2]×[4]×[4]`.

**Claude** (`code/test_johns_example.py`). `Δ` is a connected interval with minimal
elements `113, 122, 131` and maximal elements `134, 143, 223, 232`. It has 550
decreasing subsets, and exactly **3** of them are bounded splittings. So the
conjecture survives, but only just. The simplest is principal:
`S = Δ \ U(122) = {113,114,131,141,213,231}`. Its components are
`{113,114,213}` (least element `113`) and `{131,141,231}` (least element `131`).
The complement `U(122) ∩ Δ` has least element `122`. Every component is bounded
*below*. The other two splittings add `122`, or `122` and `222`, to `S`. John's
strict version fails here too. A strict cut would be a bounded splitting, but all 3
splittings have the component `{113,114,213}` of `S`, which has no upper bound.

**Follow-up (John):** summarize at the end of the document and delete the comment. **Claude:** Done. Appended `ex:barely-splittable` and removed the comment. Compiles cleanly.

### 2026-11-12: Systematic search for larger variants — `conj:bounded-splitting` is FALSE

**Request:** search systematically for larger variants of `ex:barely-splittable`.

**Method** (`code/splitsearch.py`, `code/smallest.py`): every connected interval of
a grid, enumerated as components of `A \ B` for downsets `B ⊆ A`, counting its
bounded splittings. Counterexamples were re-verified by brute force over all
subsets (`code/verify_counterexample.py`), independently of the search code.

**Results.**
- `[2]×[3]×[3]`: none (as before). `[2]×[3]×[4]`: 2 counterexamples among 15,012
  intervals (16 points each). `[2]×[4]×[4]`: many among 150,652 intervals (smallest
  16 points). `[3]^3`: 64 among 48,529 (smallest 15 points).
- Example: `{112,113,122,123,131,132,133,141,142,143,212,213,221,222,231,232}` in
  `[2]×[4]×[4]`, a connected interval with minima `112,131,221` and maxima
  `143,213,232`. All 314 decreasing subsets fail.
- Smallest found as an abstract poset (greedy deletion of points):
  `Q = {112,113,131,132,141,143,212,213,221,222,231,232}` ⊆ `[2]×[4]×[4]`, 12 points.
  It is connected; all 126 decreasing subsets fail. Hasse diagram: 112<113,132,212;
  113<143,213; 131<132,141,231; 132<143,232; 141<143; 212<213,222; 221<222,231;
  222<232; 231<232.
- **Correction:** my earlier claim that 3,000 sampled intervals of `[3]^3` all had
  bounded splittings was true, but the sample missed all 64 bad intervals. The
  evidence paragraph after `conj:bounded-splitting` in `main.tex` is therefore
  misleading.

**Consequences.**
- Theorem A (`thm:bounded-splitting-three`) is still true, but its hypothesis can
  fail in 3-D, so it doesn't give `thm:2d-zig-zag` in higher dimensions in general.
- The *conclusion* of `thm:2d-zig-zag` and `conj:three` are **not** refuted. Treating
  each counterexample (16-, 15- and 12-point) as a poset in its own right, an exact
  SAT search finds no collection needing ≥ 4 cuts with `D_I`, `U_I` free, and no
  good collection needing ≥ 4 cuts.
- In each counterexample the family of all unbounded connected intervals needs
  exactly 2 cuts. Equivalently, there is a *bounded 2-splitting*, a chain
  `L_1 ⊆ L_2` with every component of every layer bounded. That gives the 4-cut
  analogue of Theorem A.

**Follow-up (John):** approved the changes to existing text, and asked for `Δ` and
`Q` to be described at the end. **Claude:** Done.
- `conj:bounded-splitting` is now marked "[false, see Section …]". The paragraph
  after it now says the conjecture fails. The misleading sampled-grid evidence is
  replaced by the exhaustive cases plus a note that random sampling missed all 64
  bad intervals of `[3]^3`. `ex:barely-splittable` now says "has a bounded
  splitting" instead of "satisfies the conjecture".
- New final section `sec:counterexamples` contains the search table,
  `ex:no-bounded-splitting` (`Δ`, 16 points), `ex:Q` (12 points, with covering
  relations), the SAT results showing the zig-zag conclusion and `conj:three` still
  hold on these posets, and the 4-cut version via a bounded 2-splitting.
Compiles cleanly (11 pages).
