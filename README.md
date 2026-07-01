Exploring Constructive Approaches to the Umans–Wang (α,β)-Divisor Conjecture

This repository accompanies the paper:


Exploring Constructive Approaches to the Umans–Wang (α,β)-Divisor Conjecture:
A Survey of Construction Strategies, Empirical Obstructions, and Lattice-Based
Optimality Results 

https://arxiv.org/abs/2511.10851 

Prepared in collaboration with Claude (Anthropic), 2026.


What this is

Umans and Wang (arXiv:2511.10851, 2025) introduced the (α,β)-Divisor Conjecture:
whether there exist sets S, T of integers, each of size at most n^β and magnitude
at most exp(n^α), such that every integer i ≤ n divides some difference s−t. A
positive resolution with α, β < 1/2 would yield the first improvement in over a
decade to the best known algorithms for polynomial factorisation and deterministic
integer factorisation.

This project documents a systematic exploration of construction strategies for that
conjecture, producing three proved theorems about the structure of lattice-based
constructions within this family, along with a body of numerical experiments and
seven independent lines of evidence that all converge on the same barrier α+β ≈ 1.

The conjecture itself remains open.


Status and provenance

This work was produced through an extended conversation between a human collaborator
and Claude (an AI model by Anthropic). It has not been peer-reviewed and has
not been checked by an independent domain expert in number theory or
computational complexity. The three theorems are carefully checked but not
independently verified.

Specific limitations are disclosed in the paper's "Provenance and Status" section
and in Section 11.1 ("A calibrated self-assessment"). In particular:


The non-degeneracy lemma (Lemma 8.1) is fully proved by an elementary pigeonhole
argument but rests on one cited classical fact (bounded basis from reduction
theory) rather than a fully self-contained derivation.
The numerical results in Section 9 characterise the performance of our specific
lattice-reduction algorithm relative to the proven asymptotic target — they should
not be read as independent evidence of convergence to exponent 3/2.
The literature search for prior work was targeted, not exhaustive.



The three theorems

Theorem 1 (Optimality of hypercube constructions): For the hypercube lattice
construction with k binary dimensions, α+β = 1 + [k·ln2 − ln(k+1)]/ln(n) + o(1),
minimised at k ∈ {0,1} where it equals 1 exactly, and strictly greater than 1 for
all k ≥ 2.

Theorem 2 (Full-line achievability): For the star/chain construction with k =
⌈n^β⌉ − 1 generators, α+β = 1 + o(1) for every fixed β ∈ (0,1) as n → ∞ —
continuously along the entire trivial line, not merely at isolated points.

Theorem 3 (Global optimality of the chain structure): For the two-parameter
family of m blocks of d generators each (k = md total), g(m,d) := ln(1+m(2^d−1))
− ln(1+md) ≥ 0 with equality iff d=1. The star/chain (d=1) is the unique global
optimum; the hypercube (m=1, d=k) is the unique global worst point of this family
for every fixed k.

The core inequality underlying Theorem 3 is simply 2^d − 1 ≥ d for all
positive integers d, with equality only at d=1.


Repository structure under scripts:

Core lattice construction (most important):

fast_lattice.py — the final, production-quality implementation: mpmath-based LLL with dynamic precision, BKZ-style block enumeration, and exact integer verification. This is what produced the k=19 and k=25 results in Section 9.
star_chain_test.py — the original exact-fraction LLL implementation, used for Theorems 1–3 and the initial scaling study. Also contains the block_enumerate function.

Lemma 6.2 / continued-fraction experiments:

lemma62_test.py — the primary Lemma 6.2 test: CRT idempotents, continued-fraction candidates, ground-truth verification.
lemma62_scaling.py — scaling study across n=10 to n=150, including the zero-term bug fix.
c_equals_1_test.py — direct test of the paper's c=1 edge case against the necessary lower bound.

Lattice geometry experiments:

lattice_kdim.py — the key experiment showing α+β worsens for k≥2 in the hypercube family (the core observation behind Theorem 1).
lattice_scaling.py — scaling study showing α is independent of grid cell count (leading to the Minkowski-rank insight).
lattice_2d_optimization.py — LLL applied to the 2D generalized AP, producing the first verified sub-√U results.
joint_2d_optimization.py — earlier brute-force (b₁,b₂) sweep; superseded by the lattice approach but kept for reference.

Earlier construction experiments (in order of the investigation):

covering_sets.py — the very first experiment: naive bucketing and LCM constructions.
ap_divisor_test.py — single arithmetic progression tests (Proposition 3.4 angle).
greedy_cover_search.py — greedy set-cover over smooth-number candidates.
order_distribution.py — multiplicative order distribution for the discrete-log sieve.
hybrid_test.py — the discrete-log + continued-fraction hybrid (found to be worse).
recursive_doubling.py — Lemma 6.1 merge / recursive doubling attempt.
generalized_ap_test.py — two-AP merge via Lemma 6.1 (found to be worse than single AP).
alteration_plus_lemma62.py — alteration method stacked on Lemma 6.2 (found to have nothing to patch).

White paper source:

build_v2.js — the Node.js document generator for the white paper, using the docx library.
