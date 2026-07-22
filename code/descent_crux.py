"""
The crux is now precise and it's a LOAD-BALANCING question, not vertex-log:

Each slot s_k, for each incident edge carrying prime p, gets a REAL constraint
"s_k ≡ s_neighbor mod p". The star-graph shows: if a slot has many incident LARGE
primes, and its neighbors are already fixed, s_k is forced to a specific residue
mod (product of incident primes) -- and being DISTINCT can force it large.

BUT crucially: the neighbors are NOT pre-fixed -- we choose ALL slots together. The
honest question: is there a joint assignment of small integers consistent with all
congruences? The star analysis assumed center=0 then leaves forced; but we could
set leaves small and center forced instead -- SAME problem, the forcing just moves.

THE INVARIANT (this is the real math): sum over all slots isn't the point; the
binding quantity is: for the congruence system to have a solution in [0,B]^K, we
need the LATTICE L (covolume Q) to have K linearly independent vectors... no --
we need K DISTINCT POINTS of L in [0,B]^K, i.e. |L ∩ [0,B]^K| >= K.
Number of lattice points of covolume-Q lattice in a box B^K ≈ B^K / Q (when B^K>Q).
Need >= K, but really need the box to contain K points that are DISTINCT AS A
TUPLE -- actually we need ONE point of L in [0,B]^K with distinct coordinates.

So the REAL condition: does L (covolume Q ~ e^{n/2}) contain a point in the box
[0,B]^K with DISTINCT coordinates, B=e^{n^alpha}?
Box volume = B^K = e^{K n^alpha} = e^{n^{(1-alpha)/2} * n^alpha} = e^{n^{(1+alpha)/2}}.
Covolume Q = e^{n/2}. Box vol / covol = e^{n^{(1+alpha)/2} - n/2}.
Since (1+alpha)/2 < 1 for alpha<1, we have n^{(1+alpha)/2} << n/2, so
box vol / covol = e^{NEGATIVE HUGE} -> 0. The box contains ZERO lattice points
generically!
"""
import math
from sympy import primerange

print("The REAL condition: does covolume-Q lattice meet box [0,B]^K nontrivially?")
print(f"{'alpha':>6} {'n':>7} {'K':>5} {'log boxvol=K*n^a':>16} {'log covol=n/2':>14} {'boxvol/covol':>15}")
for alpha in [0.3,0.4]:
    for n in [10**4,10**6,10**8]:
        P=list(primerange(n//2+1,n+1)); logQ=sum(math.log(p) for p in P)
        per=max(1,int(n**alpha/math.log(n/2)))
        K=2
        while K*(K-1)//2*per<len(P): K+=1
        logbox=K*(n**alpha); logcov=logQ
        print(f"{alpha:>6} {n:>7.0e} {K:>5} {logbox:>16.0f} {logcov:>14.0f} "
              f"e^{logbox-logcov:>+.0f}", flush=True)
    print()
print("log boxvol - log covol = K*n^alpha - n/2 = n^{(1+alpha)/2} - n/2.")
print("For alpha<1, n^{(1+alpha)/2} << n/2, so this is HUGELY NEGATIVE:")
print("the box is EXPONENTIALLY smaller than the lattice covolume => generically")
print("ZERO lattice points in the box. This is the SAME 2beta+alpha>=1 boundary!")
print()
print("KEY: box vol >= covol REQUIRES K*n^alpha >= n/2, i.e. n^{(1-alpha)/2}*n^alpha")
print(">= n/2 => n^{(1+alpha)/2} >= n/2 => (1+alpha)/2 >= 1 => alpha>=1. IMPOSSIBLE.")
print("So a GENERIC lattice has no box point. UW needs a SPECIAL lattice whose")
print("points CLUSTER in the small box -- exactly the bounded-root-disc/unit-lattice")
print("property. The descent lemma = 'the congruence lattice clusters in the box'.")
print("This is NOT generic; it's the whole content. Verdict: descent lemma is")
print("EQUIVALENT to UW, not easier -- we've gone in a precise circle back to it.")
