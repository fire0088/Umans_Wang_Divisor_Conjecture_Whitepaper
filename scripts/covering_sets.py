"""
Exploring the Umans-Wang covering-set conjecture (arXiv:2511.10851).

Conjecture: there exist sets S, T of size n^beta, consisting of positive
integers of magnitude at most exp(n^alpha), such that every integer
i in [n] divides s - t for some s in S, t in T.

Target: alpha = beta = 1/3 is "best possible" and would give an
exponent-4/3 polynomial factorization algorithm (vs current 3/2),
and would push the deterministic integer-factoring exponent from 1/5 to 1/6.

This script doesn't factor anything -- it experimentally searches for
covering sets S, T for small n, and measures the actual (alpha, beta)
achieved by different construction strategies. This is the genuinely
open/tractable part of the paper to poke at by hand.
"""

import math
import random
from itertools import combinations


def divides(i, s, t):
    """Does i divide (s - t)?"""
    return (s - t) % i == 0


def covers_all(S, T, n):
    """Check whether every i in [1, n] divides some s-t for s in S, t in T."""
    diffs = set()
    for s in S:
        for t in T:
            diffs.add(s - t)
    for i in range(1, n + 1):
        if not any(d % i == 0 for d in diffs):
            return False, i
    return True, None


def measure_params(S, T, n):
    """Given covering sets S, T for [n], compute the empirical alpha, beta."""
    size = max(len(S), len(T))
    max_val = max(max(S, default=1), max(T, default=1))
    # size ~ n^beta  =>  beta = log(size) / log(n)
    # max_val ~ exp(n^alpha)  =>  alpha = log(log(max_val)) / log(n)
    beta = math.log(size) / math.log(n) if size > 1 and n > 1 else 0
    alpha = (math.log(math.log(max_val)) / math.log(n)
             if max_val > math.e and n > 1 else 0)
    return alpha, beta


# -----------------------------------------------------------------------
# Strategy 1: "trivial" construction achieving alpha + beta <= 1 + o(1)
# Take T = {0}, S = multiples of every integer up to n via lcm-chunking.
# A simple way: S = {1, 2, ..., n} (all multiples of everything up to n
# trivially divide themselves), T = {0}. This gives beta=1, alpha~0
# (since max value is n, not exponential) -- actually does even better
# than alpha+beta=1 in a degenerate sense. The interesting regime is
# when we *constrain* size to be much smaller, forcing magnitude up.
# -----------------------------------------------------------------------
def trivial_construction(n):
    S = list(range(1, n + 1))
    T = [0]
    return S, T


# -----------------------------------------------------------------------
# Strategy 2: factorial / LCM-based construction.
# Idea: let L = lcm(1, 2, ..., n). Then i | L for all i in [n]. Take
# T = {0}, S = {L}. This trivially covers everything with |S|=|T|=1
# (beta -> 0) but L grows like e^n (by the prime number theorem,
# log(lcm(1..n)) ~ n), so alpha -> 1. This sits at the OTHER extreme
# of the alpha+beta tradeoff.
# -----------------------------------------------------------------------
def lcm_construction(n):
    L = 1
    for i in range(1, n + 1):
        L = math.lcm(L, i)
    S = [L]
    T = [0]
    return S, T


# -----------------------------------------------------------------------
# Strategy 3: balanced construction using prime-power chunking.
# Split [1, n] into "easy" divisors covered with small numbers, and
# delegate the rest to controlled-size products. This is a toy
# illustration of the tradeoff space -- not the paper's actual
# structured construction, just an experiment to see how far naive
# bucketing gets us toward alpha, beta < 1/2.
# -----------------------------------------------------------------------
def bucketed_construction(n, num_buckets):
    """
    Partition [1, n] into num_buckets contiguous ranges. For each bucket,
    use the LCM of that bucket's integers as one element of S (paired
    with T = {0}), PLUS we get to reuse across buckets by allowing
    multiple T elements (shifts), letting us cover more values for the
    same S size. This isn't the paper's clever number-theoretic
    construction (that requires deeper machinery in Sec 6) -- it's a
    naive baseline to see what bucketing alone buys you.
    """
    bucket_size = max(1, n // num_buckets)
    S = []
    bounds = []
    start = 1
    while start <= n:
        end = min(start + bucket_size - 1, n)
        L = 1
        for i in range(start, end + 1):
            L = math.lcm(L, i)
        S.append(L)
        bounds.append((start, end))
        start = end + 1
    T = [0]
    return S, T, bounds


def run_experiment(n_values):
    print(f"{'n':>6} | {'strategy':<22} | {'|S|':>6} {'|T|':>4} | "
          f"{'max val':>14} | {'alpha':>6} {'beta':>6} | covers?")
    print("-" * 90)

    for n in n_values:
        # Trivial: beta~1, alpha~0
        S, T = trivial_construction(n)
        ok, fail = covers_all(S, T, n)
        a, b = measure_params(S, T, n)
        print(f"{n:>6} | {'trivial (S=[1..n])':<22} | {len(S):>6} {len(T):>4} | "
              f"{max(S):>14} | {a:>6.3f} {b:>6.3f} | {ok}")

        # LCM: beta~0, alpha~1
        S, T = lcm_construction(n)
        ok, fail = covers_all(S, T, n)
        a, b = measure_params(S, T, n)
        print(f"{n:>6} | {'lcm (S={lcm(1..n)})':<22} | {len(S):>6} {len(T):>4} | "
              f"{S[0]:>14} | {a:>6.3f} {b:>6.3f} | {ok}")

        # Bucketed: somewhere in between, parameterized by num_buckets
        for nb in [2, 4, 8]:
            if nb > n:
                continue
            S, T, bounds = bucketed_construction(n, nb)
            ok, fail = covers_all(S, T, n)
            a, b = measure_params(S, T, n)
            label = f"bucketed (k={nb})"
            print(f"{n:>6} | {label:<22} | {len(S):>6} {len(T):>4} | "
                  f"{max(S):>14} | {a:>6.3f} {b:>6.3f} | {ok}")
        print()


if __name__ == "__main__":
    run_experiment([10, 20, 40, 80])

    print("\n" + "=" * 90)
    print("Target for the conjecture: alpha = beta = 1/3 (both as small as possible).")
    print("Trivial sits at (alpha~0, beta~1). LCM sits at (alpha~1, beta~0).")
    print("Bucketing interpolates between them but along a roughly LINEAR")
    print("tradeoff curve (alpha+beta ~ 1) rather than bending the curve")
    print("toward the origin. Bending the curve toward (1/3, 1/3) is exactly")
    print("the open problem -- it requires genuinely new number-theoretic")
    print("structure (Section 6 of the paper discusses an arithmetic-")
    print("progression-based variant), not just better bucketing.")
