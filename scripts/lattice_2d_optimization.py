"""
Proper lattice-based joint 2D optimization.

S_2D(b1,b2) = b1*W1 + b2*W2 (mod U) where W1 = sum_{j,k} j*V_{j,k} mod U,
W2 = sum_{j,k} k*V_{j,k} mod U are FIXED constants determined by the grid
partition. We want small (B, b1, b2) with B + b1*W1 + b2*W2 ≡ 0 (mod U).

This is a rank-3 integer lattice of covolume U:
    v1 = (U, 0, 0)
    v2 = (-W1, 1, 0)
    v3 = (-W2, 0, 1)

By Minkowski's convex body theorem, this lattice contains a nonzero
vector with all coordinates O(U^(1/3)) -- genuinely better than the
sqrt(U)=U^(1/2) floor everything else in this investigation has hit.
LLL reduction finds a provably short (within a known approximation
factor) basis vector in polynomial time.
"""

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
    """Standard LLL algorithm for an integer lattice basis (list of
    lists of ints). Returns a reduced basis."""
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
    best = None  # (B, b1, b2, score, grid_seed)
    for gseed in range(grid_trials):
        grid = random_2d_grid(primes, d1, d2, gseed)
        U, V = crt_idempotents_2d(grid)

        W1 = sum(j * V[(j, k)] for (j, k) in V) % U
        W2 = sum(k * V[(j, k)] for (j, k) in V) % U

        basis = [
            [U, 0, 0],
            [-W1, 1, 0],
            [-W2, 0, 1],
        ]
        reduced = lll_reduce(basis)

        for vec in reduced:
            B, b1, b2 = vec
            # check the lattice relation actually holds (sanity)
            if (B + b1 * W1 + b2 * W2) % U != 0:
                continue
            if b1 == 0 and b2 == 0:
                continue  # degenerate: no actual progression structure
            terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
            if any(t == 0 for t in terms):
                continue
            score = max(abs(B), abs(b1), abs(b2))
            if best is None or score < best[3]:
                best = (B, b1, b2, score)
    return best


def verify_2d_covers(B, b1, b2, d1, d2, primes):
    terms = [B + j * b1 + k * b2 for j in range(d1 + 1) for k in range(d2 + 1)]
    return [p for p in primes if not any(t % p == 0 for t in terms)], terms


def run(n, d1, d2, grid_trials):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    count = (d1 + 1) * (d2 + 1)
    cube_root_bits = log_U_bits / 3
    sqrt_bits = log_U_bits / 2
    print(f"n={n}, {len(primes)} primes, grid={d1+1}x{d2+1}={count} cells | "
          f"sqrt(U) bits={sqrt_bits:.1f}, cbrt(U) bits={cube_root_bits:.1f}")

    result = search_joint_2d_lattice(primes, d1, d2, grid_trials)
    if result is None:
        print("  No solution found.")
        return
    B, b1, b2, score = result
    uncovered, terms = verify_2d_covers(B, b1, b2, d1, d2, primes)
    bits = score.bit_length()
    print(f"  Best: B={B}, b1={b1}, b2={b2} -> magnitude_bits={bits}, count={count}, "
          f"verified={'YES' if not uncovered else 'NO ' + str(uncovered)}")


if __name__ == "__main__":
    for n in [150, 300, 500]:
        print("=" * 95)
        for (d1, d2) in [(1, 1), (1, 2), (2, 2)]:
            run(n=n, d1=d1, d2=d2, grid_trials=10)
        print()
