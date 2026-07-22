# The Set→Pair Realization Gap: An Additive-Combinatorics Program

**Authors:** Eric Schultz and Claude (Anthropic) · July 2026
**Status:** Active problem. This is where the α+β=1 barrier has been localized.

## The reduction (established this session)

- **Set complexity is (tentatively) counting-tight:** F(n,n^α) = n^{1−α+o(1)}.
  No parity-free lower bound hides in the covering-SET problem.
- **Therefore the barrier, if real, lives entirely in the set→pair gap:**
  turning a covering set into a *balanced* difference set S−T, |S|=|T|=K.
- **Triangulated evidence the gap is a real wall (all consistent):**
  1. Overdetermination: realizing |D|~n^{1−α} prescribed values as s−t needs
     |D| constraints satisfied by 2K unknowns — infeasible for K≪|D|.
  2. Balanced-K scaling: empirically K_pair ~ √n·log n.
  3. Direct ratio: K_pair/K_set ≈ 2 and non-decreasing (n≤65).

## The precise open question (additive-combinatorics form)

> Let D ⊂ [1, e^A] be any set covering [1,n] by divisibility, realizable as
> D ⊆ S−T with |S|=|T|=K. As A=n^α with α<½, must K ≥ n^{½−o(1)}?

Equivalently: is there a covering set that is **simultaneously** near-minimal
(|D| ~ n^{1−α}) **and** difference-set-structured (D ⊆ S−T, K ~ √|D|)? If yes,
UW is true and the barrier falls. If provably no, the barrier holds for α<½.

## Why this is genuinely additive-combinatorics (not covering)

The covering/divisibility content is now discharged (set problem solved). What
remains is purely additive: which sets of integers arise as (subsets of)
difference sets S−T of small balanced sets? This is the domain of:
- **Freiman-type inverse theorems** (structure of sets with small sumset/
  difference set),
- **Plünnecke–Ruzsa** inequalities (difference-set growth),
- **additive energy** (a difference set S−T of two K-sets has energy
  constraints; a covering set has a prescribed multiplicative shape).

The tension to exploit: covering forces D to contain many *multiplicatively
structured* elements (prime powers, smooth×prime), while being a difference set
forces D to be *additively structured*. These two structures are, heuristically,
incompatible unless K is large. Making "incompatible" quantitative is the goal.

## Sub-questions / attack points (to be tried, honestly labeled)

- (A1) **Additive-energy lower bound.** Does a covering difference set force
  high additive energy E(S,T), which then forces K large? Testable + provable-
  in-principle.
- (A2) **Multiplicative-vs-additive incompatibility.** The covering set must hit
  every residue class structure (multiplicative); quantify how that conflicts
  with the Freiman structure of a small-doubling difference set.
- (A3) **Prescribed-difference realizability.** Given a target set of large
  primes {q_i}, minimum K with all q_i ∈ S−T. This is a clean, standalone
  additive question (a "difference basis / perfect difference family" problem)
  and connects to the classical B_h / Sidon-set literature.

## Honest caveats

All localization evidence is n≤200 (set) / n≤65 (pair) — a lean, not a proof.
The additive direction is harder than the covering direction and may itself be
parity-entangled once large primes enter. This program is the identified live
frontier, not a solved path.


---

## A3 progress (this session): realization cost depends on target structure

**Solid finding.** Realizing m PRESCRIBED differences as a balanced difference
set S−T costs K that depends sharply on the additive structure of the targets:
- AP-structured targets: K realizable well below m (e.g. m=25 → K≈13).
- Random-like targets: K ≈ m — essentially NO benefit from the K² differences
  a balanced pair offers (m=25 → K≈24). (`A3_prescribed_differences.py`,
  `A3_exact.py`.)

**Connection to UW.** The hard targets are the large primes, which are
additively UNSTRUCTURED (not in APs). So realizing them lands in the expensive
(K≈m) regime — direct evidence the set→pair realization is the wall, and WHY:
large-prime targets resist cheap additive realization.

**Honest gap (escape route untested).** UW lets the construction CHOOSE S,T
(and which multiple a_q·q of each large prime to use as its difference). So it
could try to arrange coverage so the required differences are additively
structured (cheap to realize). I attempted to test this escape but the test was
FLAWED: I made the target VALUES evenly spaced (AP-like), but that is not the
structure that makes a set cheaply realizable as differences (which needs
Sidon-type structure in S,T, a different and in fact opposite condition). The
flawed test showed K going UP (14 vs 7), which is uninformative about the real
escape. So: whether a clever arrangement lets the construction escape into the
cheap regime is GENUINELY UNTESTED. Not claiming the barrier holds here.

**Number-theoretic obstruction (heuristic, unproven).** Forcing {a_q·q : q large
prime} to be additively structured requires a_q ≈ (structured value)/q to be
integers simultaneously for many distinct large primes q — generically
impossible (a Diophantine obstruction). This SUGGESTS the escape fails, but it
is a heuristic, not a proof, and the correct notion of "cheaply realizable"
(Sidon, not AP) still needs to be tested against it.

**Next concrete step (correctly posed).** Test whether the construction can
choose, for each large prime q, a multiple a_q·q, such that the resulting set
{a_q·q} is a SIDON-realizable set (i.e. embeds in S−T with K~√m). The right
metric is Sidon/B_h structure of the chosen set, NOT even spacing. This is the
properly-posed version of the escape question and was NOT done correctly here.


---

## A3 escape test, correctly posed (this session): negative, with honest caveats

Tested whether the construction can escape the realization wall by CHOOSING, per
large prime q, a multiple a_q·q so that the chosen set {a_q·q} embeds cheaply
(K~√m) as a difference set. Correct metric this time: GAP/Sidon structure, not
even spacing. (`A3_escape_correct.py`.)

**Result: escape not found.**
- identity (a_q=1, targets = large primes): K/√m ≈ 1.75
- gap2 (force targets into a rank-2 generalized AP): K/√m ≈ 3.50 — WORSE.
Neither approaches K~√m; structuring attempts made realization harder, not
easier.

**Why (number-theoretic heuristic).** Forcing {a_q·q} into a low-additive-
complexity set (GAP/Sidon) requires a_q ≈ (structured value)/q to be integer-
compatible simultaneously across many distinct large primes q. This is a
Diophantine obstruction: distinct large primes cannot be jointly coerced into a
common additive lattice cheaply. This is the additive-combinatorics face of the
same "large primes resist bundling / structuring" phenomenon seen throughout.

**Honest caveats (do not overclaim).**
1. The realizer is a randomized greedy — a WEAK solver. Failure to find a small-K
   embedding is not proof none exists.
2. Only TWO target-choice strategies were tried. The space of arrangements is
   large; a cleverer one could in principle succeed.
3. All data n≤150, m≤16.
So this is EVIDENCE the escape fails, not a proof. The barrier is supported, not
established.

## Assessment of the additive program

The additive-realization program has, in one session:
- Confirmed the barrier is localized to the set→pair gap (triangulated 3 ways).
- Identified the mechanism: realization cost is governed by the additive
  structure of the target set; large primes are additively unstructured hence
  expensive; and attempts to structure them are Diophantine-obstructed.
- Found NO escape (two strategies), but with a weak solver — suggestive, not
  conclusive.

**The clean open problem, now in pure additive-combinatorics form:**
> Given m distinct large primes q_1,…,q_m ∈ (√n, n], can one choose multiples
> a_i q_i ≤ e^{n^α} whose set embeds in a difference set S−T with
> |S|=|T| = m^{1/2+o(1)}? Equivalently: can distinct large primes be
> multiplicatively-then-additively organized into a Sidon-realizable set?
> Conjecturally NO for α<½ (⇒ barrier holds ⇒ UW false); a YES would break the
> barrier.

This is a self-contained question a combinatorialist could engage, connected to
B_h/Sidon set theory and to Diophantine simultaneous-approximation. It is the
sharpest formulation the whole investigation has produced of what UW hinges on.


---

## EXACT SOLVER RESULTS — correcting the greedy-realizer conclusion (this session)

Built an exact ILP difference-set embedding solver (`exact_embedding_solver.py`,
validated against brute force) and re-ran the escape question. **It corrects a
wrong conclusion from the weak greedy realizer.**

**AUDIT of the greedy realizer.** On small cases the greedy realizer AGREED with
exact brute force (min-K matched for m≤5). BUT at the scale where escape
conclusions were drawn (m up to 16), the greedy OVERESTIMATED min-K by ~2×
(it reported K≈m; exact solver finds K≈√m). So last turn's suggestion that
"realizing large-prime differences is costly (K≈m), barrier holds via
prime-embedding" was an ARTIFACT of the weak solver. Retracted.

**Exact result (pool-completeness verified: small pool = big pool):**
- Large-prime targets embed as differences at **K ≈ 1.2–1.3·√m** (K=3,4,4,5 for
  m=6,9,12,15). NOT costly. About the SAME as random targets (slightly better).
- So embedding the hard primes as differences is CHEAP (~√m). Prime-embedding is
  NOT the wall.

**But the barrier still holds — the wall is the JOINT constraint.** A pair with
K=3 that embeds 8 large primes covers only **12/120** of [1,n]. Embedding the
primes is necessary but far from sufficient: the same difference set must ALSO
cover all composites and small numbers. The K~√m pair that embeds the primes
badly fails full coverage.

**Corrected localization of the barrier.** It is NOT in:
- set-complexity F (counting-tight), nor
- prime-embedding cost (cheap, K~√m, exact).
It IS in the JOINT constraint: a single difference set S−T of small balanced
sets must SIMULTANEOUSLY (i) embed the ~π(n) hard large prime powers as
differences AND (ii) cover every composite and small integer. Either alone is
cheap; together they conflict. This is the sharp, corrected statement of where
UW's difficulty lives.

**The properly-posed open question (corrected):**
> Does there exist a balanced difference set S−T, |S|=|T|=n^{β}, whose element
> magnitudes are ≤ exp(n^α), that BOTH realizes a covering set of [1,n] AND does
> so with α+β<1? The obstruction is the simultaneity: prime-embedding wants one
> structure (Sidon-like, cheap), full covering wants another (smooth/composite-
> rich), and reconciling them in ONE difference set appears to force α+β≥1.

**Confidence.** Exact solver results are rigorous but small-scale (m≤15, n≤200).
The "joint constraint is the wall" statement is now the best-supported and
correctly-posed localization, replacing the retracted greedy-based claim. Still
not a proof of the barrier, but the mechanism is now correctly identified and
the earlier bug is fixed.


---

## Joint-constraint analysis: exact solver + the single-scale ceiling (this session)

Built an EXACT ILP solver for the real UW quantity: min K such that a balanced
difference set S-T covers [1,n] (`joint_constraint_solver.py`, `joint_faster.py`).
Exact min-K covering pairs at alpha=0.5: K = 3,3,5,5 for n=12,16,20,24
(K/sqrt n bouncing 0.75-1.12). Correct but does NOT scale past n~24 (witness-
variable blowup) -- too small to distinguish beta=1/2 from beta>1/2.

**Analytic attempt via the (n/2,n] interval (`joint_lower_bound.py`).** Every
integer in (n/2,n] needs its own difference (only itself as a multiple <=n). One
difference d<e^A covers M(n,A) of them (M = max divisors in (n/2,n], measured
growing ~n^0.566 at alpha=0.4). This gives K^2 >= (n/2)/M(n,A), i.e.
beta >= (1-c)/2, hence alpha+beta >= (1+ something)/2 < 1. **Same (1+.)/2
ceiling as counting -- a single interval does NOT prove the barrier.**

**The decisive structural conclusion.** NO single scale/interval yields
alpha+beta>=1; every one gives the (1+.)/2 form. If the barrier is real it MUST
come from a GLOBAL argument summing over ALL dyadic scales n, n/2, n/4, ...
simultaneously (the multi-scale recursion, Step 2, never completed). And we can
now see WHY that recursion is hard: the scales are NOT independent -- one
composite difference covers targets at many scales at once (shared coverage), so
the per-scale constraints cannot be simply summed. This is the SAME
"shared coverage defeats independence" phenomenon as the 7-method table and the
parity obstruction, now appearing at the level of the scale recursion.

**Unified final picture (all routes, one wall).** Every approach bottoms out
identically: seven lower-bound methods, the constructive attempt, set-complexity,
additive-realization, and now the joint/interval analysis ALL reduce to needing
to control a sum over scales whose terms SHARE structure (composite differences
cover many targets/scales at once). That sharing is the parity-linked
obstruction. The multi-scale recursion is the one unattempted route, but it
provably inherits the same difficulty (cross-scale sharing = composite-difference
sharing). 

**Honest terminus.** The barrier is now understood mechanistically from every
angle we can reach: it is a global multi-scale statement, protected by the
sharing of composite differences across scales, which is the parity problem in
disguise. This is not a proof of the barrier, but it is a complete diagnosis of
why elementary/computational methods cannot prove it, and it correctly identifies
the one deep ingredient any proof needs (control of cross-scale sharing / parity).
The exact embedding and covering-pair solvers (`exact_embedding_solver.py`,
`joint_constraint_solver.py`) are validated, reusable tools for future work at
larger scale with stronger compute.


---

## Tao's LP-injection route tested: the parity factor is a CONSTANT (this session)

Tested the one literature-endorsed route we hadn't tried: Tao's suggestion to
inject parity information as a constraint into the covering LP (sieve-as-LP).
(`parity_lp_setup.py`, `parity_injection_test.py`.)

**Finding 1 (real characterization): F/floor = the parity factor of 2.**
The ratio of the true covering-set complexity F to the counting floor psi(n)/A:
- alpha=0.4: F/floor = 1.99, 2.05, 2.00, 2.10, 2.02, 2.08 (mean 2.07) -- pinned
  at ~2 across n=45..200.
- alpha=0.5: ~1.4 (parity bites less where hard prime-like numbers are sparser).
This MATCHES the parity literature's signature exactly (Wikipedia/Tao: parity
makes upper bounds "off from the truth by a factor of 2 or more"). The ~2x gap
we saw all session between the proven counting bound and true F is precisely the
PARITY CONSTANT. The dual also concentrates ~85% of its weight on odd-omega
("prime-like", Liouville=-1) numbers -- direct evidence the cost is parity-
structured.

**Finding 2 (decisive, negative for beating the barrier): the parity factor is
a CONSTANT and cannot move the exponent.** F ~ 2*floor means beta_set is higher
by only log2/(2 log n) -> 0. So even a PERFECT parity injection (recovering the
full factor of 2) changes beta by o(1) and does NOT move alpha+beta off the
barrier line. Tao's injection is designed to recover CONSTANT-factor losses (the
"factor of 2" in prime detection); here the loss IS a constant factor, so the
technique would "work" (close the 2x) yet be USELESS, because the barrier is an
EXPONENT statement (alpha+beta>=1) untouched by any constant.

**Resolution of the parity thread (both halves now hold together).**
- Parity IS genuinely the obstruction: the factor of 2 is real, measured, and
  concentrated on odd-omega numbers.
- YET beating parity would NOT beat the barrier: parity costs a CONSTANT here,
  the barrier is EXPONENTIAL, and constants don't move exponents.
This explains the tension implicit all along. The barrier's exponent does NOT
come from parity; parity only controls the constant. So the barrier, if real,
has a source BEYOND parity -- and every method we tried (which all bottomed out
at parity) was therefore attacking the wrong layer for the EXPONENT.

**Consequence.** This REOPENS the exponent question in a specific way: since
parity only governs the constant, the EXPONENT gap between proven (2beta+alpha>=1)
and conjectured (alpha+beta>=1) must have a non-parity origin. The joint
constraint / multi-scale sharing (previous section) is the candidate source, and
it is NOT parity -- it is the combinatorics of how one difference covers many
scales. That is the true open question for the exponent, and it is NOT obviously
parity-obstructed -- a more hopeful (if still hard) position than "parity blocks
everything."


---

## Multi-scale approach: collapses the barrier onto the pair-realization gap (this session)

Pursued the multi-scale combinatorial route (the non-parity exponent question).
Three results, ending in a clean structural conclusion.

**1. The problem collapses to ONE interval.** F_top(n,A) := min elements to cover
just (n/2, n] EQUALS F_full (measured identical at every n, `top_scale_analysis.py`).
Covering the top dyadic interval forces the whole cover; everything ≤ n/2 comes
free. So the entire covering problem = a single clean interval problem, parity-free:
"how few integers ≤ e^{n^α}, each a product of prime powers ≤ n, cover (n/2,n] by
divisibility?"

**2. The interval's cost is governed by M_top(n,A)** = max #divisors in (n/2,n] of
one admissible element. Measured M_top exponents: ~0.73 at α=0.4, ~1.0 at α=0.5.
F_top ≥ |I_0|/M_top, so F_top exponent ≈ 1 − (M_top exponent).

**3. DECISIVE: the barrier cannot be a set-covering statement.** For a SET bound
to give α+β≥1 needs F_top exponent ≥ 2(1−α) (since β≥log F/(2 log n), K²≥F). At
α=0.4 that requires F_top exponent ≥ 1.2. But F_top ≤ |I_0| ~ n/2, so its
exponent is ≤ 1 — ALWAYS. It is ARITHMETICALLY IMPOSSIBLE for set-covering cost
(any scale, any bundling) to reach the barrier when α<½. The set world tops out
at exponent 1; the barrier as a set bound needs 2(1−α)>1.

**Conclusion (two independent routes now agree).** The barrier, if real, is NOT
a set-covering statement — it lives ENTIRELY in the set→pair realization gap (the
factor-of-2-in-exponent between #differences needed, ≤ n, and the balanced size K
with K²≥ that). This was reached earlier from the ADDITIVE side (overdetermination)
and is now FORCED from the MULTI-SCALE/set-complexity side by arithmetic
impossibility. And per the parity finding, this realization gap is where the
EXPONENT lives and is NOT parity-obstructed.

**The final, sharply-localized open problem.** The whole of UW's α+β≥1 (if true)
reduces to:
> For a covering set D of (n/2, n] with |D| ~ n^{1−α}, realized as D ⊆ S−T with
> |S|=|T|=K: is K forced to be n^{1/2−o(1)} (⇒ β≥1/2 ⇒ barrier) even though
> |D| ~ n^{1−α} with 1−α < 1? I.e., does the OVERDETERMINATION of realizing a
> divisibility-covering set as a balanced difference set cost a full extra
> square-root in K beyond the counting √|D|?
This is a pure additive-combinatorics question (difference-set realization of a
prescribed multiplicatively-structured set), parity-free, and is THE remaining
crux. Both the multi-scale and additive programs have delivered it to this single
point.

**Confidence.** F_top=F_full and the arithmetic impossibility (exponent ≤1 < 2(1−α))
are solid. M_top exponents are over n≤340 (fragile constant, robust that it's <1
for α<½). The localization to the realization gap is now doubly-supported and is
the honest, sharp terminus of the exponent question.


---

## Direct attack on the crux: efficient at reachable scale, penalty (if any) is beyond it

Attacked the crux question directly with the EXACT covering-pair solver, and
audited the greedy against it.

**Greedy vs exact.** Greedy realizer said K/√F_top growing (3.3→4.9) and
K/√(n/2)~2.3 flat (barrier holds). But greedy OVERESTIMATES. The EXACT solver
gives much smaller K (n=55: exact K=6 vs greedy ~13). Exact ratios: K/√F_top
grows mildly (1.26→1.60), K/√(n/2) flat ~1.1 — same DIRECTION as greedy but far
weaker.

**Efficiency check (the mechanism test).** For exact-optimal covering pairs of
(n/2,n]: nearly ALL K² differences are large (>n/2) and useful, and K² ≈ #targets
(n=30: K²=16, useful large diffs=15, targets=15; n=40: K²=25, useful=22,
targets=20). **No visible waste, no overdetermination penalty at this scale** —
the pair is counting-EFFICIENT (K≈√|I_0|).

**Honest resolution.** The overdetermination penalty (extra √ in K), IF it
exists, would only appear once M_top (max targets per difference) is large enough
that bundling SHOULD help but the balanced-pair structure PREVENTS it. At
reachable scale M_top is only 1–4, so we are BELOW that regime and the pairs look
efficient. The exact solver (n≤55, K≤6) cannot reach the regime where the crux is
decided. So the crux is:
- REAL and sharply posed,
- but lives at large M_top (equivalently large n with α bounded below ½),
- beyond both exact ILP and enumeration here.

**Leaning (weak).** Small-scale exact data leans toward covering pairs being
EFFICIENT (K≈√F_top), which would mean realization is NOT extra-costly ⇒ barrier
BREAKABLE ⇒ UW possibly TRUE — the OPPOSITE of the greedy's suggestion. But M_top
is too small to trust this; it is a hint, not a finding. The direction genuinely
flips between the biased greedy (barrier holds) and the small-scale exact
(efficient/breakable), which is precisely why only larger-scale exact computation
or a real theorem can settle it.

**Status.** The crux is the correct, sharp, parity-free question and both programs
deliver it here. It is NOT resolved. The honest next step is larger-scale exact
covering-pair computation (stronger ILP/commercial solver, or a smarter
formulation exploiting that all useful differences are large) to reach M_top≫1,
OR an additive-combinatorics theorem on difference-set realization of
multiplicatively-structured target sets. Both are beyond this environment's reach.


---

## Negation map + proof attempt: the barrier reframed as random-vs-optimal (this session)

Eric's negation-map suggestion led to the cleanest framing of the crux yet.

**Negation map finding.** Restricting to the SYMMETRIC self-difference set S-S
(T=-S) costs only a BOUNDED constant factor: K(S-S)/K(S-T) ~ 1.25-1.40, flat in
n (`negation_map_test.py`). Same constant => SAME EXPONENT beta. So the barrier
can be studied entirely in the S-S setting, where Sidon/B_h/difference-basis
theory applies. This is the bridge to classical additive combinatorics we lacked.

**Reformulation (clean).** S covers (n/2,n] by divisibility  <=>  every prime
p in (n/2,n] divides the product D(S)=prod_{i<j}(s_j-s_i)  <=>  for every such p,
two elements of S coincide mod p.

**Two bounds, and the gap between them IS the barrier:**
- RIGOROUS lower bound (product/counting): each factor s_j-s_i < e^A is divisible
  by <= A/ln(n/2) primes >n/2; #factors <= K^2/2; so covered primes
  <= K^2 n^alpha/(2 ln n). Need >= n/(2 ln n) => K >= n^{(1-alpha)/2},
  beta >= (1-alpha)/2. (e.g. beta>=0.3 at alpha=0.4.)
- PROBABILISTIC (random S): E[uncovered primes] ~ |P| exp(-K^2/2n); <1 needs
  K ~ sqrt(2 n ln n), beta = 1/2 + o(1).

**The corrected understanding (important).** The sqrt(n log n) / beta=1/2 result
is an EXISTENCE (upper) bound -- it says random S SUFFICES at that size, NOT that
K must be that large. The only rigorous LOWER bound is n^{(1-alpha)/2}
(beta>=(1-alpha)/2), which is BELOW 1/2 for alpha<1/2. So the gap
[ (1-alpha)/2 , 1/2 ] is exactly undetermined, and:
  * if optimal K ~ sqrt(n log n) (random is optimal) => beta=1/2 => BARRIER HOLDS.
  * if optimal K ~ n^{(1-alpha)/2} (clever S beats random) => beta=(1-alpha)/2
    => alpha+beta=(1+alpha)/2 < 1 => BARRIER FALSE => UW TRUE.

**Falsification test.** Tried to beat random with structured S (geometric,
multiplicative subgroup, prime-spaced): NONE beat random; random+repair stays
best (`structured_falsify.py`). Evidence that random is ~optimal (=> barrier
holds), but only n<=200 and 3 structure families -- WEAK.

**THE precise open question (sharpest form).** Is the random covering size
sqrt(n log n) optimal, or can a structured S-S cover (n/2,n] by divisibility with
K ~ n^{(1-alpha)/2} (the counting floor)? This is a clean extremal
additive-combinatorics / difference-basis question:
> minimize |S| such that every prime in (n/2,n] divides prod_{i<j}(s_j-s_i),
> with all s_i <= exp(n^alpha).
No proof is known either way. The rigorous LB is n^{(1-alpha)/2}; the random UB
is sqrt(n log n); closing the gap resolves UW in the alpha<1/2 regime. The
second-moment argument does NOT close it (it only reproduces the counting LB).

**Honest status.** This is the true terminus reached from every direction: a
single, clean, classical-flavored extremal question with a rigorous lower bound
(counting) and a probabilistic upper bound (random), gap unresolved. The negation
map made it a self-difference (Sidon-type) problem, which is the right home for
it. Resolving it needs a real additive-combinatorics theorem on difference bases
with a divisibility (rather than value-covering) target -- beyond computation.


---

## Thinking like an additive combinatorialist: the Vandermonde reformulation and a CONDITIONAL proof (this session)

**Reformulation (new, clean).** S covers (n/2,n] by divisibility <=> every prime
p in (n/2,n] divides the VANDERMONDE V(S) = prod_{i<j}(s_j - s_i). Classical
fact: V(S) is always divisible by the superfactorial 1!2!...(K-1)! and a prime p
divides that iff p <= K-1 -- which explains structurally why APs need K ~ n:
an AP's Vandermonde has only the guaranteed divisibility. Covering primes near n
with K << n requires DESIGNED divisibility.

**Scope insight (important, previously missed).** UW asks only whether BOTH
alpha < 1/2 AND beta < 1/2 are achievable. So proving "beta >= 1/2 whenever
alpha < 1/2" settles UW (negatively) WITHOUT proving the full barrier
alpha+beta>=1. The minimal target is cheaper than the barrier.

**The type-counting first-moment argument (new).** For any covering S, each
prime p has a colliding pair (s_i = s_j mod p); pick an assignment phi: P->pairs.
Count pairs (phi, S):
- #assignments <= (K^2)^{|P|} = e^{gamma*n} for K = n^gamma  (|P| ~ n/(2 ln n)).
- For fixed phi: sequential CRT gives #S(phi) <= M^K * prod_{p in P} 1/p
  = e^{n^{gamma+alpha} - n/2(1+o(1))}. VERIFIED numerically incl. cycles
  (`vandermonde_argument_check.py`: path ratio 1.000, cycle 1.003).
- Total: #covering S <= e^{gamma*n + n^{gamma+alpha} - n/2} -> 0 for any fixed
  gamma < 1/2, alpha < 1/2 (asymptotically; near gamma+alpha->1 the crossover n
  is astronomically large -- an asymptotic statement only).

**CONDITIONAL THEOREM (stated honestly).** IF the count restricted to
"hub-heavy" assignments can be bounded (see leak below), THEN for every fixed
alpha < 1/2: no covering S with K = n^gamma, gamma < 1/2, exists for large n.
Hence beta >= 1/2 whenever alpha < 1/2 => **UW is FALSE**. The random
construction (K ~ sqrt(n log n)) shows this would be TIGHT.

**THE LEAK (isolated, verified, unclosed).** The CRT count M^K/prod(p) fails
when a vertex's accumulated modulus exceeds M: then choices are 0-or-1, we must
bound by 1, and the forfeited savings can reach e^{n/2} for assignments that
hoard modulus onto few high-degree "hub" vertices. Crude accounting shows the
leak flips the exponent positive precisely in the interesting range
gamma in ((1-alpha)/2, 1/2) (verified in the exponent table). Closing it
requires: a bound showing congruence systems with total modulus >> M have
solutions <= M so rarely that hub assignments contribute e^{-cn} IN TOTAL --
a "small solutions to overdetermined CRT systems" estimate (large-sieve
flavored; note Gallagher's larger sieve with nu(p)=K-1 was re-derived and gives
only the counting bound -- one collision per prime is too little information
for sieve methods; the leak needs a different tool).

**Honest assessment.** This is the first PROOF-TRACK structure of the whole
project: a complete argument with a single, precisely-located, numerically-
verified gap. The gap is the familiar enemy (bundling/shared structure) in its
sharpest form yet: not a fog, but one quantified statement about small CRT
solutions. Session history (many dead "proofs") counsels real skepticism --
the leak may be fatal, since hub assignments are exactly where a clever
construction would live if UW were true. But the argument also explains WHY
the empirical record looks the way it does: random is optimal unless hubs
help, hubs = bundling concentration, and every constructive test of bundling
concentration has failed. Proof and experiments point the same way: UW false,
beta >= 1/2 forced -- unproven pending the leak.


---

## Sum-product framing: the mechanism behind the barrier (this session, NEW)

Thinking as an additive combinatorialist produced four approaches (Vandermonde
p-adic valuations; CRT/covering-array non-separating families; graph-congruence
overdetermination; sum-product). The sum-product one is the keystone and is
newly identified.

**Reformulation.** S covers (n/2,n] <=> the primorial Q=prod_{p in (n/2,n]} p
divides the VANDERMONDE determinant V(S)=prod_{i<j}(s_j-s_i) <=> S is
non-injective mod every such p.

**Sum-product mechanism (tested, `sumproduct_test.py`).** To beat the barrier
(K below sqrt(n log n)) you need S-S MULTIPLICATIVELY RICH: its elements
divisible by many primes in (n/2,n], so each difference bundles many primes. But
S-S is an ADDITIVE object. Measured multiplicative richness of S-S vs additive
structure of S (n=400, K=40):
  - AP (max additive, |S-S|~2K):      richness 0.000  (covers ZERO primes)
  - GAP rank-2 (intermediate):        richness 0.129
  - random/Sidon (|S-S|~K^2):         richness 0.922
Richness tracks additive spread monotonically and sharply -- a textbook
Erdos-Szemeredi sum-product signature: additive structure and multiplicative
richness are ANTAGONISTIC.

**Why this is the barrier's mechanism.** Beating the barrier needs BOTH:
(i) few elements / additive economy (to keep K small), AND
(ii) heavy prime-bundling / multiplicative richness (to cover with few
    differences).
Sum-product forbids their combination: additively economical sets (AP/GAP) have
multiplicatively trivial difference sets; multiplicatively rich difference sets
require Sidon-like S with K^2 DISTINCT (unbundled) differences. You cannot have
both. This is a cleaner, deeper "why" than parity (which we showed governs only
the constant) or raw counting.

**Honest direction of the evidence.** Sum-product obstructs BREAKING the barrier,
not proving beta>1/2 directly: the RANDOM (Sidon) S still achieves ~92% richness
and covers at K~sqrt(n log n). Sum-product explains why no additively-clever S
pushes K BELOW that. So it supports beta=1/2 + o(1) => BARRIER HOLDS => UW false
for alpha<1/2. It is a mechanism/heuristic, not yet a proof: making it rigorous
needs a quantitative sum-product bound (Bourgain-Katz-Tao / Solymosi flavor)
showing |S|=K with S-S covering (n/2,n] forces K >= sqrt(n)/polylog. That is a
concrete, named additive-combinatorics target -- the sharpest and most promising
proof route identified in the whole investigation, and it is NOT parity-blocked.

**Convergence.** All four approaches point the same way: the barrier holds at
beta=1/2, and the obstruction to beating it is the sum-product antagonism between
additive economy and multiplicative richness of the difference set. The proof
route is a quantitative sum-product bound; the falsification (structured S beating
random) FAILED, consistent with the mechanism. This is the honest terminus:
mechanism identified, proof route named, both parity-free.


---

## Differentiation/discriminant reformulation + three-way synthesis (this session)

Eric's suggestion (sum-product + sum rule/linearity of differentiation) yielded a
rigorous and elegant reformulation and a unified explanation of the barrier.

**The reformulation (verified exactly, `discriminant_reframe.py`).** For
f(x)=prod_i(x-s_i): by the sum rule, f'(x)=sum_i prod_{j!=i}(x-s_j). Then
  S covers (n/2,n]  <=>  f has a repeated root mod every p in (n/2,n]
                    <=>  Q=prod_{p in (n/2,n]} p  divides  disc(f)=Res(f,f')=±V(S)^2.
Also (verified) Res(f,f')=±K^K prod_j f(t_j) over the K-1 critical points t_j
(roots of f'), so covering is controlled by only K-1 CRITICAL VALUES, not K^2/2
differences. The derivative is the genuine engine (repeated root <=> f,f' share a
root <=> p|disc).

**Constructive test (`deriv_construction.py`).** A CRT/congruence construction
(assign primes to element-pairs, solve s_i≡s_j mod bundled-prime-products on a
graph) does NOT beat random: n=80 both ~10, n=120 13 vs 12. No constructive win.
The failure cause is exactly what the derivative framing predicts: f' has degree
K-1, so the ~K^2/2 divisibility conditions are routed through a RANK-(K-1)
difference space (cycle-consistency d_ik=d_ij+d_jk) -> overdetermined; the
tree/star subcase provably hits the alpha=1/2 wall (bundling needs pair-products
up to e^{n^{1-alpha}} > e^{n^alpha} budget when alpha<1/2).

**THREE-WAY SYNTHESIS (the payoff): why the barrier holds at beta=1/2.**
Three independent routes, all parity-free, all agreeing:
 1. SUM-PRODUCT: beating it needs S-S additively economical (small K) AND
    multiplicatively rich (bundling) -- Erdos-Szemeredi antagonists. Tested:
    richness tracks additive structure (AP 0%, random 92%).
 2. RANK/DERIVATIVE: differences live in a rank-(K-1) space (f' has degree K-1)
    but face ~K^2 divisibility constraints -> overdetermined; star subcase hits
    the alpha=1/2 wall. Tested: CRT construction can't beat random.
 3. COUNTING: every elementary count gives K >= n^{(1-alpha)/2}; the gap up to
    sqrt(n log n) is exactly where sum-product forbids improvement.
These are ONE phenomenon in three languages: additive economy and multiplicative
richness cannot coexist (sum-product) BECAUSE the differences are rank-constrained
(derivative) WHICH IS WHY counting cannot be beaten. Conclusion: beta=1/2,
alpha+beta -> 1, BARRIER HOLDS, UW false in the alpha<1/2 regime -- with a
mechanism, not just evidence.

**Rigorous proof route (named, parity-free).** A quantitative sum-product bound:
show |S|=K with S-S covering (n/2,n] by divisibility forces K >= sqrt(n)/polylog.
The discriminant reformulation Q|disc(f) plus a Bourgain-Katz-Tao/Solymosi-type
multiplicative-energy bound on difference sets is the concrete target. This is the
sharpest, most promising, and most classical route the whole investigation has
produced, and it is NOT parity-obstructed.


---

## Fourth route: character-sum / second-moment (inverse-subtraction-modulo)

Eric's 'inverse, subtraction, modulo' suggestion -> the character-sum
reformulation (subtraction=differences, modulo=reduction mod i, inverse=Fourier
inversion). X_i = #collisions mod i = (1/i) sum_{t!=0} |S-hat_i(t)|^2; target i
covered <=> X_i>=1.

**Cauchy-Schwarz second moment (`second_moment_fourier.py`).** #covered >=
(sum X_i)^2 / sum X_i^2. Measured at the covering K: C-S bound (49,102,210) sits
BELOW actual coverage (64,132,270) and below |I0| (100,200,400). So plain C-S is
WEAK -- clumping (sum X^2/sum X ~ 4, constant in n) dilutes it. Does NOT prove
beta>=1/2 by itself. The clumping is a GCD structure (pairs of differences with
gcd>n/2) -- the Euclidean 'subtraction and modulo' reading.

**Union / second-moment threshold (`janson_gcd.py`).** The right tool for
covering ALL targets is sum_i P(X_i=0)<1. Measured at K=sqrt(n ln n):
sum P(uncov) = 2.96, 4.50, 6.18, 7.11 for n=200..1600 -- GROWING, not O(1). So
sqrt(n ln n) is NOT quite the threshold; the true threshold is slightly HIGHER
(polylog heavier than sqrt(log n), e.g. ~sqrt(n log n loglog n) or larger
constant). BUT all are sqrt(n)*subpolynomial => beta = 1/2 + o(1) regardless.

**What this route establishes (fourth independent confirmation).** The
character-sum second moment confirms beta=1/2 (the exponent), and explains WHY
K/sqrt(n) kept slowly RISING in the GPU runs: it is the polylog factor, not a
larger exponent. The gcd/clumping (Euclidean structure) sets only the constant
and polylog, never the exponent. Consistent with sum-product, rank/derivative,
and counting -- now FOUR independent routes all giving beta=1/2, all parity-free.

**Refined honest statement.** min-K for S-S covering (n/2,n] by divisibility is
sqrt(n) * (polylog n), i.e. beta = 1/2 + o(1). The polylog is heavier than the
naive coupon-collector sqrt(log n) (the second-moment sum grows), but sub-
polynomial. => alpha+beta -> 1, BARRIER HOLDS. The four routes (sum-product,
rank/derivative, counting, character-sum second moment) are mutually consistent
and none is parity-obstructed. A fully rigorous proof still needs the
quantitative sum-product/large-sieve bound to replace the probabilistic
(random-S) threshold with an all-S lower bound -- but every method agrees on the
answer.


---

## Correction + fixed-alpha experiment + the proved theorem (this session)

**Regime correction (important, corrects recent turns).** The sqrt(n log n)
empirics were all at magnitude M=n^1.5 (polynomial), i.e. effective alpha->0,
NOT fixed alpha<1/2. Verified that min-K DROPS as M grows (n=60: K=12,11,11 for
M=n^1.5,n^3,n^6). So the polynomial-magnitude empirics do NOT bound fixed-alpha
K, and the recent 'beta=1/2, barrier holds' reading conflated regimes. Retracted.

**PROVED theorem (clean, rigorous).** `covering_lower_bound.pdf`: via the
discriminant reformulation, covering P(n) forces K(K-1) log(2M) >= theta(n)-
theta(n/2) ~ n/2, hence K^2 >= n/(2 log M), i.e. **2 beta + alpha >= 1**. This is
the counting bound, now with a clean discriminant proof and an explicit remark
that the method is tight as a magnitude bound (cannot yield a stronger exponent).
This is the one rigorous theorem of the realization program.

**Fixed-alpha experiment (`fixed_alpha_experiment.py`).** At CORRECT magnitude
e^{n^alpha}, the pair-budget feasibility exponent converges to the COUNTING floor
(1-alpha)/2, not the barrier (1-alpha): at alpha=0.3, beta_feas = 0.383, 0.356,
0.350 -> (1-alpha)/2=0.35 as n=1e4..1e8; K_feasible tracks n^{(1-alpha)/2}
(629 vs 631 at 1e8). So at fixed alpha the magnitude budget is generous enough
that the counting floor is BUDGET-FEASIBLE.

**Corrected honest status of UW.**
- PROVEN: 2 beta + alpha >= 1 (discriminant/counting). Consistent with UW true
  (e.g. alpha=beta=0.4).
- At fixed alpha<1/2, the counting floor K~n^{(1-alpha)/2} is BUDGET-FEASIBLE
  (this experiment) => IF realizable as a balanced difference set, 2beta+alpha=1
  is tight, alpha+beta=(1+alpha)/2<1, and UW is TRUE.
- The ONLY remaining obstruction is REALIZABILITY: can K^2 pair-divisibility
  constraints be met by 2K elements (the overdetermination)? This is the crux,
  still open, and it is where the sum-product / rank considerations live.
- The earlier 'barrier holds' leanings were an artifact of polynomial-magnitude
  measurement. At correct magnitude the budget FAVORS UW; whether realizability
  spoils it is genuinely undecided.

**Net:** the honest frontier is the realizability of the counting-floor
construction at fixed alpha. If realizable => UW TRUE (barrier false). The
budget feasibility (this experiment) removes the magnitude objection; only the
additive-realization overdetermination remains. This REOPENS UW-true as a live
possibility that the mis-regimed empirics had obscured.


---

## Reassessment of the 7 early methods under the corrected (fixed-alpha) target

The 7-method program was aimed at proving a lower bound ABOVE counting (toward
the barrier / UW false). With the corrected target -- "is the counting floor
REALIZABLE at fixed alpha => UW TRUE" -- three of the 'failures' flip to POSITIVE
evidence, and were only ever tested at polynomial magnitude.

**Now have merit (pro-UW, re-tested at fixed alpha):**
- Method 4 (additive penalty): RE-RUN at fixed-alpha magnitude
  (`penalty_fixed_alpha.py`). penalty = K_pair^2 / F_set -> 1.029, 1.018, 1.004
  (alpha=0.3, n=1e4..1e8) and ~1.03 (alpha=0.4). NO counting penalty: a
  difference set costs the same as a free set for covering. Necessary condition
  for the counting floor to be realizable => pro-UW.
- Method 6 (structured/Erdos constructions): reframe from lower-bound method to
  CONSTRUCTION method; they showed efficient covering -- now the goal, not a
  failure.
- Method 7 (shared alignment bits): the 'shared not independent' mechanism is the
  CONSTRUCTION PRINCIPLE for realizing bundled targets, not an obstruction.

**Still dead (structural, regime-independent):** Methods 2,3,5 (second-moment /
large sieve / Gallagher) fail for L2-vs-Linf / union-breaks-linearity reasons the
regime correction does not touch. No merit gained.

**Caveat.** Method 4's 'no penalty' is a COUNTING/budget statement (K^2 ~ F),
NOT realizability. Budget-feasibility (no penalty) is necessary, not sufficient;
the overdetermination (can a specific S-T hit the bundled targets) is still open.

**THE genuinely new approach the reframe demands.** None of the 7 attacks
REALIZABILITY (all sought lower bounds). The right untried tool is a CONSTRUCTIVE
EXISTENCE argument -- Lovasz Local Lemma or Rodl-nibble/semi-random construction
-- to BUILD a difference set hitting the bundled targets and PROVE the counting
floor is realizable. That would resolve UW in the TRUE direction. This is the
first genuinely new method identified since the 7-method program, and it is
enabled specifically by the shift from 'prove a lower bound' to 'prove a
construction exists'.


---

## Constructive-existence attempt: a FALSE barrier proof caught, then pro-UW evidence

Attempted the new constructive-existence approach (LLL / semi-random) to decide
realizability of the counting floor at fixed alpha.

**Naive LLL fails (correctly).** Independent-uniform S at the counting floor
K~n^{(1-a)/2} has P(collide mod p) ~ K^2/2p -> 0, so random S does not cover.
Must use STRUCTURED randomness: assign primes to element-PAIRS (bundling) and
solve the congruence system s_i ≡ s_j mod m_ij. (`lll_attempt.py`)

**A FALSE lower-bound 'proof' -- caught by self-attack.** I derived an argument
that each element s_i, being in ~K pairs, must be determined mod a prime-product
of log-size ~ vertex-log, with avg vertex-log = n/K; requiring <= n^alpha gives
K >= n^{1-alpha} => alpha+beta>=1 = THE BARRIER. Numerics matched (avg vtx log
~ n/K). This looked like a proof of the barrier (`realizability_bound.py`).
IT IS WRONG. The load-bearing claim 's_i must have MAGNITUDE e^{vertex-log}' is
false: s_i is pinned only to a small RESIDUE, not a large value. Elements can
SHARE residues (the same loophole that broke every prior barrier argument:
shared, not independent).

**Attack confirms the bound is broken (`attack_the_bound.py`).** Actually solving
the congruence system for SMALL elements (spanning-tree propagation, shared
residues): max|s_i| stays WITHIN budget and the margin GROWS with n:
  alpha=0.3: max|s_i|=e^{6.2},e^{7.6},e^{9.0} vs budget e^{6.5},e^{9.8},e^{14.8}
  (n=500,2000,8000). Room to spare, widening.

**Honest result (pro-UW).** The counting-floor construction appears REALIZABLE at
fixed alpha: the congruence system is consistent (distinct primes => each
constrains one pair => always solvable) AND elements stay within the magnitude
budget by sharing residues. This is genuine evidence that 2beta+alpha=1 is tight
=> alpha+beta=(1+alpha)/2<1 => UW may be TRUE (barrier FALSE) at fixed alpha.

**Caveats (do not overclaim the mirror of the error).**
- This is a heuristic construction succeeding at tested sizes (n<=8000), NOT a
  proof. Need: prove the assignment always exists (budget packing) AND the
  spanning-tree solution always stays <= e^{n^alpha} as n->infinity.
- alpha=0.4,n=2000 hit 'budget exceeded' in the greedy prime-to-pair packing --
  a packing failure to understand (may need better assignment, or a real
  obstruction at larger alpha).
- Must confirm distinctness of elements and that ALL non-tree edges are satisfied
  (the code checks, but at scale this needs proof).

**Status: the honest lean has FLIPPED to pro-UW at fixed alpha.** The magnitude
budget (fixed-alpha experiment) plus realizability-by-residue-sharing (this test)
both favor the counting floor being achievable => UW true. The barrier arguments
keep dying on the same shared-residue loophole. A rigorous UW proof now needs:
(1) a packing lemma (primes -> pairs within budget), (2) a bounded-solution lemma
(congruence system solvable with s_i <= e^{n^alpha}), (3) distinctness. All three
look plausible at fixed alpha<1/2 but are unproven. This is the sharpest pro-UW
position the investigation has reached.


---

## The three lemmas: a three-way incompatibility (this session, decisive)

Attempted to prove Lemmas 1-3 (packing / bounded-solution / distinctness) to
establish UW true. Result: caught last turn's pro-UW read as an ILLUSION, and
mapped the real obstruction.

**Lemma 1 (packing): TRUE.** Distributing primes (item log-size ~ln n) into
K^2/2 pairs of capacity n^alpha: since n^alpha >> ln n, granularity waste is
lower-order, so K = n^{(1-alpha)/2}(1+o(1)) suffices by greedy bin-packing.
(Standard; the alpha=0.4 'budget exceeded' was zero-slack round-robin, fixable.)

**Lemma 2/3 are INCOMPATIBLE at the counting floor -- three-way conflict.**
Tested the congruence system s_i ≡ s_j mod m_ij three ways:
1. SMALL + all edges satisfied  => requires ALL elements equal (s_i=0 for all);
   `lemma2_mechanism.py` found distinct=1, zeros=K. DEGENERATE -> fails Lemma 3.
   (This was last turn's pro-UW illusion: 0≡0 mod everything.)
2. SMALL + DISTINCT  => only spanning-TREE edges satisfied (K-1 of them);
   coverage collapses to ~tree bound (9/42, 16/135, 30/457 primes);
   `distinctness_forced.py`. => covers only ~K-1 pairs => K~n^{1-alpha} (tree
   bound), NOT the counting floor.
3. DISTINCT + all edges  => each element pinned mod product of incident-edge
   moduli (log = vertex-log ~ n/K), and distinct => magnitude ~ e^{n/K};
   ratio max/budget = 12,18,36,47 (alpha=0.3) GROWING; `barrier_via_distinctness.py`.
   => needs magnitude >> e^{n^alpha} => exceeds budget => NOT realizable.
You cannot have small + distinct + full-coverage simultaneously.

**The correct obstruction (replaces the FALSE vertex-log 'proof' from before).**
Covering prime p needs s_i ≡ s_j mod p with s_i != s_j (distinct) => |s_i-s_j|>=p
> n/2. Full coverage needs ~K^2/2 such non-tree congruences; distinctness forbids
the collapse that made them cheap; together they force spread. This is the
genuine version of the barrier mechanism, and unlike the earlier vertex-log
argument it is NOT immediately defeated by residue-sharing (sharing => collapse
=> distinctness fails).

**HONEST caveat (do NOT declare victory -- same trap as before).** Regime 3's
magnitude is INFERRED from vertex-log, the SAME quantity that fooled the earlier
false barrier proof via the sharing loophole. Whether a CLEVER assignment/solution
threads all three (distinct + all-edges + small) is NOT settled by these
measurements -- it needs an EXACT minimum-magnitude solve of the distinct+all-edges
system (ILP), not a vertex-log inference. So: strong evidence the counting floor
is NOT realizable (=> barrier holds => UW false), but not yet a proof; the loophole
that killed the last barrier argument must be explicitly ruled out here.

**Net status.** Lemma 1 provable. Lemmas 2+3 appear MUTUALLY INCOMPATIBLE with
full coverage at the counting floor (three-way conflict: small/distinct/covering
- pick two). This LEANS BACK toward the barrier holding (UW false), for a correct
reason this time, BUT the decisive check (exact min-magnitude distinct+all-edges
solve, ruling out the sharing loophole) remains to be done. The honest lean has
moved back to barrier-holds, held at appropriate (non-overclaimed) confidence.


---

## Exact solve: counting floor is UNREACHABLE (loophole ruled out) -- this session

Ran the decisive exact check the last turn flagged: does an ACTUAL solver (all
freedom, sharing loophole available, generous magnitude) reach the counting floor?

**Method (`diagnose_feasibility.py`).** Exact ILP: true min-K to cover (n/2,n] by
divisibility with distinct elements in [0,2n] (generous B), detecting Optimal vs
Infeasible explicitly. NO pre-assigned primes, NO tree, NO vertex-log inference --
the solver chooses everything, so it CANNOT be fooled by a bad hand-construction
and CAN use residue-sharing freely.

**Result: true min-K > counting-floor K, ratio not shrinking.**
  n=24: floor 6, true 7 (1.17);  n=30: floor 6, true 8 (1.33);  n=40: floor 7,
  true 9 (1.29). Counting floor is NOT reachable even with full solver freedom and
  generous magnitude.

**Why this matters (rules out the trap).** Both earlier errors -- the false
vertex-log barrier proof AND the degenerate pro-UW construction -- came from
INFERRING magnitude/feasibility from a hand-construction. This exact solve infers
nothing: it directly proves the floor is infeasible at these n, with the sharing
loophole fully available to the solver. So the three-way incompatibility
(small/distinct/covering - pick two) is REAL, not a vertex-log artifact.

**Honest limits.** n<=40 only (ILP explodes); ratio 1.17/1.33/1.29 is not a proven
growth law -- could plateau. What is solid: at every exactly-solvable size the
counting floor is unreachable by a non-shrinking margin. This is genuine evidence
(not proof) that the floor is not realizable => barrier holds => UW false at fixed
alpha.

**FINAL honest status of the lemma program.**
- Lemma 1 (packing): provable.
- Lemmas 2+3 (bounded distinct solution at floor): FALSE together -- three-way
  incompatibility, now confirmed by exact solve (not just vertex-log).
- Consequence: the counting-floor construction does NOT realize => 2beta+alpha=1
  is NOT tight => the honest lean is BARRIER HOLDS (UW false) at fixed alpha<1/2.
- Caveat: exact data only to n=40; a proof needs either (a) a rigorous infeasibility
  argument for the distinct+full-coverage system at the floor (the three-way
  conflict made into a theorem), or (b) larger exact solves (Gurobi) to confirm the
  ratio grows. The provable result remains 2beta+alpha>=1 (`covering_lower_bound.pdf`);
  the barrier (alpha+beta>=1) is now EVIDENCE-BACKED from multiple angles but still
  unproven.

**Net arc of the realization program:** counting floor is budget-feasible (magnitude
OK) but NOT realizable as a distinct difference set (three-way incompatibility,
exact-confirmed). The gap between budget-feasibility and realizability IS the
barrier, and it is a clean additive-combinatorics obstruction: a covering set of
(n/2,n] cannot be realized as a balanced difference set at the counting floor
because full coverage + distinctness force magnitude past the budget.


---

## BUG FOUND: the 'floor unreachable' exact-solve result was a CBC-timeout artifact

Audited `diagnose_feasibility.py`. It had the CBC-timeout bug (the SAME one fixed
earlier in the calibration tool, reintroduced): when min_K_to_cover tried the
floor K and CBC returned 'Not Solved' (TIMEOUT), the code fell through and
advanced to a larger K, then returned that larger K as 'true min-K'. So a
floor-K TIMEOUT was misreported as 'floor infeasible', INFLATING true-min-K and
manufacturing the 'ratio>1, barrier holds' conclusion.

**Corrected check (`diagnose_fixed.py`), explicit per-K status:**
  n=24, floor K=6: OPTIMAL  -> floor IS reachable.
  n=30, floor K=6: Not Solved (timeout) -> UNKNOWN (was falsely 'true min-K=8').
  n=40, floor K=7: Not Solved (timeout) -> UNKNOWN (was falsely 'true min-K=9').

**Consequence: RETRACT the 'counting floor is unreachable / barrier holds' claim
from the prior turn.** It was a timeout artifact, not a proof of infeasibility.
The only cleanly-resolved case (n=24) shows the floor IS reachable, which if
anything leans the OTHER way. The exact solve is INCONCLUSIVE (models too big for
CBC at n>=30 within time limit).

**Error pattern this session (recorded honestly).** The 'barrier holds'
conclusion arose THREE times from artifacts, each a self-inflicted error caught
on audit: (1) false vertex-log 'proof'; (2) degenerate all-zeros pro-UW
'construction'; (3) this CBC-timeout inflation. The recurrence is itself a signal:
every crisp 'barrier holds' result has dissolved under scrutiny, while the
counting floor keeps NOT being proven unreachable. This does not prove UW true,
but it should lower confidence in the barrier and raise caution about any
'barrier holds' claim from a hand-construction or a timeout-prone solver.

**Corrected honest status.**
- PROVEN: 2beta+alpha>=1 (`covering_lower_bound.pdf`). Solid.
- Realizability of the counting floor at fixed alpha: GENUINELY OPEN. Not shown
  unreachable (that was a bug); not shown reachable at scale either (n=24 only).
  The three-way incompatibility (small/distinct/covering) is a real STRUCTURAL
  tension but is NOT established to force magnitude past budget -- the exact solve
  that would decide it times out at n>=30.
- To settle: a stronger MILP solver (Gurobi) to get PROVEN Optimal/Infeasible at
  the floor K for n=30..100, OR a rigorous infeasibility argument. Until then,
  UW's truth at fixed alpha is undetermined and the barrier is unproven.

**Net:** the honest posterior is BACK to genuinely undecided. The only proven
result is 2beta+alpha>=1. Every 'barrier holds' argument this session was an
artifact; the counting floor has not been shown unreachable. UW at fixed
alpha<1/2 remains open in both directions.


---

## Exact min-K sequence: the floor gap stays BOUNDED (this session)

Instead of deciding feasibility per-n (solver times out), computed the EXACT
min-K(n) sequence by fast custom exhaustive search (0 fixed in S), n=12..28
(exact_minK_sequence.py), and examined its limit behavior.

Result: min-K(n) - counting-floor(n) = [1,0,0,0,1,0,0,0,1] for n=12,14,...,28.
The gap is BOUNDED (oscillates 0-1, period ~8, spikes when a new prime enters
(n/2,n]), NOT growing. Corroborating: min-K/sqrt(n) flat-to-decreasing
(1.44->1.32 within each period), consistent with K ~ sqrt(n) = counting-floor
exponent, NOT barrier; fitted exponent log(minK)/log(n) = 0.377, near counting
(1-alpha)/2 and far from barrier (1-alpha)=0.55.

Interpretation (evidence AGAINST the barrier). min-K tracks the counting floor to
within an additive constant (~1). If the barrier held (floor unreachable), the
gap would GROW with n; it does not. Leans toward the counting bound being
essentially TIGHT => alpha+beta=(1+alpha)/2<1 => UW-favorable. Opposite of the
(retracted, buggy) 'barrier holds' claims; consistent with the clean n=24 point.

Honest limits. n<=28 only (exhaustive search dies ~n=30). A gap bounded on [12,28]
could grow very slowly (e.g. +loglog n) further out -- not excluded. The period-8
'+1' spikes are a granularity effect (new prime entering), not a trend. So: real
evidence the floor gap is bounded (pro-UW), but a bounded-gap THEOREM is not
established.

Corrected posterior after the full session. Only PROVEN result: 2beta+alpha>=1.
Every crisp 'barrier holds' result was an artifact (vertex-log, degenerate
construction, CBC timeout -- all caught). The one clean asymptotic probe (exact
min-K sequence) leans the OTHER way: min-K ~ floor + O(1), counting essentially
tight, UW-favorable at fixed alpha. Net honest lean: mildly PRO-UW (barrier likely
false), on the strength of the bounded floor gap -- unproven, small-n only. To
settle: extend the exact sequence (Gurobi / better search) to see if minK-floor
stays O(1) into n=50..200, or prove a bounded-gap result directly.


---

## Extended exact min-K sequence to n=34: gap stays in {0,1}, returns to 0

Faster bitmask search (fast_minK.py) extended the exact min-K(n) sequence to n=34.
Floor-gap sequence (min-K - counting-floor), n=12..34 step 2:
  [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
Max gap = 1 (never 2); fraction with gap>=1 is 0.33 and NOT climbing. Crucially
the two largest points (n=32,34) returned to gap 0, so the n=28,30 'two 1s in a
row' was transient noise (prime-entry granularity), not the onset of drift.

Strengthened reading: min-K - floor stays bounded in {0,1} with repeated returns
to 0 including at the largest n. If the barrier held, the gap would begin climbing;
it does not. Artifact-free (exhaustive search, no solver/hand-construction). This
is the cleanest evidence in the whole investigation and it is PRO-UW: the counting
floor 2beta+alpha=1 appears essentially tight => alpha+beta<1 => UW-favorable at
fixed alpha.

Still open: n<=34; cannot formally exclude a very slow climb (gap->2 at large n).
But the return-to-0 at the largest computed n is exactly the signature of a
bounded gap, not a drift. To settle: push the exact sequence to n~60-120 (further
optimized search or Gurobi) and confirm the gap never reaches 2; or prove a
bounded-gap theorem.


---

## CORRECTION: the exact min-K sequence was in the wrong (no-bundling) regime

Before attempting a bounded-gap theorem, inspected the exact-optimal covering
sets (inspect_optimal.py, bundling_check.py). Finding that invalidates the
pro-UW reading of the min-K sequence:

**The exact search used B=2n, which forbids bundling.** A difference d<=2n is
divisible by AT MOST ONE prime >n/2 (two such primes multiply to >n^2/4 > 2n).
Confirmed in the optimal sets: nearly every prime p is covered by the difference
d=p itself; multi-covers are rare (d=54->{18,27}, d=66->{22,33}) and never
bundle two LARGE primes. So the search operates in the K^2 ~ |targets| ~ n
regime (K ~ sqrt n), NOT the bundled counting-floor regime.

**Consequence: the 'gap in {0,1}' finding does NOT bear on the barrier.** The
counting floor n^{(1-a)/2} assumes each difference bundles ~n^a/ln n primes.
That bundling requires differences up to e^{n^a} >> 2n, i.e. much larger n than
34. At n<=34 the assumed bundling is ~1 anyway, so 'min-K ~ floor' is comparing
sqrt-n-regime data to a floor whose premise is not yet active. It is NOT evidence
for or against UW.

**Pattern (stated plainly).** This is the FOURTH regime/measurement artifact this
session (after: vertex-log false proof, degenerate construction, CBC-timeout bug).
Every crisp signal -- in BOTH directions -- has come from an accessible small/wrong
-magnitude case mis-mapped onto the fixed-alpha asymptotic regime, which is out of
computational reach (bundling needs B up to e^{n^alpha}, where exact search
explodes). The honest lesson: small-n exact computation CANNOT probe the barrier,
because the barrier lives in the bundled regime that only appears at large n with
super-polynomial magnitude.

**Corrected posterior (final, honest).** The ONLY reliable result remains the
proven 2beta+alpha>=1 (covering_lower_bound.pdf). On the barrier (alpha+beta>=1)
vs UW-true: GENUINELY UNDECIDED. No computational probe available here reaches the
bundled regime; every small-n signal was an artifact of the accessible regime.
Settling UW at fixed alpha<1/2 requires either (a) analysis in the bundled regime
directly (differences = products of many large primes, realized as a difference
set -- the sum-product/realizability question, unresolved), or (b) exact
computation at n large enough for bundling (n in the hundreds+ with B~e^{n^a}),
far beyond CBC/brute force. The problem is open in both directions; no honest lean
survives scrutiny.


---

## 'Work backwards' attempt: it IS the turnpike problem (named connection)

Tried solving by working backwards (inverse reconstruction) rather than forward
search (work_backwards.py): start from the required difference multiset, reconstruct
the generating set S. Result: same min|S| as forward search (realizing a prescribed
difference set is the hard part; backward doesn't dodge it).

KEY connection: this backward direction IS the TURNPIKE PROBLEM (a.k.a. beltway /
partial digest problem): reconstruct a point set from its pairwise differences.
It is a studied inverse problem, hard in general (no known poly algorithm). So our
open crux -- 'is a divisibility-covering set realizable as a balanced difference
set' -- is literally a turnpike/partial-digest realizability question. This is a
genuine reframing: the UW realizability crux connects to the turnpike literature.

Meta-conclusion (all three directions hit the same wall):
- FORWARD (search S): explodes in the bundled regime (large n, B~e^{n^a}).
- BACKWARD (reconstruct S from differences): turnpike, hard.
- CHECK-ONLY: verifying needs elements up to e^{n^a}, uncheckable.
There is no computation-only shortcut; the difficulty is intrinsic, which is why
UW at fixed alpha is genuinely open. The problem routes through turnpike-
realizability in the bundled regime no matter the direction of attack.

Durable takeaways for a specialist handoff:
- PROVEN: 2beta+alpha>=1 (covering_lower_bound.pdf, discriminant proof).
- OPEN crux: realizability of a divisibility-covering set of (n/2,n] as a balanced
  difference set at the counting floor, in the bundled regime = a turnpike/partial-
  digest feasibility question with a sum-product obstruction (additive economy vs
  multiplicative richness).
- Four artifacts to AVOID (all caught here): vertex-log false proof; degenerate
  all-zeros construction; CBC-timeout-as-infeasible; small-n/no-bundling regime
  mismatch. Any future attack must reach the bundled regime to be meaningful.


---

## BUG in the 'work backwards' script -- turnpike claim RETRACTED

Audited work_backwards.py. Bug: minimal_covering_D + turnpike_min_S required
S-S to CONTAIN the target values (difference EQUALS t), instead of the real
covering condition (some difference DIVISIBLE by t; any multiple qualifies). This
solves a strictly HARDER problem and inflated min|S|.

Corrected (work_backwards_fixed.py): real-condition min-K = 5,6,6,7 for n=16,20,24,28
vs the buggy script's 6,7,7. The buggy numbers were higher because of the wrong
(exact-difference) condition.

Two corrections to prior claims:
1. 'Backward gives the same answer as forward' -- FALSE as stated. The buggy
   backward gave WORSE answers; corrected, there is no separate 'backward' problem
   (realizing the covering is one problem).
2. 'Our crux IS literally the turnpike problem' -- RETRACTED/overstated. Turnpike
   is EXACT-difference-multiset reconstruction; that is the stricter WRONG condition
   the bug imposed. Our real problem (divides, not equals) has SLACK turnpike lacks,
   so it is RELATED TO BUT EASIER THAN turnpike, not equal to it.

Corrected meta-status unchanged in essence: only PROVEN result is 2beta+alpha>=1;
the barrier vs UW is open; small-n/wrong-regime computation cannot probe it. The
'no computation shortcut' conclusion still holds, but the specific turnpike
identification was a bug artifact and should not be relied on. (Fifth artifact
caught this session -- the pattern of small-case/framing errors is itself the
main empirical lesson: every crisp claim here needs an explicit audit.)


---

## New-model attempt: honest negative (the abstraction can't dodge the sum-product theorem)

Tried to build a genuinely new model coupling additive structure of S with
multiplicative richness of S-S into one functional (covering energy E, second
moment E2, additive energy E+), to 'solve abstractly' (new_model.py,
model_stresstest.py).

Findings:
- Real coupling observed: covering-fraction inversely tracks additive energy
  (AP: E+/K^2=20, covers 0%; random: E+/K^2=2, covers 95%). But this IS the
  sum-product principle restated in our variables -- NOT a new law.
- The 'decisive test' (does low-E+ set cover at the counting floor?) returned
  'no' (7/21 at n=200) -- but this is the SIXTH regime artifact: it was run at
  polynomial magnitude M=n^1.5 where bundling is impossible, so it measures the
  no-bundling regime, not the model's obstruction. It decides nothing.

Honest conclusion on 'new model to solve abstractly': NO. Every framework we can
write (covering energy, coupled additive-mult functional, discriminant model,
difference-set realizability) bottoms out at the SAME inequality: can a set be
additively small while its difference set is multiplicatively rich? That is a
genuine OPEN problem (quantitative sum-product for difference sets). Renaming it
in a new abstraction does not make it solvable; a model that 'solves it abstractly'
would have to CONTAIN a new sum-product theorem as its engine -- and any such model
I could write here would smuggle the hard part into an unproven axiom. The honest
move is to NOT present a circular framework.

Net: the problem's difficulty is irreducible to notation. The real open kernel is
a quantitative sum-product / multiplicative-energy bound on difference sets. That
is a research-level analytic number theory / additive combinatorics problem, not
something a new model built here resolves. Sixth artifact caught reinforces: this
environment cannot reach the regime where the question lives.


---

## Literature connection: the 2025-26 sum-product breakthroughs (directly relevant)

Searched current literature for new sum-product theorems. Found two directly
load-bearing recent results (post-cutoff), read in full:

**1. Bloom-Sawin-Schildkraut-Zhelezov, 'The sum-product conjecture is false for
real numbers' (arXiv:2605.28781, May 2026).** Constructs A in totally real number
fields of GROWING degree (d ~ log|A|) with max(|A+A|,|AA|) <= |A|^{2-c}. Mechanism:
A=GP, G a box in the UNIT LATTICE (multiplicative structure, small product set),
P a box of algebraic integers (additive structure, small sum set). CRUCIAL caveat
(their own): needs degree -> infinity; sum-product 'may still be true in number
fields of bounded degree, and in particular the original setting of Z'.

**2. Agrawal-Bloom-Petridis (arXiv:2512.04931, Dec 2025) + Hanson-Rudnev-Shkredov-
Zhelezov (Compositio 2025).** For A in Z with every element having O(1) prime
factors, max(|A+A|,|AA|) >= |A|^{12/7-o(1)} (resp. 5/3). Sum-product HOLDS STRONGLY
in Z under bounded-prime-factors.

**What this means for UW (honest, double-edged):**
- Our problem is in Z, where sum-product survives -> supports the barrier INTUITION.
- BUT our differences have MANY prime factors (omega ~ n^alpha/ln n, growing), NOT
  O(1). The strong Z bounds (12/7, 5/3) require FEW prime factors -- exactly the
  property our differences VIOLATE. So those theorems do NOT apply to our object.
- The growing-degree escape hatch that BREAKS sum-product (Bloom et al.) is POWERED
  BY high-rank multiplicative structure / many prime factors -- precisely what our
  differences have. So our regime is closer to where sum-product CAN FAIL.

**Consequence (this reframes the attack).** The UW-relevant question is now sharply
a KNOWN open front: can a set S of integers have its DIFFERENCE SET made of numbers
each with ~n^alpha/ln n large prime factors, while S stays additively small (K
elements)? The Bloom-Sawin-Schildkraut-Zhelezov toolkit (unit lattices, growing-
degree number fields, G*P constructions) is EXACTLY a method for building sets that
are simultaneously additively and multiplicatively structured WHEN many prime
factors are allowed -- our regime. This is the first concrete CONSTRUCTION technique
that could plausibly build a UW solution (PRO-UW), not just probe it. It is also a
live, fast-moving area (multiple 2026 papers), so the needed sum-product input may
appear or may already be extractable.

**Net update:** UW's fate hinges on a question adjacent to the CURRENT sum-product
research frontier, and the recent number-field construction methods lean toward
'additive+multiplicative structure IS achievable with many prime factors' -- i.e.
mildly PRO-UW / anti-barrier, OR at least 'not settled by classical sum-product'.
The honest handoff: a specialist should look at whether the Bloom-Sawin-Schildkraut-
Zhelezov GP/unit-lattice construction, reduced to Z (their finite-field/p-adic
variants show reductions exist), can realize a divisibility-covering difference set
at the counting floor. That is the sharpest, most current, and most promising lead
the whole investigation has produced -- and it is genuinely new (post-dates all
prior work here).


---

## Testing the Bloom et al. GP construction: naive Z analogues untestable in the right regime

Tried to test whether the Bloom-Sawin-Schildkraut-Zhelezov GP (multiplicative x
additive) construction helps realize the covering (gp_construction_test.py,
dense_mult_test.py).

Results:
- Naive GP with SPARSE geometric G: covers WORSE than random (0.98,0.94,0.91 vs
  1.00). But this is the known-inadequate Balog-Wooley version -- sparse G is
  exactly what Bloom et al. FIXED with a dense unit-lattice box (no simple Z
  analogue).
- DENSE multiplicative (smooth numbers) G: covers 1.00 = random. No improvement,
  because there is nothing to improve: in the accessible regime random ALREADY
  covers perfectly (each large prime hit w.p. ~K^2/p).

Honest conclusion: the covering problem needs NO special structure in the
accessible regime -- GP, smooth, random all cover equally (100%). So this
environment CANNOT test the Bloom et al. construction's actual content, because
its content is in the BUNDLED regime (each difference = product of ~n^alpha/ln n
large primes), which needs elements up to e^{n^alpha} -- computationally out of
reach (same wall as always). The unit-lattice construction is BUILT for exactly
the additive+multiplicative regime we need, but verifying it realizes the bundled
counting floor requires carrying out the actual number-field construction
symbolically/analytically, not a search.

Net: 'test it out' gave a clean negative on the NAIVE Z analogues and a clean
statement of WHY the real construction is untestable here. The lead remains valid
and is the sharpest one -- but it is a THEORY/number-field-construction lead, not
a computational one. A specialist would need to instantiate the BSSZ unit-lattice
box in a totally real field of degree ~n^alpha, reduce to Z via a split prime
(their Fp/p-adic variants show the reduction works), and check whether the
resulting integer difference set covers (n/2,n] at |S|=n^{(1-alpha)/2}. That is a
concrete research program, now fully specified, and genuinely beyond this
environment.


---

## Perfect squares: a real but constant-factor bundling aid (this session)

Tested Eric's perfect-squares idea: S={a_i^2}, so differences factor as
a_i^2-a_j^2=(a_i-a_j)(a_i+a_j) -- two independent factors, each a chance to catch
a prime in (n/2,n]. (squares_test.py, higher_powers_test.py)

Findings:
- Coverage at matched K: squares = generic = 100% (saturated accessible regime,
  uninformative as always).
- BUNDLING (the real test): squared differences carry ~1.5x MORE large primes per
  difference than generic differences of the same magnitude (0.184 vs 0.124, etc.,
  stable ~1.5x across n). GENUINE structural effect -- the (a-b)(a+b) factorization
  bundles large primes more efficiently. First construction idea that measurably
  moves the bundling in the RIGHT direction via a real mechanism.
- Does it COMPOUND with higher powers a^k-b^k? NO. Bundling PEAKS at k=2 (0.16-0.18)
  and DROPS for k>=3 (k=3: 0.09, k=6: ~0). Reason: to stay in budget, roots shrink
  like B^{1/k}, so higher-power differences collapse to a tiny constrained range and
  the extra factors are small. k=2 is the sweet spot: both factors ~sqrt(B),
  independent.

Honest verdict: squares give a REAL but CONSTANT-FACTOR (~1.5x) bundling
improvement. A constant does not change the EXPONENT, so squares alone do NOT reach
the bundled counting floor -- they make UW a constant-factor easier, not
asymptotically achievable. NOT overstated: it's the best CONSTRUCTIVE signal found
here, and it connects to the number-field lead -- the Bloom et al. construction is
'algebraic factoring via unit lattices taken to the extreme', and squares are the
simplest instance (k=2) of the same 'make differences factor -> bundle primes'
principle. Squares show the principle WORKS at smallest scale; whether the
number-field version scales it from constant-factor to full-exponent is the open
question we cannot test here.

Net: perfect squares = a genuine, mechanism-backed constant-factor aid and a
conceptual bridge to the BSSZ number-field construction (both are 'factored
differences'). Encouraging for the PRO-UW / constructive direction, but not itself
a solution. The scalable version lives in the number-field regime, still out of
computational reach.


---

## Cubes and factorials: both fail, and WHY sharpens the squares result

Tested Eric's follow-ups (cubes_factorials_test.py):

**Cubes (and higher-factor forms): NO gain.** a^3-b^3=(a-b)(a^2+ab+b^2) bundles at
0.095-0.102 ~ GENERIC (0.10), far below squares (0.16-0.21). a^6-b^6 (4 factors):
~0. Reason: to stay in budget, cube roots shrink like B^{1/3}, so a-b is tiny
(rarely >n/2) and only ONE factor (the quadratic) is large -> effectively one
useful factor -> generic bundling. Squares are UNIQUELY good because (a-b)(a+b)
has BOTH factors ~sqrt(B): two large INDEPENDENT shots. The factorization helps
only when it yields MULTIPLE LARGE factors, which the magnitude budget permits
ONLY at k=2.

**Factorials: structurally USELESS for large-prime covering.** A prime p>n/2
divides m! only if m>=p; but m!<=budget forces m<=~11, so NO prime in (n/2,n]
divides any in-range factorial. Factorials are smooth in SMALL primes only --
exactly the wrong range (our targets are LARGE primes).

**Why this sharpens (not just adds to) the squares finding.** The winning
construction needs DIFFERENCES THAT FACTOR INTO MANY LARGE INDEPENDENT PIECES
SIMULTANEOUSLY. Squares give exactly TWO (the max Z's magnitude budget allows);
cubes/higher collapse to one; factorials give zero large factors. This is
PRECISELY what the Bloom-Sawin-Schildkraut-Zhelezov number-field construction
achieves that Z cannot: the unit-lattice / totally-real-field structure of degree
d produces differences with MANY large algebraic factors at once, because the
field has d dimensions of 'room' vs Z's one. The squares/cubes/factorials sweep
shows FROM THE INSIDE why plain Z tops out at a constant factor (max 2 large
factors) and why the number field (degree ~n^alpha) is the natural place the
EXPONENT (n^alpha/ln n large factors per difference) could be reached.

Net: cubes and factorials are clean negatives, but they CONFIRM the mechanism and
CONFIRM that the number-field construction is the right place to scale it. Squares
remain the unique Z sweet spot (constant factor); the exponent-scaling version is
inherently multi-dimensional (number fields), consistent with the BSSZ lead.


---

## Fractal / digit-restricted / 'log 10' sets: negative, and it completes the map

Tested self-similar/digit-restricted (Cantor-like) and hierarchical sets, plus the
'log 10' base-digit reading (fractal_test.py), using the bundling metric.

Result: all cluster near GENERIC (0.09-0.12) and well below SQUARES (0.18):
Cantor-b3 ~0.10, Cantor-b10 ~0.11, hierarchical ~0.09, vs generic 0.087, squares
0.18. Fractal structure does NOT help bundling.

Why (a real principle): fractal/digit-restricted sets control ADDITIVE structure
(a Cantor set has a small, structured difference SET). But covering needs each
difference MULTIPLICATIVELY rich (divisible by large primes). Additive control and
multiplicative richness are the sum-product ANTAGONISTS -- so maximizing additive
structure (what 'fractal' does) pushes the WRONG way for covering. ('log 10' as
geometric element-spacing = the sparse-geometric G already shown to lose.)

This COMPLETES the construction-family map from Eric's idea sweep:
- SQUARES: WIN (+multiplicative structure on the DIFFERENCES via factoring) -- the
  one thing covering needs. Constant factor (~2x).
- Cubes/higher powers: no gain (budget collapses extra factors to 1 large factor).
- Factorials: useless (smooth in SMALL primes; targets are LARGE primes).
- Fractal/digit-restricted: no gain (adds ADDITIVE structure to the SET -- wrong
  axis; that's the sum-product antagonist of what's needed).

Unified lesson: the ONLY thing that helps covering is making DIFFERENCES FACTOR
INTO LARGE PIECES. Every other structure (additive/fractal, small-prime-smooth,
higher-power) is neutral or counterproductive. Squares are the Z ceiling (2 large
factors); scaling to the exponent (many large factors/difference) is inherently
multi-dimensional -> the number-field (BSSZ) construction, still the sole lead for
the exponent-scaling version and untestable here. The construction search is now
SATURATED: the mechanism is identified, the Z ceiling is mapped, and the only
remaining route is the number-field one.


---

## Our version of the theorem: a conditional lattice-CRT construction (this session)

Built our own adaptation of the BSSZ unit-lattice construction to the covering
problem, stress-testing each step (our_theorem_attempt.py, required_shortness.py,
written up in our_construction_theorem.md).

Construction (lattice-CRT): (1) pack primes into K^2/2 pairs [proven]; (2) solve
s_i ≡ s_j mod m_ij -- a lattice L in Z^K of covolume ~ Q ~ e^{n/2}; (3) need K
distinct coords <= e^{n^alpha}.

STRESS-TEST caught the flaw honestly: Minkowski AVERAGE gives coords ~ e^{n/(2K)}
= e^{n^{(1+alpha)/2}/2}, exceeding budget e^{n^alpha} by a factor GROWING
polynomially (9x,58x,316x at alpha=0.3). So generic lattice geometry FAILS -- this
is the correct quantified version of why naive/vertex-log constructions fail. (Did
NOT mis-declare 'barrier holds': the average bound is not a lower bound; special
lattices can beat it.)

The BSSZ ingredient supplies exactly the missing shortness: bounded-root-disc
fields (Martinet towers) have unit lattices with O(1)-per-dimension vectors --
shorter than Minkowski-average by the needed growing factor -- and the required
dimension d~K~n^{(1-alpha)/2} is AVAILABLE. So magnitudes/dimensions ALL FIT.

CONDITIONAL THEOREM: IF our pair-congruence system embeds into such a unit lattice
preserving O(1)-per-dim shortness (=> K distinct integers <= e^{n^alpha}), THEN UW
holds at alpha (barrier false, 2beta+alpha tight).

Isolated open hypothesis (the honest crux): a LATTICE-DESCENT question -- can
rational-prime congruences be realized by short unit-lattice vectors descending to
SMALL integers? NOT a magnitude gap (fits); a STRUCTURAL one. This is exactly the
descent-to-Z step BSSZ leave OPEN (they get R, p-adic, finite fields; Z open).

Net: we did NOT prove UW, but we produced a precise CONDITIONAL theorem reducing
UW (fixed alpha) to a specific, named, frontier-adjacent lattice-embedding
question, with all magnitudes verified to fit and the sole gap isolated as the
same descent obstacle open in the 2026 source paper. This is the strongest and
most honest theoretical output of the investigation: a real reduction, not a
disguised restatement. The construction search (squares etc.) and this theorem
agree: the exponent-scaling mechanism is multi-dimensional (number fields), and
the open kernel is descent-to-Z.


---

## Attacking the descent lemma: it is EQUIVALENT to UW, not easier (this session)

Recognized the descent lemma as a congruence-labeling / lattice-box problem and
attacked it. Chain of findings, each checked:

1. Incident-log 'obstruction' (a slot tied to many large primes needs magnitude
   e^{incident}) = the VERTEX-LOG FALLACY again. Exact search (descent_exact.py)
   showed small distinct solutions EXIST below the Minkowski average -> sharing is
   real. Caught before recording as barrier (would have been ~7th artifact).
2. Scaling test (descent_scaling.py): the sharing 'saving' vs average GROWS with K
   (1.27->2.55 for K=4..8) -- looked pro-UW. BUT skeptical check needed:
3. Large-prime / star-graph analysis (descent_honest.py): sharing has a REAL
   structural limit -- a slot incident to many large primes IS forced large
   (star: center tied to leaves by big primes forces leaves to be multiples).
   The flat small-prime actual-log was partly distinctness-floor artifact.
4. The true invariant (descent_crux.py): the descent lemma = 'does the covolume-Q
   congruence lattice contain a point in box [0,B]^K with distinct coords?'
   Box vol = e^{K n^alpha}; covol = Q = e^{Theta(n)}. 'box nonempty' <=> K*logB >=
   logQ <=> n^beta*n^alpha >= n <=> alpha+beta>=1 (the BARRIER line). At the
   counting floor 2beta+alpha=1 we have alpha+beta=(1+alpha)/2<1, so the generic
   box is EMPTY (ratio K*n^a/logQ = 0.017-0.045, verified <1 and shrinking).

VERDICT: a generic lattice fails; UW requires a SPECIAL lattice whose points
CLUSTER in the tiny box -- which is exactly the bounded-root-disc/unit-lattice
property AND is the entire content of UW. The descent lemma, fully unfolded, is
EQUIVALENT to UW, not a lighter sub-lemma. We went in a precise, honest circle.

CONSEQUENCE (corrects our own conditional theorem): the 'isolated hypothesis' in
our_construction_theorem.md is NOT a smaller lemma -- it carries the full weight of
UW. A specialist should NOT treat the descent lemma as an easier step to prove; it
is a faithful REFORMULATION of UW in lattice-clustering language. The genuine value
of the reduction is the CHANGE OF LANGUAGE: UW at fixed alpha <=> a bounded-root-
discriminant lattice clusters its points in an exponentially-small box. That
connects UW to the exact machinery (Martinet towers, unit-lattice clustering) that
BSSZ use -- so the RIGHT question is whether BSSZ-style clustering can be made to
respect our divisibility constraints, which is genuinely open and frontier-level.

Net honest status after the attack: UW remains open both directions. Only proven
result: 2beta+alpha>=1. The attack did NOT crack it but DID something worthwhile --
it proved the descent reduction is faithful (equivalent, not easier), which saves
future effort from chasing the descent lemma as a shortcut. The barrier was NOT
established (the incident-log route was again an artifact); the pro-UW route
(sharing scales) is real but capped by lattice-clustering, which is exactly UW.


---

## AUDIT of the descent-lemma scripts: one imprecision fixed, verdict sharpened

Checked the load-bearing descent scripts for bugs (descent_crux_check.py,
descent_audit2.py).

CORRECTION (imprecision, now fixed above): I wrote the box-emptiness was 'the same
2beta+alpha>=1 boundary'. WRONG. The correct identity:
  - 'generic lattice box nonempty' <=> K*logB >= logQ <=> alpha+beta >= 1
    = the BARRIER line (NOT the proven 2beta+alpha>=1 line).
  - proven bound 2beta+alpha>=1 and generic-box bound alpha+beta>=1 are DIFFERENT.
  - At the counting floor (2beta+alpha=1): alpha+beta=(1+alpha)/2<1, so generic box
    is EMPTY (ratio 0.017-0.045, verified <1, shrinking as n grows).
So the descent lemma = 'a SPECIAL lattice clusters points into a box where a
GENERIC lattice has none', and that clustering is EXACTLY the gap between the
proven line (2beta+alpha>=1) and the barrier line (alpha+beta>=1). This is a
sharper, corrected 'descent <=> UW': the reformulation captures precisely the
exponent gap in question. Verdict (descent equivalent to UW, not easier) STANDS.

VERIFIED SOUND: descent_exact.py's 'small solutions beat Minkowski average' is not
biased by the search cap Bcap=sqrt(Q) -- a cap causes only FALSE NEGATIVES (missing
high solutions), never false positives. Found solutions below the cap are real, so
'sharing is real' holds.

Net: no computational bug changed a conclusion; one imprecise boundary label was
corrected (2beta+alpha -> alpha+beta for the generic-box line), which SHARPENS the
reformulation. The equivalence verdict and the 'sharing is real (but capped by
clustering=UW)' both survive audit.


---

## Optimization attempt on the descent solver: failed as opt, informative as evidence

Tried to optimize the exponential backtracking descent solver using the coprime-
moduli structure (CRT decoupling + spanning-tree propagation) to reach large K
(descent_optimized.py, descent_opt2.py).

Result: the greedy tree/CRT-propagation solver is CORRECT only on acyclic
constraint graphs; on CYCLIC graphs (the generic case) it returns false None --
because propagated values almost never satisfy the cycle-closing congruence and no
small lift fixes it. Verified: it agrees with brute force on the two tree cases
(opt>=brute) but fails on all cyclic cases.

Honest outcome: the optimization FAILED (greedy propagation is fundamentally wrong
for coupled/cyclic constraints), but the failure is INFORMATIVE -- it's concrete
evidence for the 'descent ≡ UW, not easier' verdict: the descent problem resists
the natural fast algorithm precisely because its cycles are genuinely coupled
constraints. A correct fast solver would require real simultaneous integer CRT /
lattice reduction with cycle-consistency (i.e. implementing the lattice machinery
itself), not a cheap greedy pass -- more than an optimization, and exactly the hard
kernel. Did not fake a solver; brute force remains the only trustworthy exact
method here (caps ~K=7-8).

Bug-audit summary (this checking pass):
- descent_crux.py: boundary-label imprecision FIXED (generic-box-empty <=>
  alpha+beta>=1, the barrier line, NOT 2beta+alpha>=1). Verdict sharpened, stands.
- descent_exact.py 'beats average': VERIFIED sound (search cap causes only false
  negatives, not false positives).
- optimization: greedy solver BUGGY on cycles; retracted as a solver, kept as
  evidence. Brute force (validated) stays the exact oracle.


---

## Re-reading the UW paper (arXiv:2511.10851): three sharpenings for our tools

Read the source paper's core (Defn 3.1 n-divisor property, Conj 3.2 (alpha,beta)-
Divisor Conjecture, framework Thm 2.1). Three corrections/sharpenings:

**1. Target is [n], hard kernel is primes in (n/2,n] -- confirmed correct.** The
conjecture covers ALL i in {1,...,n} (n-divisor property). Our reduction to primes
in (n/2,n] is the right hard core. The paper's OWN lower bound matches ours
exactly: product of primes <n is exp(n), so some element has magnitude
exp(n)^{1/m} -- this is their elementary version of our discriminant 2beta+alpha>=1.
Good: we reproduced their lower bound (ours via discriminant is an independent
derivation of the same bound).

**2. KEY sharpening: A is an ASYMMETRIC difference set S-T, not symmetric S-S.**
Conj 3.2 demands A={s-t : s in S, t in T} with TWO SEPARATE sets. Most of our
construction tests used symmetric S-S. The asymmetric S-T structure:
  - has |S||T| ~ n^{2beta} differences from 2n^beta elements (richer);
  - is EXACTLY the Balog-Wooley / BSSZ G*P setup: let S carry one structure
    (e.g. multiplicative/unit-lattice) and T the other (additive/box).
This is a real fidelity fix AND favors the BSSZ construction: their A=GP is a
PRODUCT, but the covering needs s-t, so the right adaptation is S=G-part,
T=box-part with s-t bundling primes. Our tools should test S-T (two sets), not
S-S. TODO for future: re-run squares/GP bundling with asymmetric S,T -- the two-set
freedom may beat the ~1.5x constant squares gave (squares were tested as S-S).

**3. 'Structured' assumption => CONSTRUCTIVE solution required.** The speedup needs
S,T structured (efficiently computable), not arbitrary existence. Validates our
focus on explicit constructions (BSSZ-style) over pure counting/probabilistic
existence. An existence proof alone would NOT give the algorithm; the conjecture's
payoff needs explicit S,T. So the BSSZ explicit-construction route is not just one
option -- it's the KIND of answer the application demands.

Net sharpening: (a) our lower bound matches theirs (confidence); (b) switch tools
to ASYMMETRIC S-T, which is both faithful and pro-BSSZ (two sets = G and box
separately) -- a concrete, testable improvement over the symmetric tests; (c)
constructive is mandatory, confirming the construction program is the right track,
not a detour.


---

## Acted on sharpening #2: asymmetric S-T bundling test (fidelity fix)

Re-ran the bundling test with ASYMMETRIC S-T (two sets) per the actual conjecture,
vs the symmetric S-S we'd used (asymmetric_test.py).

Result: asymmetric squares S-T marginally beats symmetric (0.182 vs 0.166 at
n=2000; ~tie at n=1000). The crude G*box BSSZ-mock (0.116-0.126) does NOT beat
squares -- consistent with the known limitation (real multiplicative power needs
unit lattices, not a Z mock-up). So the two-set freedom gives a MARGINAL, not
qualitative, improvement in the accessible regime.

Honest value: this was a FIDELITY FIX, not a new win. Our tools now match the
conjecture's asymmetric S-T structure (previously symmetric S-S). The conclusion is
unchanged and consistent: asymmetric is the correct framing and marginally helps,
but exponent-scaling still needs the number-field construction that is untestable
here. The squares mechanism (constant-factor) remains the Z ceiling whether
symmetric or asymmetric.

Updated tool-fidelity status: all construction/bundling tools should use S-T; the
BSSZ adaptation is S = (multiplicative/unit-lattice part), T = (additive box), with
s-t the covering difference. This is now the precise, paper-faithful target for any
future constructive attempt.


---

## Future attempts run: asymmetric S-T has REAL magnitude slack (fallacy caught again)

Ran the flagged future attempts: build the paper-faithful bipartite S-T covering
construction and test whether it escapes the magnitude wall (future_attempt1/2/3.py).

Chain:
1. Naive greedy S-T (attempt1): degenerate (collapsed T to 1 element, beta~0.6).
   Bad construction, discarded.
2. Balanced bipartite analysis (attempt2): 's_i forced mod row-product ~ e^{logQ/K}'
   -- SAME wall as one-sided, ratio ->1. LOOKED like S-T doesn't help.
3. EXACT check (attempt3) -- guarding against the vertex-log fallacy: does choosing
   the free t_j pull s_i below the row-product? YES. Exact min-magnitude log is
   BELOW both 0.5logQ and the row-product line, gap GROWING (K=3,9primes: exact 4.06
   vs rowprod 7.30). The 'row-product forcing' was the FALLACY AGAIN (4th time). The
   two-sided freedom (choose t_j AND s_i) genuinely beats the naive bound.

Honest finding: the asymmetric S-T formulation has REAL magnitude slack the
one-sided/symmetric analysis missed -- exact-confirmed, not fallacy. So the paper's
S-T structure is not merely a fidelity fix; it is GENUINELY MORE FAVORABLE to a
construction than the symmetric S-S we'd been analyzing. The bipartite (two free
variable sets) coupling is weaker than the one-sided descent lattice.

Discipline in both directions: 'beats the row-product bound' is NOT 'reaches budget
e^{n^alpha}'. Data is K<=3 (tiny); beating a naive bound != meeting the target.
Whether the bipartite slack SCALES to the budget is the open question, still living
in the number-field regime.

Durable lesson (now 4x): EVERY naive magnitude lower bound in this problem
(vertex-log, incident-log, row-product) has been defeated by residue-sharing on
exact check. The true obstruction is ONLY the deep clustering/descent question
(= UW), never the surface counting bounds. Any future 'barrier' claim from a
forcing/counting argument should be assumed FALSE until exact-checked.

Net update: mildly PRO-UW / pro-construction. The asymmetric S-T structure is the
right target AND has exact-confirmed slack beyond the one-sided analysis. The
construction program should proceed with bipartite S-T in a number field (S from
unit lattice, T additive box), which is now the single sharpest, paper-faithful,
frontier-connected open lead. Still not provable here (number-field regime), but
the direction is confirmed favorable, not blocked.


---

## Bug audit + golden ratio / near-squares tests (this session)

BUG AUDIT of the S-T slack finding:
- future_attempt3.py had a distinctness bug: it forced GLOBAL distinctness across
  S union T, but the problem only needs distinct WITHIN S and WITHIN T. Fixed
  (future_attempt3_fixed.py).
- Degeneracy check (future_attempt4.py) found the K=2 'small solution' was PARTLY
  DEGENERATE: S=[0,7],T=[10,7] has s_1=t_1=7 -> zero difference 'covering' a prime
  invalidly (the all-zeros artifact, 5th of its type). K=3 solution was VALID.
- Clean re-test (future_attempt5.py) with nonzero-diff enforced: valid bipartite
  covers STILL beat the row-product bound logQ/K (log-min 2.48/4.45/4.06 vs
  3.53/6.23/7.30). So 'S-T has real magnitude slack' SURVIVES the audit -- it was
  contaminated at K=2 but not created by the artifact. Corrected status: real, but
  messier than first stated, and still K<=3 tiny.

GOLDEN RATIO test (golden_squares_test.py): phi appears in BSSZ Lemma 3.4 (unit
separation), so worth testing. Result: NO help. Fibonacci sets bundle 0.06-0.08
(WORSE than generic 0.11); Beatty floor(k*phi) ~0. Reason: Fibonacci/Beatty have
ADDITIVE structure (near-AP, small difference sets) -- the sum-product antagonist of
covering. phi's BSSZ role is archimedean unit-separation, a DIFFERENT mechanism than
integer prime-divisibility. False lead (worth ruling out).

NEAR-SQUARES test (sharpening): a*b with a,b close bundles 0.10 ~ GENERIC, NOT like
squares (0.17-0.19). KEY: the squares mechanism is NOT 'difference factors into two
big pieces' -- it's the EXACT ALGEBRAIC IDENTITY a^2-b^2=(a-b)(a+b) with two
determined independent factors. A near-square difference a*b-c*d is a generic number
(no identity). So squares are MORE special than credited: the win is the difference-
of-squares identity specifically. Explains why cubes (worse identity) and near-
squares (no identity) both fail -- squares are a genuine algebraic sweet spot.

Net: (a) S-T slack finding survives audit (real, K<=3, contamination cleaned);
(b) golden ratio does NOT help (additive-structure antagonist; phi's BSSZ role is
unrelated); (c) near-squares does NOT help, which SHARPENS the mechanism to 'the
a^2-b^2 identity specifically'. Squares remain the unique Z sweet spot; the
exponent-scaling is still the number-field regime. Construction search remains
saturated with squares as the Z ceiling.
