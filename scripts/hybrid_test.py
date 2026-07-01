"""
Hybrid construction test:

  Stage 1 (discrete-log sieve): for fixed base g, exponent budget L,
  S_disc = {g^1, ..., g^L}, T_disc = {1}. This covers (for free, via
  Fermat) every prime p with ord_p(g) <= L. Magnitude of S_disc is
  g^L, i.e. L*log2(g) BITS -- this matters, it's not "L", it's
  exponential in L (though linear in L when measured in BITS, since
  bit-length of g^L is exactly L*log2(g)).

  Stage 2 (hard core): primes NOT covered by stage 1 are fed into our
  earlier random-partition + continued-fraction Lemma 6.2 search,
  restricted to just that smaller leftover set.

  Combined cost:
    total count  = L (stage 1) + l_hard (stage 2)
    total magnitude bits = max(L*log2(g), stage-2 magnitude bits)

  Baseline: run the SAME stage-2 search on the FULL prime set (no
  pre-filtering) and compare combined cost against the hybrid.
"""

import math
import random
from sympy import primerange, factorint


def multiplicative_order(g, p):
    if p == 2:
        return 1
    phi = p - 1
    order = phi
    for prime_factor in factorint(phi):
        while order % prime_factor == 0 and pow(g, order // prime_factor, p) == 1:
            order //= prime_factor
    return order


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


def search_hard_core(primes, l_values, trials):
    """Run the Lemma 6.2 random-partition + continued-fraction search,
    restricted to the given prime list."""
    if len(primes) == 0:
        return {'l': 0, 'c': 1, 'b': 0, 'bits': 0}
    if len(primes) == 1:
        p = primes[0]
        return {'l': 1, 'c': p, 'b': 0, 'bits': p.bit_length()}

    log_U_bits = sum(p.bit_length() for p in primes)
    max_c = 1 << (log_U_bits + 5)
    overall_best = None
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
                score = max(c, abs(b))
                if overall_best is None or score < overall_best[3]:
                    overall_best = (l, c, b, score)
    if overall_best is None:
        return None
    l, c, b, score = overall_best
    return {'l': l, 'c': c, 'b': b, 'bits': score.bit_length()}


def run_hybrid(n, g, L_values, l_values, trials):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)

    print(f"n={n}, g={g}, {len(primes)} primes, full sqrt(U) baseline = {log_U_bits/2:.1f} bits")
    print()

    # baseline: hard-core search on the FULL prime set, no pre-filtering
    baseline = search_hard_core(primes, l_values, trials)
    print(f"BASELINE (no sieve): l={baseline['l']}, magnitude_bits={baseline['bits']}, "
          f"count={baseline['l']}")
    print()

    print(f"{'L':>4} | {'covered':>8} {'leftover':>9} | {'stage1 bits':>11} | "
          f"{'l_hard':>7} {'stage2 bits':>11} | {'combined bits':>13} {'combined count':>14}")
    print("-" * 95)

    orders = {}
    for p in primes:
        if math.gcd(g, p) == 1:
            orders[p] = multiplicative_order(g, p)
        else:
            orders[p] = None

    for L in L_values:
        covered = [p for p in primes if orders[p] is not None and orders[p] <= L]
        leftover = [p for p in primes if p not in covered]

        stage1_bits = max(1, int(L * math.log2(g)))

        stage2 = search_hard_core(leftover, l_values, trials)
        stage2_bits = stage2['bits'] if stage2 else 0
        l_hard = stage2['l'] if stage2 else 0

        combined_bits = max(stage1_bits, stage2_bits)
        combined_count = L + l_hard

        print(f"{L:>4} | {len(covered):>8} {len(leftover):>9} | {stage1_bits:>11} | "
              f"{l_hard:>7} {stage2_bits:>11} | {combined_bits:>13} {combined_count:>14}")

    print()
    print(f"Compare combined_bits / combined_count above against baseline: "
          f"bits={baseline['bits']}, count={baseline['l']}")


if __name__ == "__main__":
    run_hybrid(
        n=150,
        g=2,
        L_values=[5, 10, 15, 20, 30, 40],
        l_values=[2, 3, 4, 5, 6],
        trials=15,
    )
