"""
Testing the discrete-log construction directly:

  S = {g^1, g^2, ..., g^L},  T = {1}

Then s - t = g^i - 1, and a classical fact (Fermat/Gauss, via the theory
of indices / primitive roots, ~1801) says:

    p | (g^i - 1)   <=>   ord_p(g) | i

So this S,T pair covers prime p (in the n-divisor sense) iff p's
multiplicative order under g divides some i <= L. The natural minimal
choice is i = ord_p(g) itself. So we ask directly: for primes p <= n,
how does ord_p(g) distribute? If many primes have SMALL order under a
fixed g, a small L covers them very cheaply. If orders are generically
large (close to p-1), this construction alone won't help much for those
primes -- but it might still cheaply dispatch with a useful FRACTION of
primes, leaving a smaller "hard core" for other techniques (e.g. our
earlier random-partition + continued-fraction search) to mop up.

This connects to a real, studied quantity: the distribution of
multiplicative orders of a fixed base mod p (related to Artin's
conjecture on primitive roots, and to "smooth shifted primes" -- primes
p for which p-1 is smooth, which underlies Pollard's p-1 algorithm).
"""

from sympy import primerange, factorint


def multiplicative_order(g, p):
    """Order of g mod p, via the standard divide-down-from-(p-1) method."""
    if p == 2:
        return 1
    phi = p - 1
    order = phi
    factors = factorint(phi)
    for prime_factor in factors:
        while order % prime_factor == 0 and pow(g, order // prime_factor, p) == 1:
            order //= prime_factor
    return order


def analyze_order_distribution(n, bases):
    primes = [p for p in primerange(2, n + 1)]
    print(f"n={n}, {len(primes)} primes")
    print()
    print(f"{'g':>4} | {'L (budget)':>10} {'#covered':>9} {'fraction':>9} | "
          f"{'log2(L)':>8} vs {'log2(n) baseline':>17}")
    print("-" * 75)

    import math
    log2_n = math.log2(n) if n > 1 else 1

    for g in bases:
        orders = {}
        for p in primes:
            if p == g or math.gcd(g, p) != 1:
                orders[p] = None  # g and p share a factor; this base can't cover p this way
                continue
            orders[p] = multiplicative_order(g, p)

        valid_orders = sorted(o for o in orders.values() if o is not None)
        if not valid_orders:
            continue

        # try several coverage budgets L (exponent bound) and see how many
        # primes have order <= L
        for frac in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
            L = max(1, int(n * frac))
            covered = sum(1 for o in valid_orders if o <= L)
            fraction = covered / len(primes)
            print(f"{g:>4} | {L:>10} {covered:>9} {fraction:>9.2%} | "
                  f"{math.log2(L):>8.2f} vs {log2_n:>17.2f}")
        print()


if __name__ == "__main__":
    analyze_order_distribution(n=200, bases=[2, 3, 5, 7])
