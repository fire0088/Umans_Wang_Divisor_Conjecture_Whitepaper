"""
Star/chain-structured construction, inspired by addition-CHAIN structure
(each step depends only on a shared base, not on combinations of
previous steps -- the "star chain" structure from the addition-chain
literature, as opposed to the full hypercube generalized AP).

S = {B, B+b1, B+b2, ..., B+bk}  (k+1 terms, NOT 2^k)

Each prime is assigned to ONE slot: slot 0 means p | B; slot i (i>=1)
means p | (B+bi). Crucially, bi only appears in slot i's constraint --
so we have one free real-valued unknown per slot, all sharing only B.

This is a rank-(k+1) lattice (B, b1, ..., bk) with covolume U (same
Minkowski bound as the hypercube), but COUNT = k+1 (linear in k)
instead of 2^k (exponential in k) -- if this works, it gives much more
flexible control over where on the alpha+beta=1 line we land, without
the alpha,beta<1/2 barrier being broken.
"""

import math
from fractions import Fraction
from sympy import primerange


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def crt_idempotents(groups):
    """groups[0] = primes for slot 0 (B alone), groups[1..k] = primes
    for slots 1..k (B + b_i)."""
    U_list = [prod(g) for g in groups]
    U = prod(U_list)
    V = []
    for Ui in U_list:
        Mi = U // Ui
        Ti = pow(Mi, -1, Ui)
        Vi = (Mi * Ti) % U
        V.append(Vi)
    return U, V


def lll_reduce(basis, delta=Fraction(3, 4)):
    B = [row[:] for row in basis]
    n = len(B)

    def dot(u, v):
        return sum(Fraction(a) * Fraction(b) for a, b in zip(u, v))

    def gram_schmidt():
        Bstar = []
        mu = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            vi = [Fraction(x) for x in B[i]]
            for j in range(i):
                mu[i][j] = dot(B[i], Bstar[j]) / dot(Bstar[j], Bstar[j])
                vi = [vi[t] - mu[i][j] * Bstar[j][t] for t in range(len(vi))]
            Bstar.append(vi)
        return Bstar, mu

    k = 1
    while k < n:
        Bstar, mu = gram_schmidt()
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q != 0:
                B[k] = [B[k][t] - q * B[j][t] for t in range(len(B[k]))]
        Bstar, mu = gram_schmidt()
        lhs = dot(Bstar[k], Bstar[k])
        rhs = (delta - mu[k][k - 1] ** 2) * dot(Bstar[k - 1], Bstar[k - 1])
        if lhs >= rhs:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            k = max(k - 1, 1)
    return B


def random_star_partition(primes, k, seed):
    """Assign each prime to one of (k+1) slots: 0 (B alone), 1..k
    (B+b_i)."""
    import random
    rng = random.Random(seed)
    groups = [[] for _ in range(k + 1)]
    for p in primes:
        groups[rng.randrange(k + 1)].append(p)
    for g in groups:
        if not g:
            g.append(1)
    return groups


def search_star(primes, k, trials):
    """For each random slot-assignment, build the rank-(k+1) lattice
    (B, b1,...,bk) with relation B + sum_{i in slot} ... handled via
    idempotents, and LLL-reduce to find a short vector."""
    best = None
    for seed in range(trials):
        groups = random_star_partition(primes, k, seed)
        U, V = crt_idempotents(groups)
        # V[0] is the idempotent for slot 0 (B alone: no b_i contributes)
        # V[i] for i=1..k corresponds to slot i (B + b_i)
        # Lattice relation: B ≡ 0 (mod U_0), and B + b_i ≡ 0 (mod U_i)
        # Equivalently: B ≡ -sum_i b_i * [indicator of being needed] ...
        # We build via: target congruence is B*V[0]-weighted plus per-slot
        # Construct basis directly: B's coefficient ties all slots together.
        # B ≡ 0 (mod U_0) and B ≡ -b_i (mod U_i) for i=1..k.
        # Using CRT idempotents: define
        #   Bbase = 0 (since B must be ≡0 mod U_0 from slot 0 -- but we
        #   want freedom, so instead fold slot 0 into the lattice too)
        # Simpler: treat ALL k+1 unknowns (B, b1,...,bk) via idempotents
        # directly, each V[i] ties to exactly one unknown's constraint.
        kdim = k  # b1..bk free vars; B is the "always-present" var
        Ws = []
        for i in range(1, k + 1):
            Ws.append(V[i])  # B + b_i ≡ 0 (mod U_i) => coefficient on b_i is V[i]... handled via lattice below

        # Lattice rows: (U,0,...,0), and for each i: (-V[i]-ish term,...)
        # We need B + b_i*1 ≡ 0 mod U_i, and B ≡ 0 mod U_0.
        # Combine via idempotents: target T = sum_i b_i * V[i] (mod U),
        # we want B + T ≡ 0 (mod U) AND the slot-0 constraint is
        # automatically satisfied since V[0] ensures mod U_0 all other
        # V[i]≡0, so T≡0 (mod U_0), giving B≡0 (mod U_0) as required.
        basis = [[U] + [0] * kdim]
        for i in range(kdim):
            row = [-Ws[i]] + [0] * kdim
            row[1 + i] = 1
            basis.append(row)

        reduced = lll_reduce(basis)
        for vec in reduced:
            Bval = vec[0]
            bs = vec[1:]
            check = (Bval + sum(bs[i] * Ws[i] for i in range(kdim))) % U
            if check != 0:
                continue
            terms = [Bval] + [Bval + bs[i] for i in range(kdim)]
            if any(t == 0 for t in terms):
                continue
            score = max(abs(x) for x in [Bval] + list(bs))
            if best is None or score < best[2]:
                best = (Bval, bs, score, terms)
    return best




def run_balanced_point(n_values, trials):
    print("TARGETING THE BALANCED POINT alpha=beta=1/2 (minimizing max(alpha,beta))")
    print(f"{'n':>6} {'k':>4} {'count':>6} | {'bits':>6} | {'alpha':>7} {'beta':>7} | "
          f"{'max(a,b)':>9} {'exponent':>9} | verified")
    print("-" * 90)
    for n in n_values:
        primes = list(primerange(2, n + 1))
        log_U_bits = sum(p.bit_length() for p in primes)
        k = max(1, round(math.sqrt(n)) - 1)
        result = search_star(primes, k, trials)
        if result is None:
            print(f"{n:>6}  no solution")
            continue
        Bval, bs, score, terms = result
        uncovered = [p for p in primes if not any(t % p == 0 for t in terms)]
        bits = score.bit_length()
        count = k + 1
        ln_n = math.log(n)
        alpha = math.log(bits * math.log(2)) / ln_n if bits > 0 else 0
        beta = math.log(count) / ln_n if count > 1 else 0
        mx = max(alpha, beta)
        ok = "YES" if not uncovered else f"NO {uncovered}"
        print(f"{n:>6} {k:>4} {count:>6} | {bits:>6} | {alpha:>7.3f} {beta:>7.3f} | "
              f"{mx:>9.3f} {1+mx:>9.3f} | {ok}")


if __name__ == "__main__":
    run_balanced_point([300, 400, 600, 800, 1000], trials=2)
