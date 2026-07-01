"""
Generalizing to k-dimensional generalized APs:

  S = {B + j1*b1 + j2*b2 + ... + jk*bk : 0<=j_i<=d_i}

This gives a rank-(k+1) lattice of covolume U (the full primorial):
  v0 = (U, 0, 0, ..., 0)
  v1 = (-W1, 1, 0, ..., 0)
  v2 = (-W2, 0, 1, ..., 0)
  ...
  vk = (-Wk, 0, ..., 0, 1)

Minkowski's theorem predicts a vector of size O(U^(1/(k+1))) exists.
We test: does increasing k (lattice dimension) actually drive the
achieved exponent down toward 1/(k+1), independent of how many total
cells (d1+1)*(d2+1)*...*(dk+1) we use?
"""

import math
import random
from fractions import Fraction
from sympy import primerange


def prod(lst):
    p = 1
    for x in lst:
        p *= x
    return p


def crt_idempotents_kd(grid):
    cells = list(grid.items())
    U_list = [prod(primes) for (_, primes) in cells]
    U = prod(U_list)
    V = {}
    for (coords, _), Ui in zip(cells, U_list):
        Mi = U // Ui
        Ti = pow(Mi, -1, Ui)
        V[coords] = (Mi * Ti) % U
    return U, V


def random_kd_grid(primes, dims, seed):
    rng = random.Random(seed)
    ranges = [range(d + 1) for d in dims]
    cells_coords = []

    def cartesian(ranges):
        if not ranges:
            yield ()
            return
        for x in ranges[0]:
            for rest in cartesian(ranges[1:]):
                yield (x,) + rest

    cells_coords = list(cartesian(ranges))
    grid = {c: [] for c in cells_coords}
    for p in primes:
        cell = rng.choice(cells_coords)
        grid[cell].append(p)
    for c in cells_coords:
        if not grid[c]:
            grid[c] = [1]
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


def search_joint_kd_lattice(primes, dims, grid_trials):
    kdim = len(dims)
    best = None
    for gseed in range(grid_trials):
        grid = random_kd_grid(primes, dims, gseed)
        U, V = crt_idempotents_kd(grid)

        Ws = []
        for axis in range(kdim):
            Wa = sum(coords[axis] * V[coords] for coords in V) % U
            Ws.append(Wa)

        basis = [[U] + [0] * kdim]
        for axis in range(kdim):
            row = [-Ws[axis]] + [0] * kdim
            row[1 + axis] = 1
            basis.append(row)

        reduced = lll_reduce(basis)

        for vec in reduced:
            Bval = vec[0]
            bs = vec[1:]
            check = (Bval + sum(bs[a] * Ws[a] for a in range(kdim))) % U
            if check != 0:
                continue
            if all(x == 0 for x in bs):
                continue
            # enumerate all terms in the generalized AP to verify/score
            def all_terms():
                ranges = [range(d + 1) for d in dims]

                def rec(idx, acc):
                    if idx == kdim:
                        yield acc
                        return
                    for j in range(dims[idx] + 1):
                        yield from rec(idx + 1, acc + j * bs[idx])
                yield from rec(0, Bval)

            terms = list(all_terms())
            if any(t == 0 for t in terms):
                continue
            score = max(abs(Bval), max(abs(x) for x in bs))
            if best is None or score < best[2]:
                best = (Bval, bs, score, terms)
    return best


def run(n, dims, grid_trials):
    primes = list(primerange(2, n + 1))
    log_U_bits = sum(p.bit_length() for p in primes)
    count = 1
    for d in dims:
        count *= (d + 1)
    kdim = len(dims)
    predicted_bits = log_U_bits / (kdim + 1)

    result = search_joint_kd_lattice(primes, dims, grid_trials)
    if result is None:
        print(f"n={n}, dims={dims}: no solution found")
        return None
    Bval, bs, score, terms = result
    uncovered = [p for p in primes if not any(t % p == 0 for t in terms)]
    bits = score.bit_length()

    ln_n = math.log(n)
    alpha = math.log(bits * math.log(2)) / ln_n if bits > 0 else 0
    beta_actual = math.log(count) / ln_n if count > 1 else 0

    ok = "YES" if not uncovered else f"NO {uncovered}"
    print(f"n={n:5d} k={kdim} dims={dims} count={count:4d} | "
          f"bits={bits:5d} (predicted~{predicted_bits:.0f}) alpha={alpha:.3f} beta={beta_actual:.3f} | {ok}")
    return alpha


if __name__ == "__main__":
    n = 400
    print(f"--- Fixed n={n}, increasing lattice dimension k ---")
    for k in [1, 2, 3, 4, 5, 6]:
        dims = [1] * k  # smallest possible grid per dimension (2 values each)
        run(n=n, dims=dims, grid_trials=4)
