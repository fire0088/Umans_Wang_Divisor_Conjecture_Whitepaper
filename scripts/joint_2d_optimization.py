"""
True joint 2D generalized AP optimization.

S = {B + j*b1 + k*b2 : 0<=j<=d1, 0<=k<=d2}, T = {0}.

We want: for every prime p <= n, exists (j,k) in the grid with
p | (B + j*b1 + k*b2).

Construction: partition primes into a (d1+1)x(d2+1) grid of cells. For
FIXED (b1, b2) (which we sweep over), each cell (j,k) imposes a single
linear constraint on B: B ≡ -(j*b1 + k*b2)  (mod U_{j,k}), where U_{j,k}
is the product of primes assigned to that cell. Since the U_{j,k} are
pairwise coprime, CRT gives a unique combined target S_2D mod U such
that finding small B reduces to the SAME 1D continued-fraction problem
we've already solved -- but now S_2D itself depends on (b1,b2), so we
get to jointly search over (b1,b2,B) instead of just one parameter.

This is the "true joint optimization" version: both progressions attack
the SAME full prime set together, rather than splitting the set in half
and merging two independent solutions (which we already tried and found
to lose).
"""

import random
from sympy import primerange


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def crt_idempotents_2d(grid):
    """grid: dict (j,k) -> list of primes assigned to that cell."""
    cells = list(grid.items())
    U_list = [prod(primes) for (_, primes) in cells]
    U = prod(U_list)
    V = {}
    for ((j, k), _), Ui in zip(cells, U_list):
        Mi = U // Ui
        Ti = pow(Mi, -1, Ui)
        V[(j, k)] = (Mi * Ti) % U
    return U, V


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


def random_2d_grid(primes, d1, d2, seed):
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


def verify_2d_covers(B, b1, b2, d1, d2, primes):
    terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
    uncovered = [p for p in primes if not any(t % p == 0 for t in terms)]
    return uncovered, terms


def search_joint_2d(primes, d1, d2, grid_trials, b1b2_range):
    """For each grid partition, sweep over small (b1,b2) pairs, and for
    each compute S_2D and find the best B via continued fractions."""
    log_U_bits = sum(p.bit_length() for p in primes)
    max_c = 1 << (log_U_bits + 5)

    best = None  # (B, b1, b2, score)
    for gseed in range(grid_trials):
        grid = random_2d_grid(primes, d1, d2, gseed)
        U, V = crt_idempotents_2d(grid)

        for b1 in range(1, b1b2_range + 1):
            for b2 in range(1, b1b2_range + 1):
                # S_2D ≡ (j*b1 + k*b2) mod U_{j,k} for each cell, built
                # via CRT idempotents. Since b1,b2 are fixed, finding the
                # smallest |B| with B ≡ -S_2D (mod U) is just the signed
                # residue directly (no continued fraction needed here --
                # that machinery was for finding a free multiplier c,
                # which doesn't apply once b1,b2 are already fixed).
                S_2D = sum(((j * b1 + k * b2) * V[(j, k)]) for (j, k) in V) % U
                r = S_2D % U
                B = -r if r <= U - r else U - r

                terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
                if any(t == 0 for t in terms):
                    continue
                score = max(abs(B), b1, b2)
                if best is None or score < best[3]:
                    best = (B, b1, b2, score)
    return best


def run(n, d1, d2, grid_trials, b1b2_range):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    count = (d1 + 1) * (d2 + 1)
    print(f"n={n}, {len(primes)} primes, grid={d1+1}x{d2+1}={count} cells, "
          f"sqrt(U) baseline = {log_U_bits/2:.1f} bits")

    result = search_joint_2d(primes, d1, d2, grid_trials, b1b2_range)
    if result is None:
        print("No solution found in search budget.")
        return
    B, b1, b2, score = result
    uncovered, terms = verify_2d_covers(B, b1, b2, d1, d2, primes)
    bits = score.bit_length()
    print(f"Best: B={B}, b1={b1}, b2={b2}  ->  magnitude_bits={bits}, count={count}, "
          f"verified={'YES' if not uncovered else 'NO ' + str(uncovered)}")
    return count, bits, not uncovered


if __name__ == "__main__":
    for n in [150, 300]:
        print("=" * 90)
        for (d1, d2) in [(1, 1), (1, 2), (2, 2)]:
            run(n=n, d1=d1, d2=d2, grid_trials=8, b1b2_range=150)
            print()
