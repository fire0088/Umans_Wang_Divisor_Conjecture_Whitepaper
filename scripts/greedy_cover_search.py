"""
Novel approach: instead of formulaic S,T (products, LCMs, APs), use a
greedy combinatorial SET-COVER search over smooth-number candidates.

Rationale: smooth numbers (products of small primes) are divisible by
many small integers at once, so they're natural high-coverage candidates
for either S or T. We search greedily for (s,t) pairs from a smooth-number
candidate pool that jointly cover the n-divisor property: every i in [n]
divides some s-t.

Goal: see whether real combinatorial search can push (alpha,beta) below
the trivial formulaic line alpha=1-beta, toward the information-theoretic
floor alpha=1-2beta implied by Proposition 3.4 + the primorial bound.
"""

import math
import random
from sympy import factorint


def generate_smooth_candidates(bound, prime_bound, count):
    """
    Generate 'count' smooth numbers up to 'bound', built from primes
    up to 'prime_bound'. Smooth numbers maximize divisor coverage per
    unit magnitude -- a natural high-value candidate pool for greedy
    set cover.
    """
    primes = [p for p in range(2, prime_bound + 1) if all(p % d for d in range(2, int(p**0.5) + 1))]
    candidates = set()
    random.seed(42)
    attempts = 0
    while len(candidates) < count and attempts < count * 50:
        attempts += 1
        val = 1
        # random product of small prime powers, capped at bound
        random.shuffle(primes)
        for p in primes:
            if val * p > bound:
                continue
            if random.random() < 0.5:
                val *= p
                # occasionally allow repeated prime power
                while random.random() < 0.3 and val * p <= bound:
                    val *= p
        if val > 1:
            candidates.add(val)
    return sorted(candidates)


def coverage_for_pair(s, t, n):
    """Set of i in [1,n] such that i | (s-t)."""
    diff = abs(s - t)
    if diff == 0:
        return set()
    covered = set()
    # only need to check divisors of diff that are <= n
    for d in range(1, int(math.isqrt(diff)) + 1):
        if diff % d == 0:
            if d <= n:
                covered.add(d)
            other = diff // d
            if other <= n:
                covered.add(other)
    return covered


def greedy_cover(n, candidate_pool, max_pairs=2000):
    """
    Greedy set cover: maintain growing S, T sets (shared pool of
    candidates can be used in either role). Repeatedly pick the pair
    (s,t) from the pool that covers the most new i's, until all of
    [1,n] is covered or we exhaust the pool/budget.
    """
    uncovered = set(range(1, n + 1))
    S, T = set(), set()
    pool = candidate_pool

    # seed with 0 in T (covers nothing alone, but enables s-0=s checks)
    T.add(0)

    while uncovered and max_pairs > 0:
        best_gain = -1
        best_choice = None
        # Try adding a new element to S (paired against all of T)
        sample = random.sample(pool, min(60, len(pool)))
        for cand in sample:
            gain = set()
            for t in T:
                gain |= coverage_for_pair(cand, t, n) & uncovered
            if len(gain) > best_gain:
                best_gain = len(gain)
                best_choice = ('S', cand, gain)
        # Try adding a new element to T (paired against all of S)
        for cand in sample:
            gain = set()
            for s in S:
                gain |= coverage_for_pair(s, cand, n) & uncovered
            if len(gain) > best_gain:
                best_gain = len(gain)
                best_choice = ('T', cand, gain)

        if best_choice is None or best_gain <= 0:
            break

        role, val, gain = best_choice
        if role == 'S':
            S.add(val)
        else:
            T.add(val)
        uncovered -= gain
        max_pairs -= 1

    return S, T, uncovered


def measure_params(S, T, n):
    size = max(len(S), len(T))
    max_val = max(max(S, default=1), max(T, default=1))
    beta = math.log(size) / math.log(n) if size > 1 and n > 1 else 0
    alpha = (math.log(math.log(max_val)) / math.log(n)
             if max_val > math.e and n > 1 else 0)
    return alpha, beta


def run_experiment(n_values):
    print(f"{'n':>5} | {'|S|':>5} {'|T|':>5} | {'max_val':>14} | "
          f"{'alpha':>6} {'beta':>6} {'a+b':>6} | uncovered")
    print("-" * 80)
    for n in n_values:
        bound = n ** 3  # generous magnitude budget for the candidate pool
        prime_bound = max(10, n // 2)
        pool = generate_smooth_candidates(bound, prime_bound, count=400)
        if not pool:
            print(f"{n:>5} | pool generation failed")
            continue
        S, T, uncovered = greedy_cover(n, pool)
        alpha, beta = measure_params(S, T, n)
        print(f"{n:>5} | {len(S):>5} {len(T):>5} | {max(max(S,default=1),max(T,default=1)):>14} | "
              f"{alpha:>6.3f} {beta:>6.3f} {alpha+beta:>6.3f} | {sorted(uncovered) if uncovered else 'none'}")


if __name__ == "__main__":
    run_experiment([20, 30, 40, 60])

    print()
    print("=" * 80)
    print("If alpha+beta drops meaningfully below 1 here (vs ~1.0-1.5 from")
    print("formulaic constructions), greedy search over smooth candidates is")
    print("genuinely finding difference-set structure that closed-form")
    print("constructions miss. If it stays >= 1, the bottleneck isn't search")
    print("quality -- it's that smooth numbers alone don't supply enough")
    print("additive (difference) structure, confirming the mult/additive")
    print("mismatch as the real obstruction.")
