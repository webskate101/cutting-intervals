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
- **Chains (Example 3):** in `1 < 2 < ... < n+2`, the `n+1` covering pairs
  `{j, j+1}` are `n`-uncuttable, because each initial segment cuts only one of
  them. The same holds for any `n+1` intervals in a chain that meet at most in
  shared endpoints.
- **Antichains (Example 4):** on an `m`-element antichain, all pairs are
  `n`-cuttable iff `m ≤ 2^n`. The argument encodes each point by its 0/1 membership
  in `L_1, ..., L_n` (a binary encoding with pigeonhole). This shows a collection can
  be `n`-uncuttable even though every two of its members are `n`-cuttable.

**Possible questions to pursue:**
1. *Chains:* I believe a collection in a chain is `n`-uncuttable iff it contains
   `n+1` intervals as in Example 3. Each interval `I` gives the half-open range
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
