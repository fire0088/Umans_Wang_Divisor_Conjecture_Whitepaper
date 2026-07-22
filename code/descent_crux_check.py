"""
Audit descent_crux.py. Two concerns:
(1) Lattice dimension/covolume: L={s in Z^K: s_i≡s_j mod m_ij} is FULL-RANK in Z^K.
    Its covolume in R^K = [Z^K : L] = product of constraint indices. Each prime p on
    edge (i,j) imposes s_i≡s_j mod p, index p. Primes distinct across edges => total
    index = prod over all primes = Q. So covol(L)=Q, dimension K. CORRECT.
    The box [0,B]^K has volume B^K. #(L ∩ box) ≈ B^K/Q. So the comparison K*logB vs
    logQ IS the right one. Good -- the verdict's inequality is dimensionally fine.
(2) BUT: the '#points ≈ vol/covol' heuristic needs box SIDE B >= covol^{1/K} per
    dimension to be meaningful, AND we don't need MANY points -- we need ONE with
    distinct coords. More importantly: is K*n^alpha vs n/2 the right knife-edge, or
    does the counting-floor K (with its 1/log factor) change it? CHECK exactly.
"""
import math
from sympy import primerange

print("Exact check of the knife-edge K*logB vs logQ at the TRUE counting floor:")
print(f"{'alpha':>6} {'n':>8} {'K_floor':>8} {'K*n^a':>12} {'logQ=n/2ish':>12} {'K*n^a / logQ':>13}")
for alpha in [0.3,0.4,0.45]:
    for n in [10**4,10**6,10**8]:
        P=list(primerange(n//2+1,n+1)); logQ=sum(math.log(p) for p in P)
        # TWO ways to compute K: (a) with 1/log factor (code), (b) pure n^{(1-a)/2}
        per=max(1,int(n**alpha/math.log(n/2)))
        Ka=2
        while Ka*(Ka-1)//2*per<len(P): Ka+=1
        KlogB=Ka*(n**alpha)
        print(f"{alpha:>6} {n:>8.0e} {Ka:>8} {KlogB:>12.0f} {logQ:>12.0f} {KlogB/logQ:>13.4f}", flush=True)
    print()
print("If K*n^a / logQ < 1 (and shrinking): box vol << covol, generic lattice has")
print("no box point -> verdict HOLDS (descent needs special clustering = UW).")
print("If ratio ~1 or >1: the verdict was WRONG and the box is big enough generically.")
print()
print("Note: K_floor already SATISFIES K(K-1)/2 * per >= |P|, and per ~ n^a/log,")
print("so K*(K*per) ~ K^2 per ~ |P| ~ n/log n ~ logQ. Thus K*n^a = K*per*log ~")
print("(logQ/K)*... let's just trust the computed ratio above.")
