"""
Working backwards: directly testing the paper's own flagged-but-open
edge case. Section 6 of Umans-Wang states:

  "Although it seems unlikely, we cannot rule out the possibility that
   the Arithmetic Progression Version may hold with b <= exp(O(n^(1-2beta)))
   and c = 1!"

With c fixed at 1, Lemma 6.2's congruence c*S + b ≡ 0 (mod U) collapses
to b = -S (mod U), completely determined by the factorization choice --
no continued-fraction optimization is possible. We directly search many
random partitions and track how small |b| gets, comparing against the
PROVEN necessary floor exp(n^(1-2*beta)).

If b never gets close to that floor across extensive search, this is
real evidence against the c=1 possibility. If it does, that's a
genuinely surprising and citable finding.
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


def random_partition(primes, l, seed):
    rng = random.Random(seed)
    groups = [[] for _ in range(l)]
    for p in primes:
        groups[rng.randrange(l)].append(p)
    return [g if g else [1] for g in groups]


def best_b_for_c_equals_1(primes, l, trials):
    """With c=1 fixed, b = -S (mod U) signed. Search over partitions for
    the smallest |b|. Also verify ground truth."""
    best = None  # (b, terms, groups)
    for seed in range(trials):
        groups = random_partition(primes, l, seed)
        U, S = compute_S(groups)
        r = S % U
        b = -r if r <= U - r else U - r
        terms = [b + i for i in range(1, l + 1)]  # c=1
        if any(t == 0 for t in terms):
            continue
        if best is None or abs(b) < abs(best[0]):
            best = (b, terms)
    return best


def verify(terms, primes):
    return [p for p in primes if not any(t % p == 0 for t in terms)]


def run(n, l_values, trials):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)

    print(f"n={n}, {len(primes)} primes, log2(U)={log_U_bits} bits")
    print(f"{'l':>5} {'beta':>6} | {'best |b| bits':>14} {'necessary floor bits':>20} | "
          f"{'b/floor ratio':>14} | verified")
    print("-" * 95)

    for l in l_values:
        beta = math.log(l) / math.log(n) if l > 1 else 0
        result = best_b_for_c_equals_1(primes, l, trials)
        if result is None:
            print(f"{l:>5} {beta:>6.3f} | no solution found")
            continue
        b, terms = result

        # necessary floor: (b+c) >= exp(n^(1-2*beta))  =>  b >= exp(n^(1-2*beta)) roughly
        exponent = max(0.0, 1 - 2 * beta)
        floor_value_log2 = (n ** exponent) / math.log(2) if exponent > 0 else 0

        b_bits = abs(b).bit_length()
        uncovered = verify(terms, primes)
        ok = "YES" if not uncovered else f"NO ({len(uncovered)} missing)"

        ratio = b_bits / floor_value_log2 if floor_value_log2 > 0 else float('inf')
        print(f"{l:>5} {beta:>6.3f} | {b_bits:>14} {floor_value_log2:>20.1f} | "
              f"{ratio:>14.3f} | {ok}")


if __name__ == "__main__":
    for n in [100, 300, 700]:
        print("=" * 95)
        run(n=n, l_values=[2, 4, 8, 16, 32], trials=200)
        print()
