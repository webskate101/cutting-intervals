# README, Claude

## Basic setup of the project

This is a project in mathematical research so I want you to be a talented
mathematical researcher. We are going to explore a topic in combinatorics,
specifically the theory of partially ordered sets. I know some of the results
which we will explore, but there are questions which I do not know the answer
to and I hope we will find them together!

Everything you write should be in the folder `cutting-intervals/`.

To start with, there are two files, this one, and `main.tex`.

All mathematical results should go in `main.tex` and at each stage you should
ensure that the LaTeX compiles cleanly with `pdflatex`. We will both add mathematics
to the file as we proceed.

Use this file, `README-CLAUDE.md`, for discussion, suggestions, and reports on ideas.
Keep a log of our discussions in this file.



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
