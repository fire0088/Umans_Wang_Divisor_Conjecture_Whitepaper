# uw_floor_check.py -- honest feasibility checker for the UW counting floor

## The question
For covering (n/2, n] by divisibility with a DISTINCT set S in [0,B]: is the true
minimum |S| as small as the counting floor K_floor? If yes at scale, 2b+a=1 is
tight (UW-favorable). If the true min-K is provably larger, the floor is
unreachable (barrier-favorable).

## Why trust this one
Earlier code mistook CBC "Not Solved" (a TIMEOUT) for "Infeasible" and thereby
manufactured a false "barrier holds" result. This tool fixes that:
- Reports Optimal / Infeasible / TIMEOUT explicitly and NEVER conflates them.
- Ships an independent BRUTE-FORCE oracle (fixes 0 in S WLOG, prunes by coverage)
  and uses it as ground truth; the ILP is only trusted where it agrees.
- `--selftest` verifies the ILP never CONTRADICTS brute force (timeouts allowed).
- Supports Gurobi (`--solver gurobi`) to push past where CBC times out.

**Rule:** "the floor is unreachable at n" is justified ONLY when the true min-K
(from brute force, or a PROVEN ILP Infeasible at K_floor) exceeds the floor -- a
timeout never justifies it.

## Usage
    python uw_floor_check.py --selftest                 # trust check (do this first)
    python uw_floor_check.py --ns 24 30 40              # sweep, brute + ILP
    python uw_floor_check.py --n 40 --brute             # brute force only
    python uw_floor_check.py --n 40 --solver gurobi --time-limit 120
    python uw_floor_check.py --n 30 --B 90 --kmax 12    # custom magnitude / K range

## Reading the output
Per-K status: Optimal = feasible set exists; Infeasible = PROVEN none; Timeout =
unknown (not infeasible!). The VERDICT line uses brute force when available.

Findings so far (small n, brute force = ground truth):
    n=24: true min-K = 6 = floor  -> floor REACHABLE (UW-favorable)
    n=30: true min-K = 7 > floor 6 -> floor UNREACHABLE at this n (barrier-favorable)
Mixed at tiny n -- genuinely undecided; needs larger n (Gurobi, or brute with
more time) to see the trend. Brute force is exponential, so it fades ~n=40-50;
Gurobi is the way to go higher.

## Notes
- Brute force fixes 0 in S (covering depends only on differences, translation-
  invariant) and prunes; it returns None if it exceeds its node budget (raise it
  in code for larger n).
- The counting floor uses alpha only to set primes-per-pair; the covering
  feasibility itself is magnitude-bounded by B (default 2n), independent of alpha.

Author: Eric Schultz & Claude (Anthropic), July 2026.
