This white paper is my AI assisted analysis of https://arxiv.org/abs/2511.10851 .

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
