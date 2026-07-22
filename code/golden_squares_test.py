"""
Test (a) golden ratio phi and (b) denser squares constructions for prime bundling.

Golden ratio motivation: BSSZ's Lemma 3.4 literally uses phi=(1+sqrt5)/2 for unit-
lattice separation (u in {+-1} iff |sigma_i(u)| in (phi^-1,phi)). So phi-based sets
connect to the actual construction. Test:
  - Fibonacci/Lucas sets (phi-structured): S from Fibonacci numbers
  - phi-scaled: S = {round(phi^k)} or beatty sequence floor(k*phi)
  - denser squares: products of two square-ish factors, near-squares

Measure primes-in-(n/2,n] per difference (asymmetric S-T where relevant).
"""
import math, random
from sympy import primerange, factorint

PHI=(1+5**0.5)/2

def primes_per(diffs, P, sample=500):
    if not diffs: return 0.0
    ds=random.sample(diffs, min(sample,len(diffs)))
    return sum(sum(1 for p in factorint(d) if p in P) for d in ds)/len(ds)

def fib_set(count, B):
    F=[1,2]
    while F[-1]<=B and len(F)<count+5: F.append(F[-1]+F[-2])
    return [f for f in F if f<=B]

def beatty(count, B):
    return sorted({int(k*PHI) for k in range(1,count*3) if int(k*PHI)<=B})[:count]

def squares(count, B, rng):
    rc=int(B**0.5); A=rng.sample(range(1,rc+1),min(count,rc)); return [a*a for a in A]

def near_squares(count, B, rng):
    # a*b with a,b close (near-square rectangles) -- two large factors like squares
    rc=int(B**0.5); out=set()
    while len(out)<count:
        a=rng.randint(1,rc); b=rng.randint(a,min(rc,a+a//4+1))
        if a*b<=B: out.add(a*b)
    return list(out)

print("Bundling (primes in (n/2,n] per diff): golden-ratio & squares variants")
print(f"{'n':>5} {'generic':>8} {'squares':>8} {'near-sq':>8} {'Fibonacci':>10} {'Beatty phi':>11}")
for n in [1000, 2000]:
    P=set(primerange(n//2+1,n+1)); rng=random.Random(1); B=n*n*8; K=int(4*n**0.5)
    S=rng.sample(range(1,B+1),K); gen=primes_per([abs(a-b) for a in S for b in S if a!=b],P)
    sq=squares(K,B,rng); sqd=primes_per([abs(a-b) for a in sq for b in sq if a!=b],P)
    ns=near_squares(K,B,rng); nsd=primes_per([abs(a-b) for a in ns for b in ns if a!=b],P)
    fb=fib_set(K,B); fbd=primes_per([abs(a-b) for a in fb for b in fb if a!=b],P) if len(fb)>3 else 0
    bt=beatty(K,B); btd=primes_per([abs(a-b) for a in bt for b in bt if a!=b],P) if len(bt)>3 else 0
    print(f"{n:>5} {gen:>8.3f} {sqd:>8.3f} {nsd:>8.3f} {fbd:>10.3f} {btd:>11.3f}", flush=True)
print()
print("phi appears in BSSZ Lemma 3.4 (unit separation). Fibonacci/Beatty are the")
print("Z-native phi structures. If they beat squares: phi-structure helps bundling.")
print("near-squares tests if the 'two large factors' mechanism generalizes beyond")
print("exact squares (it should, if the mechanism is 'difference factors into 2 big').")
