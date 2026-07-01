"""
Scaling test: grow the 2D grid count with n (count ~ n^beta for fixed
target beta), using the LLL lattice machinery, and track the resulting
alpha as n grows. This is the genuine test of whether lattice-based
joint optimization changes the asymptotic exponent, vs the constant-size
grid experiment which (we now understand) just matches the known
1/m floor for fixed m.

Predictions to check against:
  - trivial single-set bound (no difference-set structure): alpha ~ 1-beta
  - information-theoretic floor (WITH difference-set structure):
    alpha >= 1-2*beta
  - target (best possible):                                  alpha = beta = 1/3
"""

import math
from fractions import Fraction
from sympy import primerange


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def crt_idempotents_2d(grid):
    cells = list(grid.items())
    U_list = [prod(primes) for (_, primes) in cells]
    U = prod(U_list)
    V = {}
    for ((j, k), _), Ui in zip(cells, U_list):
        Mi = U // Ui
        Ti = pow(Mi, -1, Ui)
        V[(j, k)] = (Mi * Ti) % U
    return U, V


def random_2d_grid(primes, d1, d2, seed):
    import random
    rng = random.Random(seed)
    grid = {(j, k): [] for j in range(d1 + 1) for k in range(d2 + 1)}
    cells = list(grid.keys())
    for p in primes:
        cell = rng.choice(cells)
        grid[cell].append(p)
    for cell in cells:
        if not grid[cell]:
            grid[cell] = [1]
    return grid


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
                vi = [vi[k] - mu[i][j] * Bstar[j][k] for k in range(len(vi))]
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


def search_joint_2d_lattice(primes, d1, d2, grid_trials):
    best = None
    for gseed in range(grid_trials):
        grid = random_2d_grid(primes, d1, d2, gseed)
        U, V = crt_idempotents_2d(grid)
        W1 = sum(j * V[(j, k)] for (j, k) in V) % U
        W2 = sum(k * V[(j, k)] for (j, k) in V) % U
        basis = [[U, 0, 0], [-W1, 1, 0], [-W2, 0, 1]]
        reduced = lll_reduce(basis)
        for vec in reduced:
            B, b1, b2 = vec
            if (B + b1 * W1 + b2 * W2) % U != 0:
                continue
            if b1 == 0 and b2 == 0:
                continue
            terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
            if any(t == 0 for t in terms):
                continue
            score = max(abs(B), abs(b1), abs(b2))
            if best is None or score < best[3]:
                best = (B, b1, b2, score)
    return best


def verify_2d_covers(B, b1, b2, d1, d2, primes):
    terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
    return [p for p in primes if not any(t % p == 0 for t in terms)]


def run_scaling(n_values, beta_target, grid_trials):
    print(f"--- target beta = {beta_target} ---")
    print(f"{'n':>5} {'count target':>13} {'grid':>8} {'actual count':>13} | "
          f"{'bits':>6} {'alpha':>7} {'beta(actual)':>13} | verified")
    print("-" * 90)
    for n in n_values:
        primes = list(primerange(2, n + 1))
        count_target = max(2, n ** beta_target)
        # use a rectangular grid that more finely tracks the target,
        # rather than rounding both dimensions to the same square side
        d1 = max(1, round(count_target ** 0.5))
        d2 = max(1, round(count_target / d1))
        d1, d2 = d1 - 1, d2 - 1
        count = (d1 + 1) * (d2 + 1)
        if count > len(primes):
            scale = (len(primes) / count) ** 0.5
            d1 = max(0, round((d1 + 1) * scale) - 1)
            d2 = max(0, round((d2 + 1) * scale) - 1)
            count = (d1 + 1) * (d2 + 1)

        result = search_joint_2d_lattice(primes, d1, d2, grid_trials)
        if result is None:
            print(f"{n:>5}  no solution found")
            continue
        B, b1, b2, score = result
        uncovered = verify_2d_covers(B, b1, b2, d1, d2, primes)
        bits = score.bit_length()

        ln_n = math.log(n)
        alpha = math.log(bits * math.log(2)) / ln_n if bits > 0 else 0
        beta_actual = math.log(count) / ln_n if count > 1 else 0

        ok = "YES" if not uncovered else f"NO {uncovered}"
        print(f"{n:>5} {count_target:>13.1f} {f'{d1+1}x{d2+1}':>8} {count:>13} | "
              f"{bits:>6} {alpha:>7.3f} {beta_actual:>13.3f} | {ok}")
    print()


if __name__ == "__main__":
    n_values = [30, 60, 100, 150, 250, 400, 600, 900, 1300, 1800]
    for beta_target in [0.3, 0.4, 0.5]:
        run_scaling(n_values, beta_target, grid_trials=6)
