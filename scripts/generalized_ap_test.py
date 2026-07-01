"""
Testing the genuinely multi-dimensional structure: Conjecture 3.3 wants
S, T to be SUMS of several arithmetic progressions, not single APs. We've
only ever tested the single-AP special case (Proposition 3.4). This
script properly tests the 2-progression case using Lemma 6.1's exact
combination formula:

  Given A1 = {b1 + i*c1 : 1<=i<=l1}, A2 = {b2 + i*c2 : 1<=i<=l2}, the
  generalized AP

    A = {c1*b2 + i*(c1*c2) + j*(c2*b1 - c1*b2) : 1<=i<=max(l1,l2), j in {0,1}}

  contains a multiple of x if A1 or A2 does.

This time we apply it correctly (not flattening to a union, which is
what broke the "recursive doubling" experiment earlier) -- we split the
primes into TWO halves, find a strong single-AP solution for EACH half
independently (reusing the verified Lemma 6.2 search), then combine the
two solutions into one genuine 2-term generalized AP via Lemma 6.1, and
measure its (count, magnitude) honestly against the single-AP baseline
on the full prime set.
"""

import math
import random
from sympy import primerange


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def crt_idempotents(groups):
    U_list = [prod(g) for g in groups]
    U = prod(U_list)
    V = []
    for Ui in U_list:
        Mi = U // Ui
        Ti = pow(Mi, -1, Ui)
        Vi = (Mi * Ti) % U
        V.append(Vi)
    return U, V


def compute_S(groups):
    U, V = crt_idempotents(groups)
    S = sum((i + 1) * V[i] for i in range(len(V))) % U
    return U, S


def continued_fraction_candidates(S, U, max_c):
    a = S % U
    q_prev, q_cur = 1, 0
    x, y = a, U
    candidates = []
    while y != 0 and q_cur <= max_c:
        q = x // y
        x, y = y, x - q * y
        q_prev, q_cur = q_cur, q * q_cur + q_prev
        if 0 < q_cur <= max_c:
            c = q_cur
            r = (c * S) % U
            b = -r if r <= U - r else U - r
            candidates.append((c, b))
    return candidates


def random_partition(primes, l, seed):
    rng = random.Random(seed)
    groups = [[] for _ in range(l)]
    for p in primes:
        groups[rng.randrange(l)].append(p)
    return [g if g else [1] for g in groups]


def solve_single_AP(primes, l_values, trials):
    """Find a strong (l, c, b) AP covering this prime set, via the
    verified random-partition + continued-fraction search."""
    if len(primes) == 0:
        return None
    if len(primes) == 1:
        p = primes[0]
        return (1, p, 0)
    log_U_bits = sum(p.bit_length() for p in primes)
    max_c = 1 << (log_U_bits + 5)
    best = None
    for l in l_values:
        if l > len(primes):
            continue
        for seed in range(trials):
            groups = random_partition(primes, l, seed)
            U, S = compute_S(groups)
            for c, b in continued_fraction_candidates(S, U, max_c):
                terms = [b + i * c for i in range(1, l + 1)]
                if any(t == 0 for t in terms):
                    continue
                covered = sum(1 for p in primes if any(t % p == 0 for t in terms))
                if covered < len(primes):
                    continue  # only accept full coverage of this half
                score = max(c, abs(b))
                if best is None or score < best[3]:
                    best = (l, c, b, score)
    return best[:3] if best else None


def lemma_6_1_merge(A1, A2):
    """Combine two simple APs into one generalized AP per Lemma 6.1."""
    l1, c1, b1 = A1
    l2, c2, b2 = A2
    lmax = max(l1, l2)
    terms = []
    for i in range(1, lmax + 1):
        for j in (0, 1):
            term = c1 * b2 + i * (c1 * c2) + j * (c2 * b1 - c1 * b2)
            terms.append(term)
    return terms, lmax * 2


def verify_terms_cover(terms, primes):
    return [p for p in primes if not any(t % p == 0 for t in terms)]


def run_comparison(n, l_values, trials, split_fraction=0.5):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    print(f"n={n}, {len(primes)} primes, sqrt(U) baseline = {log_U_bits/2:.1f} bits")
    print()

    # --- baseline: single-AP solution on the FULL prime set ---
    baseline = solve_single_AP(primes, l_values, trials)
    if baseline:
        l, c, b = baseline
        bits = max(c, abs(b)).bit_length()
        print(f"BASELINE (single AP, full set): l={l}, magnitude_bits={bits}, count={l}")
    print()

    # --- generalized AP: split into two halves, solve each, merge ---
    split_idx = int(len(primes) * split_fraction)
    half1, half2 = primes[:split_idx], primes[split_idx:]
    print(f"Splitting into halves: {len(half1)} + {len(half2)} primes")

    A1 = solve_single_AP(half1, l_values, trials)
    A2 = solve_single_AP(half2, l_values, trials)
    if A1 is None or A2 is None:
        print("Could not solve one of the halves.")
        return

    l1, c1, b1 = A1
    l2, c2, b2 = A2
    bits1 = max(c1, abs(b1)).bit_length()
    bits2 = max(c2, abs(b2)).bit_length()
    print(f"  Half1 solution: l={l1}, bits={bits1}")
    print(f"  Half2 solution: l={l2}, bits={bits2}")

    merged_terms, merged_count = lemma_6_1_merge(A1, A2)
    uncovered = verify_terms_cover(merged_terms, primes)
    merged_bits = max(abs(t) for t in merged_terms).bit_length()

    print()
    print(f"GENERALIZED AP (Lemma 6.1 merge): count={merged_count}, "
          f"magnitude_bits={merged_bits}, verified={'YES' if not uncovered else 'NO ' + str(uncovered)}")
    print()
    if baseline:
        print(f"Comparison: baseline (l={baseline[0]}, bits={max(baseline[1],abs(baseline[2])).bit_length()}) "
              f"vs generalized (count={merged_count}, bits={merged_bits})")


if __name__ == "__main__":
    for n in [150, 300, 500]:
        print("=" * 90)
        run_comparison(n=n, l_values=[2, 3, 4], trials=15)
        print()
