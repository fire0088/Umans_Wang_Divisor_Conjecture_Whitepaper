# MASTER RECORD — Umans–Wang (α,β)-Divisor Conjecture Investigation

**Authors:** Eric Schultz and Claude (Anthropic)
**Span:** July 2–9, 2026 (six sessions)
**Subject:** arXiv:2511.10851
**This file is the authoritative index.** Read it before trusting any other
file in this folder. Every artifact is tagged by trust level below.

---

## The one-paragraph truth

We did **not** prove or refute the Umans–Wang conjecture; it remains open.
Along the way we produced one polished "proof" that was **computationally
refuted** (do not trust it), three **genuinely verified** lattice theorems
(trustworthy), an honest empirical survey showing four construction families
all hit the same α+β=1 barrier, one rigorous partial lower bound (2β+α ≥ 1),
and a diagnosed structural obstruction (L2/second-moment methods cannot prove
the barrier). The most valuable outputs are the negative results and the
failure analysis, not any claimed solution.

---

## Code audit (July 2026)

All load-bearing scripts were audited for errors. Results:
- **Counting bound (2β+α≥1):** SOUND. log₂M is a valid bound on ω(d); verified.
- **The refutation (coverage falls with n):** SOUND. The coverage test exactly
  matches the problem definition (i covered iff some |s−t| divisible by i);
  reproduces. This is the archive's most important result and it holds.
- **Large-sieve obstruction:** SOUND. The exp(n^α)-vs-polynomial gap is
  insensitive to constants; conclusion robust.
- **Boolean-rank note:** HAD AN ERROR, now CORRECTED. The claim "rank(B)=|D|
  exactly" was a greedy artifact, not a fact about covering (a valid covering
  can have rank as low as 1). The conclusion — rank fails as a lower-bound
  method — is unchanged and in fact strengthened. See the corrected addendum
  in `lower_bound_strategy_sketch.md` and `audit_rank_claim.py`.

- **Star-chain coverage (survey):** HAD AN ERROR, now CORRECTED. The
  star-chain construction covers every *prime* p≤n but NOT every integer
  (it misses prime powers and composites) — verified by direct check. The
  survey originally listed it as a full covering pair. Corrected: it is a
  *prime-covering* pair, a weaker object, now flagged in `covering_survey.pdf`.
  The barrier conclusion is unaffected (full covering is harder, so a genuine
  full-covering star-chain sits at α+β ≥ its prime-covering value). NOTE: the
  companion `lattice_covering_theorems.pdf` is CORRECT and needs no fix — it
  explicitly defines its covering condition as "every prime p≤n" (§1), so its
  theorems are about prime-covering by definition and do not overclaim.
- **Fourier, hybrid, zone/CRT families:** SOUND. All check coverage of every
  i≤n (verified: `audit_survey_families.py`). The zone/CRT refutation
  (checks all i) is unaffected.

Audit scripts: `audit_rank_claim; `audit_recent.py`.
- **Parity structure test (Addm 13):** HAD A BUG, now CORRECTED. Structured S,T
  (norm forms) were built with tiny elements vs the random control, making the
  "structure kills bundling / clean dichotomy" conclusion a magnitude artifact.
  At equal magnitude, norm/subgroup/random bundle about equally. The parity
  route is INCONCLUSIVE, not blocked. Corrected in the strategy sketch Addm 13.py`, `audit_others.py`, `audit_all.py`,
`audit_lattice.py`, `audit_starchain_full.py`, `audit_survey_families.py`.

## Late-session additions (post-dating earlier sections)

### Latest thread — the barrier localized to ONE parity-free question (newest)
Full detail in `additive_realization_program.md` and `F_measurement_findings.md`.
Chain of results (each an attempt whose failure sharpened the problem):
- **F (set-complexity) is ~counting-tight**, ≈2× the floor. That 2× is the
  **parity factor** (measured F/floor→2.0 at α=0.4; dual weight 85% on odd-ω
  numbers) — but it is a CONSTANT, so parity does NOT affect the exponent.
- **Tao's LP parity-injection** tried: works to recover the constant, useless for
  the exponent. ⇒ the barrier's EXPONENT has a NON-parity origin.
- **Prime-embedding is cheap** (exact ILP solver: K~√m), so realizing the hard
  primes as differences is NOT the wall. (Corrected a greedy-realizer bug that
  had said otherwise.)
- **Multi-scale collapse:** covering (n/2,n] alone costs the same as covering
  [1,n] (F_top=F_full). And it is ARITHMETICALLY IMPOSSIBLE for set-covering cost
  to reach the barrier (needs F_top exponent ≥2(1−α)>1, but F_top≤n/2 ⇒ exp ≤1).
- **Double-forced conclusion:** the barrier (if real) is NOT a set statement — it
  lives entirely in the **set→pair realization gap**, reached independently from
  the additive side (overdetermination) and the multi-scale side (arithmetic
  impossibility), and it is parity-free.

**THE remaining crux (one clean additive-combinatorics question):**
> For a divisibility-covering set D of (n/2,n] with |D|~n^{1−α}, realized as
> D ⊆ S−T with |S|=|T|=K: does the overdetermination force K ≥ n^{1/2−o(1)}
> (⇒ β≥1/2 ⇒ barrier), i.e. cost a full extra √ beyond the counting √|D|?

Validated reusable tools: `exact_embedding_solver.py` (difference-set embedding),
`joint_constraint_solver.py` (exact covering-pair min-K).



- **NEW THEOREM (proven):** the Smoothness Covering Decomposition — see
  `smoothness_decomposition.pdf`. The one genuinely new theorem of the later
  sessions; exhaustively verified n=2..3000.
- **Realizability finding:** the theorem's covering SET is provably NOT
  realizable as a balanced difference set (overdetermination: |D| constraints
  vs 2K unknowns). Balanced covering pairs empirically need K ~ √n·log n
  (consistent with β=1/2+o(1), unproven). Sets and pairs are different objects.
- **Addendum 14 (strategy sketch):** bundling and covering are in measured
  tension — high-bundling difference sets cannot cover; the parity foothold is
  illusory at the construction level.
- **Addendum 15:** a serious attempt to CONSTRUCT below the barrier failed at a
  concrete α=½ wall: the √n-smoothness needed for cheap covering itself costs
  α=½; spending less reopens the medium-prime gap. Strongest constructive
  evidence for the barrier.
- **Document repair:** the strategy sketch had accumulated triplicated addenda
  blocks (53 headers for 14 addenda) — cleaned to one copy each; consolidated
  executive summary added at top.

## Trust levels — read this table first

| Artifact | Trust | What it is |
|----------|-------|------------|
| `lattice_covering_theorems.pdf` | ✅ **TRUSTWORTHY** | 3 theorems, every core enumeration-verified |
| `covering_survey.pdf` | ✅ **TRUSTWORTHY** | Empirical survey of 4 families; honest negative result |
| `FAILURES_LOG.md` | ✅ **TRUSTWORTHY** | What failed and why, incl. our process failures |
| `lower_bound_strategy_sketch.md` | ✅ **TRUSTWORTHY** | Lower-bound strategy; 2β+α≥1 proven; L2 obstruction diagnosed |
| `barrier_conjecture.pdf` / `.tex` | ✅ **TRUSTWORTHY** | Proven bounds + refined *Barrier Conjecture* (labeled conjecture); UW stays open |
| `smoothness_decomposition.pdf` / `.tex` | ✅ **TRUSTWORTHY** | NEW THEOREM (proven, exhaustively verified): smoothness covering decomposition. Honestly scoped: covering SET only; explicitly disclaims the pair question |
| `NEW_THEOREM_smoothness_decomposition.md` | ✅ **TRUSTWORTHY** | Same theorem, notes form, with corrected realizability discussion |
| `bundling_core_data.json` | ✅ **TRUSTWORTHY** | Logged core data: dedicated prime powers track π(n) |
| `verify_chain_theorems.py`, `verify_nondegeneracy.py` | ✅ **TRUSTWORTHY** | Enumeration checks for the lattice theorems |
| The `fourier_*`, `hybrid_*`, `fast_lattice`, `lb_*`, `d1_*` scripts | ✅ **TRUSTWORTHY** | Reproduce the survey and lower-bound findings |
| `umans_wang_divisor_conjecture_v2.pdf` / `.tex` | ❌ **REFUTED** | The claimed "unconditional proof" — FALSE, see below |
| `Umans_Wang_..._Whitepaper_v3.docx` (+ v1,v2) | ❌ **REFUTED** | Same claimed proof, Word form |
| `covering_pair_final.py`, `dedicated_construction.py`, `lemma_x_proof.py`, `divisibility_covering_poc.py` | ❌ **REFUTED** | Implement the refuted zone/CRT construction |
| `CORRECTION_NOTICE.md` | ✅ **TRUSTWORTHY** | Documents the refutation in detail |
| `full_coverage_test.py`, `confirm_za_zb_gap.py` | ✅ **TRUSTWORTHY** | The scripts that DID the refuting |

If you only read three things: this file, `lattice_covering_theorems.pdf`,
and `FAILURES_LOG.md`.

---

## What actually happened, in order

### 1. A claimed proof was built (sessions 1–5) and refuted (session 6)
The zone/CRT construction partitioned [1,n] by prime size, covered each zone
with a tailored mechanism, and — on paper — achieved α=1/3+ε, β→1/3, below
the barrier. It grew across five sessions into a polished "unconditional
proof." In session 6 we ran the one experiment that had never been run to
completion: **measure actual coverage of [1,n] by the full construction.**
Result: coverage *falls* as n grows (77%→49%→33%→27%→21% for n=1000→40000),
the opposite of what a correct proof predicts. **Root cause:** composites
m·q with m a small prime and q a middle prime (e.g. 327=3×109) are covered
by no mechanism — a structural gap, not a tuning issue. `full_coverage_test.py`
and `confirm_za_zb_gap.py` demonstrate it. See `CORRECTION_NOTICE.md`.

### 2. Three lattice theorems were verified and written up (trustworthy)
Independent of the refuted work. `lattice_covering_theorems.pdf`:
- **Theorem 1 (hypercube optimality):** α+β = 1 + (k ln2 − ln(k+1))/ln n;
  equals 1 exactly at k∈{0,1}, strictly above for k≥2.
- **Theorem 2 (star-chain achievability):** reaches α+β=1+o(1) for every
  fixed β∈(0,1), using k+1 terms not 2^k. (Pointwise in β; rate caveat.)
- **Theorem 3 (chain global optimality):** pure chain is the unique optimum,
  pure hypercube the unique worst, in the hybrid family.
Every combinatorial core (f(k)≥0; 2^d−1≥d; monotonicity of (2^d−1)/d; the
non-degeneracy union-bound; the adversarial example) verified by direct
enumeration BEFORE writing. These are honest statements about *proven upper
bounds*, claiming nothing about achieved α beyond Minkowski.

### 3. Four construction families surveyed — all hit α+β=1 (trustworthy)
`covering_survey.pdf`. Star-chain lattice (covers, α+β≈1.01–1.04, on the
line from above); Fourier-balanced (covers, β→½ birthday bound, no gain over
random); discrete-log hybrid (covers, slides along α+β≈1); zone/CRT
(parameters say <1, but fails to cover). **Every family that provably covers
lands on or above α+β=1; the only apparent exception fails to cover.**

### 4. Lower-bound strategy attempted (trustworthy, partial)
`lower_bound_strategy_sketch.md`. Rigorously provable: **2β+α ≥ 1**
(counting). This is *weaker* than the observed α+β≥1. Every purely
multiplicative strengthening (incidence, divisor, factor-packing) stalls at
the same 2β+α≥1 ceiling. A tempting β≥½ argument was found and shown
**false** (multiples of p share divisor structure; one composite difference
covers many). The one live direction — exploiting that differences form a
*difference set* — was attempted via the large sieve (D1) and **failed
structurally**: covering is an L∞/positivity condition, the sieve is L2, and
squaring inflates the bound by exp(n^α). This is the **third** independent
sighting of "second-moment methods are the wrong tool" (after the dispersion
method and Fourier-balancing). Untested candidates that respect positivity:
Boolean-rank of the covering matrix; a new entropy-compression encoding.

---

## The two lessons worth carrying forward

**Mathematical:** α+β=1 behaves as a genuine barrier for all methods tried.
The provable partial result is 2β+α≥1; the gap to α+β≥1 is real and,
diagnostically, cannot be closed by any second-moment method. A proof (if one
exists) needs an L∞/positivity-respecting technique.

**Process (from `FAILURES_LOG.md`, Part II):** the refuted proof did not come
from bad mathematics — it came from *gap-filling instead of gap-sitting*.
An early peer review correctly flagged the gaps; instead of leaving them
open, each was "strengthened" with plausible machinery until "conditional"
had quietly become "unconditional." Proxies (the i=3 trick) were relabeled as
the real thing. A fitted constant was presented as derived. And the decisive
coverage check — a 20-line script — was not run to completion for five
sessions. The correction: **when a gap is found, state it and stop; don't
generate machinery that makes it look closed.** Every claim should be a
falsifiable inequality checked against the real constructions, which are the
test oracle.

---

## If you want to continue

The honest open problems, in rough order of tractability:
1. **Prove 2β+α ≥ 1 is not tight** — even a small improvement (e.g.
   (3/2)β+α ≥ 1) would be new. Needs an L∞ method; the sketch's Boolean-rank
   idea is the first thing to try, cold and skeptically.
2. **Confirm or refute** whether the star-chain's α+β dips below 1 as n→∞
   (currently unconfirmed at reachable n; requires SVP at scales beyond our
   compute).
3. **The conjecture itself** remains open and hard; nothing here suggests an
   easy path.

**Loose end (still open, honestly flagged):** whether the star-chain's
*achieved* α (measured ~0.6 via LLL at small n) converges to the *proven*
Minkowski bound 1−β requires exact-SVP at scales beyond our compute
(`exact_svp_test.py`, `exact_svp_test2.py` ran small cases; small-k results
were consistent with the bound but the asymptotic regime is unreachable).
This is listed as open problem 2 and remains genuinely unresolved.

Do not resurrect the zone/CRT construction without first re-reading
`CORRECTION_NOTICE.md` and re-running `full_coverage_test.py`.
