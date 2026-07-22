# A conditional construction theorem for Umans-Wang at fixed alpha

*Our adaptation of the Bloom-Sawin-Schildkraut-Zhelezov (BSSZ, arXiv:2605.28781)
unit-lattice construction to the divisibility-covering problem. This is a
CONDITIONAL theorem: the hypothesis is isolated and unproven (it is the same
descent-to-Z obstacle open in BSSZ). Magnitudes verified numerically in
`our_theorem_attempt.py` and `required_shortness.py`.*

## Setup
Fix alpha < 1/2. Target: a set S of K = n^{(1-alpha)/2 + o(1)} integers, all
<= e^{n^alpha}, whose difference set covers every prime in P(n) = (n/2, n] by
divisibility. By the proven bound 2beta+alpha >= 1, this K is the smallest
possible, so success proves UW true (barrier false) at this alpha.

## The construction (lattice-CRT)
1. **Packing (proven).** Assign the primes of P(n) to the K(K-1)/2 pairs {i,j}
   so each pair's assigned-prime-product m_ij satisfies log m_ij <= n^alpha.
   Feasible since bin capacity n^alpha >> item size log n (greedy bin-packing).
2. **Congruence lattice.** Seek s_0,...,s_{K-1} with s_i ≡ s_j (mod m_ij) for each
   assigned pair. These cut out a lattice L in Z^K of covolume ≈ Q = prod_{p in P} p,
   with log Q ≈ n/2.
3. **Shortness requirement.** We need K distinct coordinates all <= e^{n^alpha}.
   Minkowski's *average* gives coordinates ≈ Q^{1/K} = e^{n/(2K)} = e^{n^{(1+alpha)/2}/2}.
   Since (1+alpha)/2 > alpha for alpha < 1, the naive/average solution EXCEEDS the
   budget by a factor growing polynomially in n (verified: 9x, 58x, 316x at
   alpha=0.3, n=1e4..1e8). **Generic lattice geometry is NOT enough** -- this is
   the correct, quantified reason the naive construction (and the earlier
   vertex-log heuristic) fails.

## The BSSZ ingredient (why a number field)
BSSZ build sets in totally real number fields K of degree d with root-discriminant
bounded (Delta_K <= C^d, via Martinet class-field towers). In such a field the
UNIT LATTICE has covolume = regulator <= C^d over dimension d-1, hence
O(1)-size-per-dimension basis vectors -- vectors far SHORTER than the Minkowski
average for a lattice of that covolume. This is exactly the "shortness beyond
average" our step 3 requires. The required dimension d ~ K ~ n^{(1-alpha)/2} is
AVAILABLE (Martinet towers give bounded root-disc for d -> infinity). So the
MAGNITUDES ALL FIT: dimension available, covolume/shortness type matches.

## The conditional theorem
**Theorem (conditional).** Suppose the pair-congruence system of step 2 can be
embedded into the unit lattice of a totally real number field of degree d ~ K with
root-discriminant O(1)^d, in such a way that a simultaneous solution inherits the
unit-lattice O(1)-per-dimension shortness (equivalently, yields K distinct integers
<= e^{n^alpha}). Then UW holds at exponent alpha: covering pairs exist with
|S|,|T| = n^{(1-alpha)/2+o(1)} and elements <= e^{n^alpha}. Hence the barrier
alpha+beta >= 1 is false and 2beta+alpha = 1 is tight.

## The isolated open hypothesis (the honest crux)
The hypothesis is a LATTICE-EMBEDDING / DESCENT question:
> Can a congruence system over rational primes (s_i ≡ s_j mod m_ij) be realized
> by short vectors of a bounded-root-discriminant unit lattice, so the solution
> descends to SMALL integers?
This is NOT a magnitude gap (magnitudes fit). It is a STRUCTURAL compatibility:
unit-lattice shortness is about smallness in all archimedean embeddings, while our
constraints are about rational-prime divisibility of integer differences. Bridging
these is exactly the descent-to-Z step that BSSZ leave OPEN (they prove the R,
p-adic, and finite-field cases; Z is not established). Our theorem shows UW at
fixed alpha REDUCES to this specific embedding question.

## Status (honest)
- Magnitudes/dimensions: verified to fit (not a hand-wave).
- Packing lemma: provable.
- The embedding hypothesis: OPEN -- and it is the same obstacle open in the source
  paper, so we should not expect to close it here. What we HAVE done is reduce UW
  (fixed alpha) to a precise, named lattice-descent question tied to the current
  research frontier, and identify exactly why generic methods fail (Minkowski
  average is a polynomial factor short; only special-field shortness can close it).

*Companion to `covering_lower_bound.pdf` (proven 2beta+alpha>=1), `solution_shape.md`
(what a solution must satisfy), and `additive_realization_program.md` (full record).*
