# Umans–Wang $(\alpha,\beta)$-divisor conjecture — investigation package

Eric Schultz (independent researcher, ORCID 0009-0006-6283-1696), July 2026.

This package collects an extended investigation of the Umans–Wang
$(\alpha,\beta)$-divisor conjecture (arXiv:2511.10851), whose positive resolution
at $\alpha,\beta<1/2$ would break the exponent-$3/2$ barrier for polynomial
factorization.

## Bottom line (honest status)

- **Proven, unconditional:** the magnitude lower bound **$2\beta+\alpha \ge 1$**.
  This is consistent with the conjecture (it does not decide it) and reproduces the
  paper's own bound by an independent (discriminant) route.
- **Main contribution:** a **reduction of the conjecture at fixed $\alpha$ to a
  lattice-clustering statement that is equivalent to the conjecture**, tied to the
  2026 Bloom–Sawin–Schildkraut–Zhelezov number-field construction. All magnitudes
  and dimensions are shown compatible; a single descent-to-$\mathbb{Z}$ embedding
  question remains — the same one open in that paper.
- **The conjecture itself is OPEN in both directions.** Evidence gathered leans
  *mildly* toward it being true / not blocked by anything classical, but nothing
  here proves or refutes it.

## Contents

### `papers/`
- **`main_paper.pdf`** — the main result: the lower bound and the
  lattice-clustering reduction (what a specialist needs to continue). **Start here.**
- **`secondary_paper.pdf`** — the negative results: what was tried, what failed,
  and *why*. The catalogue of dead ends (a practical time-saver for any future
  attack).
- `covering_lower_bound.pdf` — earlier standalone writeup of the proven bound.

### `record/`
- **`additive_realization_program.md`** — the authoritative running record of the
  entire investigation, including every claim made, audited, and (where necessary)
  retracted. The full honest trail.
- `solution_shape.md` — specification of what any solution must satisfy.
- `our_construction_theorem.md` — the conditional construction theorem
  (superseded in part by the main paper's equivalence result — see note there).
- `MASTER_RECORD.md` — older index / trust table.

### `code/`
Verified, load-bearing scripts. Highlights:
- `final_verify.py`, `verify_theorem_proof.py` — verify the proven theorem's
  ingredients and proof chain.
- `uw_floor_check.py` (+README) — honest feasibility checker (reports
  Optimal/Infeasible/Timeout explicitly; brute-force cross-check). Use `--selftest`.
- `fast_minK.py`, `exact_minK_sequence.py` — exact minimum-$K$ computations.
- `descent_crux.py`, `descent_crux_check.py`, `descent_audit2.py` — the
  lattice-clustering / equivalence analysis.
- `squares_test.py`, `cubes_factorials_test.py`, `fractal_test.py`,
  `golden_squares_test.py`, `asymmetric_test.py` — construction-family bundling
  tests.
- `future_attempt4.py`, `future_attempt5.py` — the (audited) asymmetric $S-T$
  bipartite analysis, with the degeneracy filter.

Scripts need Python 3 with `sympy`; some use `pulp` (CBC) or optionally Gurobi.

### `superseded/` — ⚠️ RETRACTED, DO NOT CITE
These PDFs are from **early, incorrect** phases of the work and are kept only for
provenance. In particular any file named `REFUTED_...` or `..._v2` asserting a
*barrier* / refutation is **wrong**: every internal "barrier holds" conclusion in
this project was later found to be an artifact (a generic bound mistaken for a lower
bound, a degenerate solution, or a solver timeout). See `secondary_paper.pdf` §2 for
the five documented forms of that error. The correct status is in `papers/`.

## The one thing to remember

Every elementary "barrier" argument against this conjecture that we produced turned
out to be an artifact on exact checking. Treat any counting- or forcing-based
"barrier" claim (including in the superseded files) as presumed-false until verified
exactly. The genuine obstruction is the lattice-clustering question, which is
equivalent to the conjecture itself.
