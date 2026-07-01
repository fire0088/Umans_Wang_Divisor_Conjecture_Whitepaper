"""
Testing Lemma 6.2 of Umans-Wang (arXiv:2511.10851).

An arithmetic progression A = {b + ic : 1 <= i <= l} contains a multiple of
every prime p <= n  iff  there's a factorization U = U_1 * U_2 * ... * U_l
of the primorial U (product of all primes <= n) and integers b, c such that

    c * (sum_{i=1}^l  i * V_i)  +  b  ≡  0  (mod U)

where V_i = (U/U_i) * T_i mod U, and T_i is the inverse of (U/U_i) mod U_i
(standard CRT idempotent construction).

For a FIXED factorization (hence fixed S = sum i*V_i mod U), finding the
smallest (b,c) satisfying c*S + b ≡ 0 (mod U) is exactly a Diophantine
approximation problem: convergents of the continued fraction expansion of
S/U give the best small (b,c) pairs (Dirichlet's approximation theorem).
Generically this gives b,c ~ sqrt(U) ~ exp(n/2) -- matching the known floor.

What we're hunting for: does any CHOICE of factorization (grouping of
primes into U_1..U_l, and assignment to slots i=1..l) produce an S with
an anomalously good early convergent -- i.e. a much smaller (b,c) than
the generic sqrt(U) bound -- which would be genuine evidence toward the
conjecture (or at least toward the prime sub-case of it)?
"""

import random
from sympy import primerange


def crt_idempotents(groups):
    """
    Given groups (list of lists of primes), with U_i = product of group i,
    U = product of all primes, return V_i = (U/U_i)*T_i mod U for each i,
    where T_i = inverse of (U/U_i) mod U_i.
    """
    U_list = [prod(g) for g in groups]
    U = prod(U_list)
    V = []
    for Ui in U_list:
        Mi = U // Ui          # U / U_i
        Ti = pow(Mi, -1, Ui)  # inverse of Mi mod U_i
        Vi = (Mi * Ti) % U
        V.append(Vi)
    return U, V


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def compute_S(groups):
    U, V = crt_idempotents(groups)
    S = sum((i + 1) * V[i] for i in range(len(V))) % U
    return U, S


def continued_fraction_convergents(S, U, max_c):
    """
    Compute convergents (c, b) of the continued fraction expansion of S/U,
    i.e. integers c (denominators) and corresponding b = (c*S) mod U taken
    as the signed residue closest to 0, for c up to max_c. Returns the
    list of (c, b) pairs found via the Euclidean algorithm on (S, U).
    """
    a, bb = S % U, U
    p_prev, p_cur = 0, 1   # numerator convergents (not needed directly)
    q_prev, q_cur = 1, 0   # denominator convergents
    results = []
    x, y = a, bb
    while y != 0 and q_cur <= max_c:
        q = x // y
        x, y = y, x - q * y
        q_prev, q_cur = q_cur, q * q_cur + q_prev
        if q_cur <= max_c and q_cur > 0:
            c = q_cur
            r = (c * S) % U
            # need b ≡ -c*S (mod U): b = -r or U-r, whichever is smaller magnitude
            b = -r if r <= U - r else U - r
            results.append((c, b))
    return results


def best_pair(S, U, max_c):
    candidates = continued_fraction_convergents(S, U, max_c)
    if not candidates:
        return None
    # minimize max(c, |b|) -- the quantity that sets our magnitude bound
    best = min(candidates, key=lambda cb: max(cb[0], abs(cb[1])))
    return best


def random_partition(primes, l, seed):
    rng = random.Random(seed)
    groups = [[] for _ in range(l)]
    for p in primes:
        groups[rng.randrange(l)].append(p)
    # avoid empty groups (U_i must be >=1; empty group -> U_i=1, harmless)
    return [g if g else [1] for g in groups]


def sequential_partition(primes, l):
    groups = [[] for _ in range(l)]
    for idx, p in enumerate(primes):
        groups[idx % l].append(p)
    return [g if g else [1] for g in groups]


def contiguous_partition(primes, l):
    groups = [[] for _ in range(l)]
    chunk = max(1, len(primes) // l)
    for idx, p in enumerate(primes):
        groups[min(idx // chunk, l - 1)].append(p)
    return [g if g else [1] for g in groups]


def verify_ap_covers_primes(b, c, l, primes):
    """Ground-truth check: does {b + i*c : i=1..l} actually contain a
    multiple of every prime in 'primes'?"""
    terms = [b + i * c for i in range(1, l + 1)]
    uncovered = []
    for p in primes:
        if not any(t % p == 0 for t in terms):
            uncovered.append(p)
    return uncovered


def run_experiment(n, l_values, trials_per_l=8):
    primes = list(primerange(2, n + 1))
    print(f"n={n}, primes={primes}, U has {len(primes)} prime factors")
    log_U_bits = sum(p.bit_length() for p in primes)  # rough proxy for log2(U)
    print(f"approx log2(U) ~ {log_U_bits}")
    print()
    print(f"{'l':>4} {'strategy':<12} | {'best c':>15} {'best b':>15} | "
          f"log2(max(c,|b|))  vs  log2(sqrt(U))~{log_U_bits/2:.1f}")
    print("-" * 95)

    for l in l_values:
        max_c = 1 << (log_U_bits)  # generous search budget

        strategies = {
            'sequential': [sequential_partition(primes, l)],
            'contiguous': [contiguous_partition(primes, l)],
            'random': [random_partition(primes, l, seed) for seed in range(trials_per_l)],
        }

        for name, group_list in strategies.items():
            best_overall = None
            for groups in group_list:
                U, S = compute_S(groups)
                bp = best_pair(S, U, max_c)
                if bp is None:
                    continue
                c, b = bp
                score = max(c, abs(b))
                if best_overall is None or score < best_overall[2]:
                    best_overall = (c, b, score)
            if best_overall:
                c, b, score = best_overall
                bits = score.bit_length()
                uncovered = verify_ap_covers_primes(b, c, l, primes)
                check = "VERIFIED" if not uncovered else f"FAILED missing={uncovered}"
                print(f"{l:>4} {name:<12} | {c:>15} {b:>15} | "
                      f"{bits:>6}  vs  {log_U_bits/2:.1f}  | {check}")


if __name__ == "__main__":
    run_experiment(n=30, l_values=[2, 3, 4, 5])
    print()
    run_experiment(n=50, l_values=[2, 3, 4, 5, 8])
