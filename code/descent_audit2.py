"""
(A) Verify the box-emptiness IS the proven 2beta+alpha>=1 bound restated.
(B) Audit descent_exact.py's claim 'small solutions beat Minkowski average' for a
    bug: was the comparison fair? (Bcap=sqrt(Q) caps the search -- if the TRUE min
    were above sqrt(Q), the search would miss it and falsely report 'beats avg'.)
"""
import math, random
from itertools import combinations
from collections import defaultdict
from sympy import primerange

# (A) identity check: box vol >= covol  <=>  2beta+alpha <= 1 boundary
print("(A) Is 'box empty' identical to the proven 2beta+alpha>=1?")
print("    box>=covol  <=>  K*logB >= logQ  <=>  K*n^alpha >= n/2 (approx).")
print("    With K=n^beta, logB=n^alpha: n^beta * n^alpha >= n^1/2 (logQ~n/2, but as")
print("    a POWER logQ=Theta(n), take log: beta+alpha vs 1). Wait -- logB=n^alpha is")
print("    already a log. Let me be careful with what's an exponent vs a log.")
print()
print("    B=e^{n^alpha} so logB=n^alpha. K=n^beta. logQ=Theta(n).")
print("    box nonempty needs K*logB >~ logQ: n^beta * n^alpha >~ n")
print("    => beta+alpha >= 1.  <-- THIS is the barrier alpha+beta>=1 !!")
print()
print("    So 'generic box nonempty' <=> alpha+beta>=1 (the BARRIER).")
print("    Covering forces box NONEMPTY (a solution IS a box point). So a solution")
print("    existing at alpha+beta<1 REQUIRES the special-clustering (non-generic).")
print("    The proven bound is 2beta+alpha>=1; the box/generic bound is alpha+beta>=1.")
print("    These are DIFFERENT lines. Let me check which the lattice count gives.")
print()
# Numerically: does generic lattice-point-count vanish at the counting floor
# (2beta+alpha=1) or only at alpha+beta=1?
print(f"{'alpha':>6} {'beta_floor':>10} {'2b+a':>6} {'a+b':>6} {'K*logB/logQ':>12} {'<1?':>5}")
for alpha in [0.3,0.4,0.45]:
    n=10**6
    P=list(primerange(n//2+1,n+1)); logQ=sum(math.log(p) for p in P)
    per=max(1,int(n**alpha/math.log(n/2)))
    K=2
    while K*(K-1)//2*per<len(P): K+=1
    beta=math.log(K)/math.log(n)
    ratio=K*(n**alpha)/logQ
    print(f"{alpha:>6} {beta:>10.3f} {2*beta+alpha:>6.2f} {alpha+beta:>6.2f} {ratio:>12.4f} {str(ratio<1):>5}", flush=True)
print()
print("At the counting floor 2beta+alpha=1, beta=(1-alpha)/2, so alpha+beta=(1+alpha)/2")
print("<1. So generic box is EMPTY (ratio<1) at the floor -> confirms: reaching the")
print("floor needs NON-generic clustering. Verdict stands and is now precise:")
print("descent lemma <=> 'special lattice clusters in box' <=> exactly the gap")
print("between proven 2beta+alpha>=1 and the desired alpha+beta<1. NOT a bug.")
print()
# (B) audit descent_exact Bcap
print("(B) descent_exact.py Bcap=sqrt(Q)+50: does capping bias 'beats average'?")
print("    Minkowski avg = sqrt(Q) per 2 coords ~ Q^{1/K}... the script compared")
print("    log(minS) to 0.5*logQ. If TRUE min > sqrt(Q), search (capped at sqrt(Q))")
print("    finds nothing and returns None, NOT a false 'beat'. Since it returned")
print("    values < 0.5logQ, those are REAL solutions found below the cap. So the")
print("    'beats average' claim is not biased by the cap -- a found solution is real.")
print("    (The cap could only cause FALSE NEGATIVES, not false positives.) OK.")
