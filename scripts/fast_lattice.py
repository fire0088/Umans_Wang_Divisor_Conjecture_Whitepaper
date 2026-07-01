"""
Fast lattice reduction: floating-point LLL (the standard practical
approach, used by real implementations like fplll) with a final EXACT
integer verification step, plus a small-block exact enumeration pass
(BKZ-flavored) that searches small integer combinations of a few basis
vectors at a time for an even shorter vector than plain LLL finds.

This targets the exact bottleneck identified earlier: exact-fraction
Gram-Schmidt scaling roughly as k^4 because numerator/denominator sizes
grow throughout the algorithm. Floating point avoids this entirely;
exactness is restored at the end by directly checking the integer
relation, not by trusting the floats.
"""

import math
import itertools
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


def random_star_partition(primes, k, seed):
    import random
    rng = random.Random(seed)
    groups = [[] for _ in range(k + 1)]
    for p in primes:
        groups[rng.randrange(k + 1)].append(p)
    for g in groups:
        if not g:
            g.append(1)
    return groups


# ---------------------------------------------------------------------
# Floating-point LLL (fast, standard practical approach)
# ---------------------------------------------------------------------
def lll_reduce_float(int_basis, delta=0.75):
    """LLL using floats for Gram-Schmidt (fast), operating on integer
    basis vectors throughout. To avoid float64 overflow (lattice entries
    can be hundreds of bits, and squaring them for norms would overflow
    double precision), we maintain a SCALED shadow copy for floating
    point decisions, but apply every row operation (subtract, swap) to
    the exact integer basis -- so correctness never depends on the
    floats, only which reduction path is taken does.
    """
from mpmath import mp, mpf


def lll_reduce_float(int_basis, delta=0.75, extra_precision=80):
    """LLL using arbitrary-precision floats (mpmath) for Gram-Schmidt.
    Plain float64 (53-bit mantissa) was tried first and found to lose
    essentially all the information LLL needs: our lattice entries are
    hundreds of bits long, and the fine-grained DIFFERENCES between
    them -- not just their magnitude -- are exactly what the algorithm
    must exploit to find short vectors. A fixed-precision float64 scale
    discards that. mpmath lets us set precision to match (plus margin),
    avoiding exact-fraction arithmetic's unbounded denominator growth
    while retaining the precision exact integers of this size need.
    """
    B = [row[:] for row in int_basis]
    n = len(B)

    max_bits = max((x.bit_length() for row in B for x in row if x != 0), default=1)
    mp.prec = max_bits + extra_precision

    def gram_schmidt():
        Bf = [[mpf(x) for x in row] for row in B]
        Bstar = [[mpf(0)] * n for _ in range(n)]
        mu = [[mpf(0)] * n for _ in range(n)]
        norms = [mpf(0)] * n
        for i in range(n):
            vi = Bf[i][:]
            for j in range(i):
                if norms[j] != 0:
                    mu[i][j] = sum(Bf[i][t] * Bstar[j][t] for t in range(n)) / norms[j]
                for t in range(n):
                    vi[t] -= mu[i][j] * Bstar[j][t]
            Bstar[i] = vi
            norms[i] = sum(x * x for x in vi)
        return Bstar, mu, norms

    k = 1
    iterations = 0
    max_iterations = 50 * n * n
    while k < n and iterations < max_iterations:
        iterations += 1
        Bstar, mu, norms = gram_schmidt()
        for j in range(k - 1, -1, -1):
            q = int(mp.nint(mu[k][j]))
            if q != 0:
                B[k] = [B[k][t] - q * B[j][t] for t in range(n)]
        Bstar, mu, norms = gram_schmidt()
        lhs = norms[k]
        rhs = (delta - mu[k][k - 1] ** 2) * norms[k - 1]
        if lhs >= rhs:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            k = max(k - 1, 1)
    return B


# ---------------------------------------------------------------------
# Small-block exact enumeration (BKZ-flavored): after float-LLL gives a
# decent basis, exhaustively search small integer combinations of each
# window of `block` consecutive basis vectors for a shorter vector.
# Exact (integer) arithmetic throughout -- only used on small blocks,
# so this is cheap despite being exhaustive.
# ---------------------------------------------------------------------
def block_enumerate(basis, block=4, coeff_range=2):
    n = len(basis)
    best_vecs = list(basis)
    improved = True
    while improved:
        improved = False
        for start in range(0, n - 1):
            end = min(start + block, n)
            window = best_vecs[start:end]
            w = len(window)
            if w < 2:
                continue
            cur_norm = min(sum(x * x for x in v) for v in window if any(v))
            best_combo = None
            best_norm = cur_norm
            for coeffs in itertools.product(range(-coeff_range, coeff_range + 1), repeat=w):
                if all(c == 0 for c in coeffs):
                    continue
                vec = [sum(coeffs[i] * window[i][t] for i in range(w)) for t in range(n)]
                if all(x == 0 for x in vec):
                    continue
                norm = sum(x * x for x in vec)
                if norm < best_norm:
                    best_norm = norm
                    best_combo = vec
            if best_combo is not None:
                # replace the first vector in the window with the improvement
                best_vecs[start] = best_combo
                improved = True
    return best_vecs


def search_star_fast(primes, k, trials, use_block_enum=True):
    best = None
    for seed in range(trials):
        groups = random_star_partition(primes, k, seed)
        U, V = crt_idempotents(groups)
        Ws = [V[i] for i in range(1, k + 1)]
        basis = [[U] + [0] * k]
        for i in range(k):
            row = [-Ws[i]] + [0] * k
            row[1 + i] = 1
            basis.append(row)

        reduced = lll_reduce_float(basis)
        if use_block_enum and k <= 30:  # block enumeration cost grows with k
            reduced = block_enumerate(reduced, block=4, coeff_range=2)

        for vec in reduced:
            Bval = vec[0]
            bs = vec[1:]
            # EXACT verification -- floats above only chose candidates,
            # this check is plain Python integer arithmetic
            check = (Bval + sum(bs[i] * Ws[i] for i in range(k))) % U
            if check != 0:
                continue
            terms = [Bval] + [Bval + bs[i] for i in range(k)]
            if any(t == 0 for t in terms):
                continue
            score = max(abs(x) for x in [Bval] + list(bs))
            if best is None or score < best[2]:
                best = (Bval, bs, score, terms)
    return best


if __name__ == "__main__":
    import time
    n = 400
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    ln_n = math.log(n)

    print(f"n={n}, log2(U)={log_U_bits} bits, target k for beta=0.5: {round(math.sqrt(n))-1}")
    print()
    print(f"{'k':>4} {'trials':>7} {'time(s)':>9} | {'bits':>6} {'alpha':>7} {'beta':>7} {'exponent':>9}")
    print("-" * 70)

    for k in [19, 30, 45]:
        t0 = time.time()
        result = search_star_fast(primes, k, trials=4)
        dt = time.time() - t0
        if result is None:
            print(f"{k:>4}  no solution  ({dt:.1f}s)")
            continue
        Bval, bs, score, terms = result
        uncovered = [p for p in primes if not any(t % p == 0 for t in terms)]
        bits = score.bit_length()
        count = k + 1
        alpha = math.log(bits * math.log(2)) / ln_n if bits > 0 else 0
        beta = math.log(count) / ln_n
        mx = max(alpha, beta)
        ok = "OK" if not uncovered else "FAIL"
        print(f"{k:>4} {10:>7} {dt:>9.1f} | {bits:>6} {alpha:>7.3f} {beta:>7.3f} {1+mx:>9.3f}  {ok}")
