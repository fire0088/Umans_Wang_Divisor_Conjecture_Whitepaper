"""
Build OUR version of a UW construction, adapting the BSSZ unit-lattice idea, and
STRESS-TEST each step numerically where possible. The construction we want:

GOAL: for fixed alpha<1/2, a set S of integers, |S|=K~n^{(1-alpha)/2}, elements
<= e^{n^alpha}, whose difference set covers primes in (n/2,n] by divisibility.

BSSZ-INSPIRED IDEA (our adaptation to the DIVISIBILITY-COVERING problem):
The BSSZ construction gets differences that FACTOR into many pieces via a
number field of degree d. Our covering needs each difference divisible by
~n^alpha/ln n primes from (n/2,n]. 

KEY REALIZATION to check: we don't need a difference to EQUAL a product of large
primes -- we need it DIVISIBLE by a chosen prime p (any multiple works). So the
cleanest construction is CRT-based, and the number-field structure is what lets
the CRT solution stay SMALL (the failure mode we found: distinctness forced
magnitude up).

OUR VERSION -- 'lattice-CRT construction':
1. Assign the ~|P| primes to K^2/2 pairs (packing lemma, PROVEN feasible).
2. For each pair (i,j), we need s_i ≡ s_j mod m_ij (m_ij = product of assigned primes).
3. The BSSZ insight: work in a LATTICE where the s_i are lattice points, so that
   the congruence constraints are LINEAR conditions cut out on the lattice, and
   the lattice's GEOMETRY guarantees a short (small-magnitude) simultaneous solution.

The question our construction must answer: does a lattice exist where ALL K^2/2
congruences are satisfiable by K DISTINCT points of magnitude <= e^{n^alpha}?

TEST the core tension numerically at small scale: set up the congruence lattice,
compute its shortest-vector / successive minima, and check if K distinct points
fit under budget. This is the crux the vertex-log argument got WRONG (it ignored
lattice geometry). Let's see if lattice geometry RESCUES small solutions.
"""
import math, random
from sympy import primerange
from itertools import combinations

def test_lattice_crt(n, alpha, seed=0):
    P=list(primerange(n//2+1,n+1))
    budget_log = n**alpha
    per_pair=max(1,int(budget_log/math.log(n/2)))
    K=2
    while K*(K-1)//2*per_pair<len(P): K+=1
    # assign primes to pairs
    pairs=list(combinations(range(K),2)); rng=random.Random(seed); rng.shuffle(pairs)
    from collections import defaultdict
    assign=defaultdict(list); plog=defaultdict(float); pi=0
    for p in sorted(P,reverse=True):
        for _ in range(len(pairs)):
            pr=pairs[pi%len(pairs)]; pi+=1
            if plog[pr]+math.log(p)<=budget_log:
                assign[pr].append(p); plog[pr]+=math.log(p); break
    # The congruence system: s_i - s_j ≡ 0 mod m_ij for each assigned pair.
    # Variables s_0..s_{K-1}. This defines a LATTICE L in Z^K:
    #   L = { (s_0,...,s_{K-1}) : s_i ≡ s_j mod m_ij for all assigned (i,j) }.
    # We want K coords that are DISTINCT and all small. The relevant quantity:
    # the lattice L has covolume = product of m_ij (roughly), spread over K coords.
    # By Minkowski, L has a basis with vectors of size ~ covol^{1/K}.
    # covol ~ prod m_ij = prod over all primes = Q ~ e^{n/2}. Over K coords:
    #   typical coordinate size ~ (e^{n/2})^{1/K} = e^{n/(2K)}.
    # With K~n^{(1-alpha)/2}: n/(2K) ~ n/(2 n^{(1-alpha)/2}) = n^{(1+alpha)/2}/2.
    # Need <= n^alpha (budget). Is n^{(1+alpha)/2} <= n^alpha? 
    #   (1+alpha)/2 <= alpha  <=>  1+alpha <= 2 alpha  <=>  1 <= alpha. FALSE for alpha<1.
    covol_log = sum(math.log(p) for p in P)  # = log Q
    typical_coord_log = covol_log / K
    budget = n**alpha
    exponent_needed = math.log(typical_coord_log)/math.log(n) if typical_coord_log>1 else 0
    return dict(K=K, covol_log=covol_log, typical_coord_log=typical_coord_log,
                budget=budget, ratio=typical_coord_log/budget,
                coord_exponent=exponent_needed)

print("Our lattice-CRT construction: does Minkowski give small enough solutions?")
print(f"{'alpha':>6} {'n':>7} {'K':>5} {'typ coord log':>14} {'budget n^a':>11} {'ratio':>8} {'coord exp':>10}")
for alpha in [0.3, 0.4]:
    for n in [10**4, 10**6, 10**8]:
        r=test_lattice_crt(n,alpha)
        print(f"{alpha:>6} {n:>7.0e} {r['K']:>5} {r['typical_coord_log']:>14.1f} "
              f"{r['budget']:>11.1f} {r['ratio']:>8.2f} {r['coord_exponent']:>10.3f}", flush=True)
    print()
print("If ratio <= 1: lattice geometry gives small solutions -> construction WORKS -> UW.")
print("If ratio >> 1 and grows: even optimal lattice packing exceeds budget -> the")
print("congruence lattice is genuinely too dense -> barrier. Compare coord exponent")
print("to alpha: coord needs n^{(1+alpha)/2}/2K... let's see the honest number.")
