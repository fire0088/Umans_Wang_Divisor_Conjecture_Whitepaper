"""
Scaling study: for n = 10, 20, ..., does the "lucky convergent" effect we
found at n=30,50 persist (or grow) as n increases, or does it fade?

For each n, we try the random-partition strategy (which won previously)
across many trials and several l values, and track:

    savings(n) = log2(sqrt(U)) - log2(best achieved max(|b|,c))

If savings(n) grows or holds roughly constant as n grows, that's a real
signal the effect has asymptotic legs. If it shrinks toward 0, it's a
small-n artifact.

All winning (b,c) pairs are verified against ground truth (direct
divisibility check) before being counted.
"""

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


def verify_ap_covers_primes(b, c, l, primes):
    terms = [b + i * c for i in range(1, l + 1)]
    return [p for p in primes if not any(t % p == 0 for t in terms)]


def best_for_n(n, l_values, trials):
    primes = list(primerange(2, n + 1))
    if len(primes) < 2:
        return None
    log_U_bits = sum(p.bit_length() for p in primes)
    max_c = 1 << log_U_bits

    overall_best = None  # (l, c, b, score)
    for l in l_values:
        if l > len(primes):
            continue
        for seed in range(trials):
            groups = random_partition(primes, l, seed)
            U, S = compute_S(groups)
            candidates = continued_fraction_candidates(S, U, max_c)
            for c, b in candidates:
                terms = [b + i * c for i in range(1, l + 1)]
                if any(t == 0 for t in terms):
                    continue  # reject degenerate zero-term solutions
                score = max(c, abs(b))
                if overall_best is None or score < overall_best[3]:
                    overall_best = (l, c, b, score)

    if overall_best is None:
        return None
    l, c, b, score = overall_best
    uncovered = verify_ap_covers_primes(b, c, l, primes)
    return {
        'n': n,
        'num_primes': len(primes),
        'log_U_bits': log_U_bits,
        'l': l,
        'c': c,
        'b': b,
        'best_bits': score.bit_length(),
        'verified': not uncovered,
        'uncovered': uncovered,
    }


def run_scaling_study(n_values, l_values, trials):
    print(f"{'n':>5} {'#primes':>8} {'log2(U)':>8} {'sqrt(U) bits':>13} | "
          f"{'best l':>6} {'best bits':>10} {'savings (bits)':>15} | verified | min|term|")
    print("-" * 110)
    results = []
    for n in n_values:
        r = best_for_n(n, l_values, trials)
        if r is None:
            continue
        sqrt_bits = r['log_U_bits'] / 2
        savings = sqrt_bits - r['best_bits']
        results.append((n, savings))
        ok = "YES" if r['verified'] else f"NO {r['uncovered']}"
        terms = [r['b'] + i * r['c'] for i in range(1, r['l'] + 1)]
        min_term = min(abs(t) for t in terms)
        print(f"{r['n']:>5} {r['num_primes']:>8} {r['log_U_bits']:>8} {sqrt_bits:>13.1f} | "
              f"{r['l']:>6} {r['best_bits']:>10} {savings:>15.1f} | {ok:>10} | {min_term}")
    return results


if __name__ == "__main__":
    n_values = [10, 20, 30, 40, 50, 70, 90, 110, 130, 150]
    l_values = [2, 3, 4, 5, 6]
    trials = 40

    results = run_scaling_study(n_values, l_values, trials)

    print()
    print("=" * 95)
    print("Trend in 'savings' (bits below the generic sqrt(U) floor):")
    for n, savings in results:
        bar = "#" * max(0, int(savings))
        print(f"  n={n:>4}  savings={savings:>6.1f}  {bar}")
