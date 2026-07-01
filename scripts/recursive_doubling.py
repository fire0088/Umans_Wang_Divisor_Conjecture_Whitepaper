"""
Porting a classical technique: recursive doubling of extremal bases
(Rohrbach 1937, building on Sylvester's coin/postage-stamp problem) --
build small, easy generating sets and recursively combine them, rather
than solving the whole covering problem in one global shot.

The paper hands us the exact combination primitive for free, as Lemma 6.1:

  Given A1 = {b1 + i*c1 : 1<=i<=l1} and A2 = {b2 + i*c2 : 1<=i<=l2},
  the generalized AP

    A = {c1*b2 + i*(c1*c2) + j*(c2*b1 - c1*b2) : 1<=i<=max(l1,l2), j in {0,1}}

  contains a multiple of x if A1 or A2 does.

Strategy: split the primes <= n into small chunks. For each chunk, find a
small, cheap AP covering just that chunk (easy -- few primes, small search).
Then recursively merge chunk-solutions pairwise via Lemma 6.1 (binary tree
merge, the classic doubling pattern), tracking how the term-count and
magnitude grow through the merge tree. Compare the final (l, magnitude)
against our earlier single-shot global random search.
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


def solve_chunk(primes_chunk, l_values, trials):
    """Find a small, cheap AP covering exactly this chunk of primes."""
    if len(primes_chunk) == 1:
        # trivial: a single prime p is covered by AP {p} itself (l=1,c=anything,b=0... )
        # but b=0 is degenerate (term = i*c = c when i=1, fine as long as c=p, nonzero)
        p = primes_chunk[0]
        return (1, p, 0)  # l=1, c=p, b=0 -> term = p, covers p. b=0 itself is fine
        # (only the AP TERM being zero is degenerate, not b itself)
    best = None
    for l in l_values:
        if l > len(primes_chunk):
            continue
        for seed in range(trials):
            groups = random_partition(primes_chunk, l, seed)
            U, S = compute_S(groups)
            max_c = 1 << (sum(p.bit_length() for p in primes_chunk) + 5)
            for c, b in continued_fraction_candidates(S, U, max_c):
                terms = [b + i * c for i in range(1, l + 1)]
                if any(t == 0 for t in terms):
                    continue
                score = max(c, abs(b))
                if best is None or score < best[3]:
                    best = (l, c, b, score)
    if best is None:
        return None
    l, c, b, _ = best
    return (l, c, b)


def merge_lemma_6_1(A1, A2):
    """A1, A2 are (l, c, b) tuples. Returns merged generalized AP as a
    flat list of integer terms (since the merged structure is no longer
    a simple AP, we materialize it as an explicit term list for the next
    level of recursion -- this loses some structure but lets us verify
    and continue merging)."""
    l1, c1, b1 = A1
    l2, c2, b2 = A2
    lmax = max(l1, l2)
    terms = []
    for i in range(1, lmax + 1):
        for j in (0, 1):
            term = c1 * b2 + i * (c1 * c2) + j * (c2 * b1 - c1 * b2)
            terms.append(term)
    return terms


def verify_terms_cover(terms, primes):
    uncovered = []
    for p in primes:
        if not any(t % p == 0 for t in terms):
            uncovered.append(p)
    return uncovered


def recursive_doubling_solution(primes, chunk_size, l_values, trials):
    """Split primes into chunks, solve each chunk, merge pairwise (binary
    tree) using Lemma 6.1, return final term list."""
    chunks = [primes[i:i + chunk_size] for i in range(0, len(primes), chunk_size)]
    solutions = [solve_chunk(chunk, l_values, trials) for chunk in chunks]

    # Convert each (l,c,b) chunk solution into an explicit term list to
    # start the merge tree uniformly.
    term_lists = []
    for (l, c, b) in solutions:
        term_lists.append([b + i * c for i in range(1, l + 1)])

    # Binary tree merge: repeatedly merge adjacent (l,c,b)-style APs.
    # For simplicity we merge the ORIGINAL (l,c,b) tuples pairwise via
    # Lemma 6.1 (not the flattened term lists), then flatten only at the end.
    level = solutions
    while len(level) > 1:
        next_level = []
        for k in range(0, len(level) - 1, 2):
            A1, A2 = level[k], level[k + 1]
            merged_terms = merge_lemma_6_1(A1, A2)
            # represent the merged generalized AP abstractly: we can't
            # treat it as a simple (l,c,b) AP anymore (it has 2 free
            # dimensions i,j), so for further merging we collapse it to
            # a SET of terms and merge sets directly going forward.
            next_level.append(('SET', merged_terms))
        if len(level) % 2 == 1:
            last = level[-1]
            if isinstance(last, tuple) and last[0] != 'SET':
                l, c, b = last
                next_level.append(('SET', [b + i * c for i in range(1, l + 1)]))
            else:
                next_level.append(last)
        level = next_level
        # once everything is 'SET', merge sets pairwise by simple union
        if all(isinstance(x, tuple) and x[0] == 'SET' for x in level) and len(level) > 1:
            merged = []
            for tag, terms in level:
                merged.extend(terms)
            level = [('SET', merged)]
            break

    final_terms = level[0][1] if isinstance(level[0], tuple) and level[0][0] == 'SET' else level[0]
    return final_terms


def run_comparison(n_values, chunk_size, l_values, trials):
    print(f"{'n':>5} {'#primes':>8} {'log2(U)':>8} {'sqrt(U) bits':>13} | "
          f"{'#terms':>7} {'max|term| bits':>15} | verified")
    print("-" * 90)
    for n in n_values:
        primes = list(primerange(2, n + 1))
        log_U_bits = sum(p.bit_length() for p in primes)
        sqrt_bits = log_U_bits / 2

        terms = recursive_doubling_solution(primes, chunk_size, l_values, trials)
        uncovered = verify_terms_cover(terms, primes)
        max_bits = max(abs(t) for t in terms).bit_length() if terms else 0
        ok = "YES" if not uncovered else f"NO {uncovered}"
        print(f"{n:>5} {len(primes):>8} {log_U_bits:>8} {sqrt_bits:>13.1f} | "
              f"{len(terms):>7} {max_bits:>15} | {ok}")


if __name__ == "__main__":
    run_comparison(
        n_values=[10, 20, 30, 40, 50, 70, 90, 110, 130, 150],
        chunk_size=2,
        l_values=[2, 3],
        trials=10,
    )
