"""
Sharpening #2 from the UW paper: A is ASYMMETRIC S-T (two separate sets), not S-S.
Re-test prime bundling with two sets, exploiting the BSSZ split: let S carry one
structure and T another, so differences s-t bundle large primes better than the
symmetric squares test (~1.5x).

Test several asymmetric pairings vs symmetric baseline and vs generic:
  - S squares, T squares (symmetric-ish baseline we had)
  - S = a*G (geometric/mult), T = box (additive)  [BSSZ-style]
  - S, T independent random (control)
Measure primes-in-(n/2,n] per difference s-t.
"""
import math, random
from sympy import primerange, factorint

def primes_per(diffs, P, sample=500):
    if not diffs: return 0.0
    ds=random.sample(diffs, min(sample,len(diffs)))
    return sum(sum(1 for p in factorint(d) if p in P) for d in ds)/len(ds)

def diffs_ST(S,T):
    return [abs(s-t) for s in S for t in T if s!=t]

print("Asymmetric S-T bundling vs symmetric, primes in (n/2,n] per difference:")
print(f"{'n':>5} {'generic S-T':>12} {'squares S-S':>12} {'sq S - sq T':>12} {'G*box S-T':>11}")
for n in [1000, 2000]:
    P=set(primerange(n//2+1,n+1)); rng=random.Random(0); B=n*n*8
    K=int(3*n**0.5)
    # generic asymmetric
    S=rng.sample(range(1,B+1),K); T=rng.sample(range(1,B+1),K)
    g=primes_per(diffs_ST(S,T),P)
    # symmetric squares (our old test)
    rc=int(B**0.5); A=rng.sample(range(1,rc+1),K); sq=[a*a for a in A]
    sS=primes_per([abs(x-y) for x in sq for y in sq if x!=y],P)
    # asymmetric squares: S=squares of one root set, T=squares of another
    A2=rng.sample(range(1,rc+1),K); sqT=[a*a for a in A2]
    sST=primes_per(diffs_ST(sq,sqT),P)
    # BSSZ-style: S = g*base (mult structured), T = additive box
    base=rng.randint(2,50)
    Sg=sorted({base**0 * (rng.randint(1,rc)) for _ in range(K)})  # placeholder mult
    # better: S = {c * m : m in small mult set}, T = {c + a : a in AP}
    mult=[2**i*3**j for i in range(6) for j in range(6)]
    c=rng.randint(1,int(B**0.5))
    Sm=sorted({c*m for m in mult if c*m<=B})[:K]
    Tb=[c+i for i in range(K)]  # additive box near c
    gb=primes_per(diffs_ST(Sm,Tb),P) if Sm and Tb else 0
    print(f"{n:>5} {g:>12.3f} {sS:>12.3f} {sST:>12.3f} {gb:>11.3f}", flush=True)
print()
print("Compare: does asymmetric S-T (esp. squares or G*box) beat the ~1.5x that")
print("symmetric squares gave? If asym-squares > sym-squares: the two-set freedom")
print("helps. If G*box high: BSSZ-style split bundles better -- the right direction.")
