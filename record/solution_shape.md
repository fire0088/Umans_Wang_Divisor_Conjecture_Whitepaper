# What a Umans-Wang solution would look like (at fixed alpha, beta < 1/2)

*A specification of the target — necessary conditions, each checkable by
definition. Independent of which way the answer goes. Quantitative claims
verified numerically in `solution_requirements.py`.*

## The object
For each large n, a set S of integers with:
- **size** |S| = K ≈ n^{(1−α)/2},
- **magnitude** all elements in [0, e^{n^α}],
- **covering** every integer in (n/2, n] divides some difference s_i − s_j.
(Covering the interval reduces to covering the primes P(n) = {p prime : n/2 < p ≤ n}.)

## The four requirements

**[A] On the proven boundary (no slack).** We proved 2β+α ≥ 1 (discriminant/
primorial magnitude bound; see `covering_lower_bound.pdf`). A solution must be
tight: **2β+α = 1**, β = (1−α)/2. log Q = θ(n)−θ(n/2) ~ n/2 (verified), and the
budget e^{n^α} leaves exactly enough room and no more.

**[B] Heavy bundling (forced by counting).** ~K²/2 differences must cover ~n/ln n
primes, so each difference must be divisible by ~n^α/ln n **distinct** primes of
(n/2,n] simultaneously (verified: needed ≈ budget-allowed at every α,n). Each
difference is thus a product of ~n^α/ln n primes each > n/2, of size ~e^{n^α} —
saturating the budget. Near-perfect bundling with negligible waste is required.

**[C] From one small set (realizability).** Those ~K²/2 bundled differences are
the pairwise differences of a single K-set. So S−S must consist almost entirely
of these "n^α/ln n-almost-primes with large prime factors." A very rigid
constraint on S.

**[D] Distinct and spread.** Each collision s_i ≡ s_j (mod p) is between distinct
elements, so |s_i − s_j| ≥ p > n/2. No collapse to a point; elements spread across
[0, e^{n^α}].

## The essential tension (why it is hard)
[B] wants the differences **multiplicatively rich** (products of many large
primes). [C] wants them all **differences of one small set** (additively
structured). Erdős–Szemerédi sum-product says a set cannot be both additively and
multiplicatively structured. A solution must thread exactly this needle. This is
the precise knife-edge — and the reason the problem is genuinely hard, not merely
unsolved.

## Shape of a proof, either direction
- **UW true:** exhibit or prove existence (probabilistic / Rödl-nibble /
  semi-random construction) of a set S meeting [A]–[D] simultaneously — the
  near-perfectly-bundled, distinct, budget-saturating difference set.
- **UW false (barrier α+β≥1):** prove the sum-product tension is fatal — no set
  has [C] additive structure with its difference set having [B] multiplicative
  richness at the required density — forcing β strictly above (1−α)/2.

## What is NOT the way (documented dead ends from this project)
- Discriminant magnitude alone → only gives 2β+α≥1, provably cannot reach the
  barrier (tight as a magnitude bound).
- Small-n / polynomial-magnitude computation → wrong regime: bundling (the crux)
  only switches on at large n with super-polynomial magnitude; small-n optimal
  sets cover ~1 prime/difference (√n regime), not the bundled floor.
- Vertex-log "each element needs magnitude e^{vertexlog}" → false; defeated by
  residue-sharing.
- Requiring S−S to equal the targets (turnpike/exact reconstruction) → stricter
  than the real (divisibility) condition; not the actual problem.

*Companion to `additive_realization_program.md` (full program record) and
`covering_lower_bound.pdf` (the one proven theorem, 2β+α≥1).*
