"""
Stacking the alteration method on top of the Lemma 6.2 construction.

Instead of running the random-partition + continued-fraction search with
enough trials/structure to guarantee FULL coverage of all primes <= n
(which is what we did before), we deliberately UNDERSHOOT: use a smaller
l and/or fewer search trials, accept that some primes will be left
uncovered, and patch each leftover prime individually with one cheap
extra element.

We compare total cost (combined magnitude, combined count) against the
"force full coverage" baseline from before.
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


def best_undersized(primes, l, trials, n):
    """Find the best (l,c,b) AP using only 'trials' random partitions
    (deliberately undershooting -- fewer trials than needed to guarantee
    full coverage), measured by max(c,|b|), allowing partial coverage."""
    log_U_bits = sum(p.bit_length() for p in primes)
    max_c = 1 << (log_U_bits + 5)
    best = None
    for seed in range(trials):
        groups = random_partition(primes, l, seed)
        U, S = compute_S(groups)
        for c, b in continued_fraction_candidates(S, U, max_c):
            terms = [b + i * c for i in range(1, l + 1)]
            if any(t == 0 for t in terms):
                continue
            score = max(c, abs(b))
            covered = sum(1 for p in primes if any(t % p == 0 for t in terms))
            # prioritize: prefer more coverage, tie-break on smaller score
            key = (-covered, score)
            if best is None or key < best[0]:
                best = (key, l, c, b, covered)
    if best is None:
        return None
    _, l, c, b, covered = best
    return l, c, b, covered


def patch_holes(b, c, l, primes):
    terms = [b + i * c for i in range(1, l + 1)]
    holes = [p for p in primes if not any(t % p == 0 for t in terms)]
    # cheapest patch: one extra element per hole, targeting exactly p
    patch_terms = [(b % p) and (p - (b % p)) or p for p in holes]  # not used directly
    patches = []
    for p in holes:
        # smallest positive multiple-of-p style fix: new term = p itself
        # (trivially p | p) -- cheapest possible patch
        patches.append(p)
    return holes, patches


def run_comparison(n, l_values, undershoot_trials, full_trials):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    print(f"n={n}, {len(primes)} primes, sqrt(U) baseline = {log_U_bits/2:.1f} bits")
    print()

    print("--- FULL-COVERAGE baseline (many trials, force full coverage) ---")
    best_full = None
    for l in l_values:
        res = best_undersized(primes, l, full_trials, n)
        if res is None:
            continue
        l_, c, b, covered = res
        if covered == len(primes):
            score = max(c, abs(b))
            if best_full is None or score < best_full[0]:
                best_full = (score, l_, covered)
    if best_full:
        print(f"best full-coverage: l={best_full[1]}, magnitude_bits={best_full[0].bit_length()}, "
              f"count={best_full[1]}")
    print()

    print("--- UNDERSHOOT + PATCH (fewer trials, smaller l, patch leftovers) ---")
    print(f"{'l':>3} {'trials':>7} | {'magnitude bits':>15} {'covered':>8} {'holes':>6} | "
          f"{'combined count':>15} {'combined bits':>14}")
    print("-" * 80)
    for l in l_values:
        res = best_undersized(primes, l, undershoot_trials, n)
        if res is None:
            continue
        l_, c, b, covered = res
        holes, patches = patch_holes(b, c, l_, primes)
        mag_bits = max(c, abs(b)).bit_length()
        patch_bits = max((p.bit_length() for p in patches), default=0)
        combined_bits = max(mag_bits, patch_bits)
        combined_count = l_ + len(holes)
        print(f"{l:>3} {undershoot_trials:>7} | {mag_bits:>15} {covered:>8} {len(holes):>6} | "
              f"{combined_count:>15} {combined_bits:>14}")


if __name__ == "__main__":
    for n in [300, 500, 800]:
        print("=" * 80)
        run_comparison(
            n=n,
            l_values=[2, 3, 4],
            undershoot_trials=1,   # extremely cheap search
            full_trials=30,
        )
        print()
