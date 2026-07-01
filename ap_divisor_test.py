"""
Testing Proposition 3.4 of Umans-Wang (arXiv:2511.10851).

Definition 3.1 (n-divisor property): A set A of positive integers satisfies
the n-divisor property if for every i in {1,...,n}, there exists a in A
such that i | a.

Proposition 3.4: if there's a SINGLE arithmetic progression A = {b, b+c,
b+2c, ..., b+Kc} (size K+1 = n^(2*beta), magnitude <= exp(n^alpha))
satisfying the n-divisor property, that alone implies the Strong
(alpha,beta)-Divisor Conjecture.

The open question (explicitly stated unresolved in the paper): can we
beat the trivial line alpha = 1 - beta? This script tests natural
AP-based constructions to see whether arithmetic-progression structure
buys anything beyond the trivial bucketing bound.

Strategy under test: pick common difference c = lcm(1..m) for varying
m. For i <= m, gcd(i,c) = i, so k=1 (i.e. a=c) covers it immediately.
For i in (m, n], the smallest k with i | kc is k = i / gcd(i,c) -- this
can be as large as i itself if gcd(i,c) is small, which is the
bottleneck we expect to find.
"""

import math


def lcm_range(lo, hi):
    L = 1
    for x in range(lo, hi + 1):
        L = math.lcm(L, x)
    return L


def min_k_for_ap(i, c):
    """Smallest k >= 1 such that i divides k*c (with b=0)."""
    g = math.gcd(i, c)
    return i // g


def build_ap_construction(n, m):
    """
    b = 0, c = lcm(1..m). Returns (K, max_val) where K is the number
    of AP terms needed (covering i=1..n), and max_val = K*c is the
    magnitude of the largest element used.
    """
    c = lcm_range(1, m)
    K = 1
    for i in range(1, n + 1):
        k_i = min_k_for_ap(i, c)
        K = max(K, k_i)
    max_val = K * c
    return K, max_val, c


def measure_ap_params(n, K, max_val):
    # |A| = K (roughly n^(2*beta))  =>  beta = log(K) / (2*log(n))
    # max_val ~ exp(n^alpha)        =>  alpha = log(log(max_val)) / log(n)
    beta = math.log(K) / (2 * math.log(n)) if K > 1 else 0
    alpha = (math.log(math.log(max_val)) / math.log(n)
             if max_val > math.e else 0)
    return alpha, beta


def verify_ap_covers(n, c, K):
    """Sanity check: does {0, c, 2c, ..., Kc} actually satisfy the
    n-divisor property?"""
    for i in range(1, n + 1):
        if not any((k * c) % i == 0 for k in range(0, K + 1)):
            return False, i
    return True, None


def run_experiment(n_values, m_fractions):
    print(f"{'n':>6} {'m':>6} {'m/n':>6} | {'K (=|A|)':>12} {'max_val':>20} | "
          f"{'alpha':>6} {'beta':>6} | {'alpha+beta':>10} | covers?")
    print("-" * 100)

    for n in n_values:
        for frac in m_fractions:
            m = max(1, int(n * frac))
            K, max_val, c = build_ap_construction(n, m)
            alpha, beta = measure_ap_params(n, K, max_val)
            ok, fail = verify_ap_covers(n, c, K)
            print(f"{n:>6} {m:>6} {frac:>6.2f} | {K:>12} {max_val:>20} | "
                  f"{alpha:>6.3f} {beta:>6.3f} | {alpha+beta:>10.3f} | {ok}")
        print()


if __name__ == "__main__":
    run_experiment(
        n_values=[30, 60, 120],
        m_fractions=[0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    )

    print("=" * 100)
    print("Interpretation:")
    print("If alpha+beta stays pinned near 1 across all m, the AP structure")
    print("(via this simple b=0, c=lcm(1..m) construction) is NOT bending the")
    print("curve below the trivial line -- it's just re-deriving the same")
    print("tradeoff bucketing already gave us, dressed as an AP.")
    print()
    print("This is consistent with the paper's own statement that achieving")
    print("alpha < 1-beta is an OPEN problem even with AP structure imposed --")
    print("our simple lcm-based c doesn't exploit anything beyond what")
    print("non-AP bucketing already exploited. A genuine improvement would")
    print("need a cleverer choice of c (or nonzero b) that makes gcd(i,c)")
    print("large for i > m too, not just i <= m.")
