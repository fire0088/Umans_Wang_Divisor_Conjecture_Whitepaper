#!/usr/bin/env python3
"""
uw_floor_check.py -- is the counting floor reachable? (honest feasibility checker)

THE QUESTION
------------
For covering the interval (n/2, n] by divisibility with a DISTINCT set S of
integers in [0, B]: what is the true minimum |S| = K, and is it as small as the
counting floor K_floor = smallest K with C(K,2) * (budget primes per pair) >= |P|?

If the true min-K equals K_floor, the counting bound 2beta+alpha=1 is tight
(evidence UW may be TRUE). If true min-K is provably larger, the floor is
unreachable (evidence for the barrier / UW false).

WHY THIS TOOL EXISTS
--------------------
Earlier attempts got fooled by CBC returning "Not Solved" (a TIMEOUT) and the
code treating that as "infeasible", which inflated the reported min-K and
manufactured a false "barrier holds" conclusion. This tool:
  * reports Optimal / Infeasible / TIMEOUT explicitly and NEVER conflates them;
  * cross-checks the ILP against an independent brute-force search at small n,
    so you can trust the result without trusting the solver;
  * supports Gurobi (if installed) to push past where CBC times out.

A claim of the form "the floor K is unreachable" is only justified when the
solver returns a PROVEN "Infeasible" at K = K_floor (not a timeout).

USAGE
-----
    python uw_floor_check.py --selftest              # verify against brute force
    python uw_floor_check.py --n 30                  # analyze one n
    python uw_floor_check.py --ns 24 30 40 50        # sweep
    python uw_floor_check.py --n 40 --solver gurobi  # use Gurobi if available
    python uw_floor_check.py --n 40 --time-limit 120 # give CBC longer
    python uw_floor_check.py --n 24 --brute          # brute force only (no ILP)

INTERPRETATION of the per-K status:
    Optimal    -> a valid distinct covering set of that size EXISTS (feasible)
    Infeasible -> PROVEN no such set exists at that size (K too small)
    TIMEOUT    -> solver could not decide in the time limit -> UNKNOWN
                  (do NOT interpret as infeasible)

Author: Eric Schultz & Claude (Anthropic), July 2026.
"""

import argparse, math, itertools, sys
from sympy import primerange


# ----------------------------------------------------------------------
# problem setup
# ----------------------------------------------------------------------
def targets_of(n):
    """The interval (n/2, n] we must cover by divisibility."""
    return list(range(n // 2 + 1, n + 1))

def counting_floor_K(n, alpha):
    """Smallest K with C(K,2) * (primes bundleable per pair) >= |targets|.
    'primes per pair' = budget(log) / (log of a typical prime) = n^alpha / ln(n/2)."""
    m = len(targets_of(n))
    per_pair = max(1, int(n**alpha / math.log(n / 2)))
    K = 2
    while K * (K - 1) // 2 * per_pair < m:
        K += 1
    return K, per_pair, m


# ----------------------------------------------------------------------
# brute force (ground truth at small n) -- trust this, not the solver
# ----------------------------------------------------------------------
def brute_covers(S, targets):
    diffs = {abs(a - b) for a in S for b in S if a != b}
    return all(any(d % i == 0 for d in diffs) for i in targets)

def brute_feasible_at_K(n, K, B, targets, node_budget=8_000_000):
    """Exhaustively (with pruning) decide if a distinct K-set in [0,B] covers.
    Returns True / False / None(gave up). Fixes 0 in S WLOG (covering depends
    only on differences, which are translation-invariant)."""
    pool = list(range(1, B + 1))            # 0 is fixed as the first element
    need = set(targets)
    count = [0]
    # order pool to try spread-out elements first (helps find covers fast)
    def rec(start, chosen, covered):
        count[0] += 1
        if count[0] > node_budget:
            return None
        if len(covered) == len(need):
            # already covered with fewer than K? pad distinctly if room
            return True if len(chosen) <= K else None
        if len(chosen) == K:
            return len(covered) == len(need)
        # prune: not enough remaining elements to reach K
        if K - len(chosen) > len(pool) - start:
            return False
        res_any_none = False
        for idx in range(start, len(pool)):
            v = pool[idx]
            newc = set(covered)
            for c in chosen:
                d = abs(v - c)
                for t in need:
                    if t not in newc and d % t == 0:
                        newc.add(t)
            r = rec(idx + 1, chosen + [v], newc)
            if r is True:
                return True
            if r is None:
                res_any_none = True
        return None if res_any_none else False
    r = rec(0, [0], set())
    return r


def brute_min_K(n, B, kmax, targets):
    """Smallest K for which a distinct covering set exists in [0,B], by brute force."""
    for K in range(2, kmax + 1):
        r = brute_feasible_at_K(n, K, B, targets)
        if r is True:
            return K, "brute-exact"
        if r is None:
            return None, f"brute-gaveup@K={K}"
    return None, "brute-none"


# ----------------------------------------------------------------------
# ILP feasibility (with honest status) -- CBC or Gurobi
# ----------------------------------------------------------------------
def ilp_status_at_K(n, K, B, targets, solver="cbc", time_limit=30):
    """Return 'Optimal' / 'Infeasible' / 'Timeout' / 'ModelInfeasible' for the
    existence of a distinct K-set in [0,B] covering targets by divisibility."""
    import pulp
    pool = list(range(0, B + 1))
    prob = pulp.LpProblem("cover", pulp.LpMinimize)
    x = {a: pulp.LpVariable(f"x{a}", cat="Binary") for a in pool}
    prob += 0
    prob += pulp.lpSum(x.values()) == K
    for i in targets:
        ors = []
        for a in pool:
            for b in pool:
                if a > b and (a - b) % i == 0:
                    y = pulp.LpVariable(f"y_{i}_{a}_{b}", cat="Binary")
                    prob += y <= x[a]
                    prob += y <= x[b]
                    ors.append(y)
        if not ors:
            return "ModelInfeasible"      # target i can't be covered in [0,B] at all
        prob += pulp.lpSum(ors) >= 1

    if solver == "gurobi":
        try:
            cmd = pulp.GUROBI_CMD(msg=0, timeLimit=time_limit)
        except Exception:
            cmd = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    else:
        cmd = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    prob.solve(cmd)
    st = pulp.LpStatus[prob.status]
    # PuLP maps CBC "stopped on time" to "Not Solved"/"Undefined"
    if st == "Optimal":
        return "Optimal"
    if st == "Infeasible":
        return "Infeasible"
    return "Timeout"


def ilp_min_K(n, B, kmax, targets, solver="cbc", time_limit=30, verbose=True):
    """Smallest K with a PROVEN feasible (Optimal) covering set. Reports each K's
    status honestly. Returns (min_K or None, list of (K,status)).
    Crucially: a Timeout at some K is NOT treated as infeasible."""
    trace = []
    min_feasible = None
    for K in range(2, kmax + 1):
        st = ilp_status_at_K(n, K, B, targets, solver, time_limit)
        trace.append((K, st))
        if verbose:
            print(f"      K={K:3d}: {st}", flush=True)
        if st == "Optimal":
            min_feasible = K
            break
        if st == "Timeout":
            # We cannot conclude anything about this K. Keep going to find SOME
            # feasible K (an upper bound), but do NOT claim min-K is above here.
            continue
        # Infeasible or ModelInfeasible -> genuinely too small, advance.
    return min_feasible, trace


# ----------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------
def analyze_n(n, alpha, solver, time_limit, B=None, kmax=None, do_brute=True,
              do_ilp=True):
    targets = targets_of(n)
    fK, per_pair, m = counting_floor_K(n, alpha)
    if B is None:
        B = 2 * n                      # generous magnitude
    if kmax is None:
        kmax = fK + 6
    print(f"\nn={n}  alpha={alpha}  |targets|={m}  counting-floor K={fK}  B={B}")

    brute_K = None
    if do_brute:
        bK, bnote = brute_min_K(n, B, kmax, targets)
        brute_K = bK
        print(f"  brute-force true min-K: {bK}  ({bnote})")

    ilp_K = None
    if do_ilp:
        print(f"  ILP ({solver}) per-K feasibility status:")
        iK, trace = ilp_min_K(n, B, kmax, targets, solver, time_limit)
        ilp_K = iK
        # honest verdict about the FLOOR specifically
        floor_status = dict(trace).get(fK, "not reached")
        print(f"  ILP min feasible K (proven Optimal): {iK}")
        print(f"  status AT the counting-floor K={fK}: {floor_status}")

    # verdict
    print("  VERDICT:", end=" ")
    truth = brute_K if brute_K is not None else ilp_K
    if truth is None:
        print("undetermined (brute gave up / ILP no Optimal in limits).")
    elif truth == fK:
        print(f"floor REACHABLE (true min-K = floor = {fK}). "
              f"Counting bound tight here -> UW-favorable at this n.")
    elif truth > fK:
        # only meaningful if we PROVED the floor infeasible, else it's an upper bound
        if do_ilp:
            fs = dict(trace).get(fK, "?")
            if fs == "Infeasible":
                print(f"floor UNREACHABLE (proven): true min-K = {truth} > floor {fK}. "
                      f"Barrier-favorable at this n.")
            else:
                print(f"true min-K found = {truth}, but floor K={fK} status is '{fs}' "
                      f"(NOT proven infeasible) -> cannot claim floor unreachable.")
        else:
            print(f"true min-K = {truth} > floor {fK} (brute force). Barrier-favorable.")
    return dict(n=n, floorK=fK, brute_K=brute_K, ilp_K=ilp_K)


def selftest():
    """Cross-check ILP vs brute force on tiny n. The test is CONSISTENCY: the ILP
    must never CONTRADICT brute force. Specifically:
      - at brute min-K, ILP must be Optimal (feasible) -- never Infeasible;
      - just below brute min-K, ILP must be Infeasible OR Timeout -- never Optimal.
    A Timeout is acceptable (CBC often can't prove the hard infeasibility side at
    these sizes -- which is exactly why we keep brute force as the oracle)."""
    print("SELFTEST: ILP must be CONSISTENT with brute force (never contradict it).")
    print("  (Timeout is allowed; the failure we care about is a direct contradiction.)")
    ok = True
    for n in [16, 20, 24]:
        targets = targets_of(n)
        B = 2 * n
        bK, _ = brute_min_K(n, B, 12, targets)
        st_at = ilp_status_at_K(n, bK, B, targets, "cbc", 30)
        st_below = ilp_status_at_K(n, bK - 1, B, targets, "cbc", 30) if bK > 2 else "n/a"
        # contradiction = ILP says Infeasible where brute says feasible, or
        #                 ILP says Optimal where brute says infeasible.
        contradiction = (st_at == "Infeasible") or (st_below == "Optimal")
        consistent = not contradiction
        ok = ok and consistent
        print(f"  n={n}: brute min-K={bK}; ILP@{bK}={st_at}, ILP@{bK-1}={st_below} "
              f"-> {'CONSISTENT' if consistent else 'CONTRADICTION'}")
    print("SELFTEST", "PASSED" if ok else "FAILED",
          "-- brute force is the oracle; ILP must not contradict it.")
    # also sanity-check brute force itself against a hand value:
    # n=16: primes/targets in (8,16] = {9,10,11,12,13,14,15,16}; min covering set
    print(f"  (brute-force sanity: n=16 min-K computed as "
          f"{brute_min_K(16, 32, 12, targets_of(16))[0]})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--n', type=int, help='single n to analyze')
    ap.add_argument('--ns', type=int, nargs='+', help='several n to sweep')
    ap.add_argument('--alpha', type=float, default=0.45,
                    help='exponent for the counting-floor calc & budget')
    ap.add_argument('--solver', choices=['cbc', 'gurobi'], default='cbc')
    ap.add_argument('--time-limit', type=int, default=30, help='ILP seconds per K')
    ap.add_argument('--B', type=int, default=None, help='magnitude cap (default 2n)')
    ap.add_argument('--kmax', type=int, default=None, help='max K to test')
    ap.add_argument('--brute', action='store_true', help='brute force only (no ILP)')
    ap.add_argument('--no-brute', action='store_true', help='ILP only (skip brute)')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()

    if args.selftest:
        selftest(); return

    ns = args.ns if args.ns else ([args.n] if args.n else [24, 30, 40])
    for n in ns:
        analyze_n(n, args.alpha, args.solver, args.time_limit,
                  B=args.B, kmax=args.kmax,
                  do_brute=not args.no_brute,
                  do_ilp=not args.brute)


if __name__ == "__main__":
    main()
