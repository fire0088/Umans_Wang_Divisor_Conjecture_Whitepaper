"""
'Fractal exponents / log 10' -> test self-similar / digit-restricted (Cantor-like)
sets and log/geometric-scaled sets, using the same bundling metric that caught
squares (primes in (n/2,n] per difference vs generic).

Candidates:
[A] base-b digit-restricted set (Cantor-like fractal): numbers whose base-b digits
    lie in a restricted set D. Classic self-similar structure.
[B] multi-scale / hierarchical GAP: S = sum of terms at geometric scales
    (b^0, b^1, b^2, ...), a 'fractal' arithmetic structure.
[C] log-spaced (geometric) element sizes.
Compare bundling to generic and to squares (the known winner).
"""
import math, random
from sympy import primerange, factorint

def primes_per(diffs, P, sample=400):
    if not diffs: return 0.0
    ds=random.sample(diffs, min(sample,len(diffs)))
    return sum(sum(1 for p in factorint(d) if p in P) for d in ds)/len(ds)

def digit_restricted(b, digits, ndig, count, rng, B):
    """Cantor-like: base-b numbers using only allowed digits."""
    S=set()
    tries=0
    while len(S)<count and tries<count*50:
        tries+=1
        v=0
        for _ in range(ndig):
            v=v*b+rng.choice(digits)
        if 0<v<=B: S.add(v)
    return list(S)

def hierarchical(b, scales, coeffs, count, rng, B):
    """S = sum c_i b^{k_i}: multi-scale fractal arithmetic set."""
    S=set(); tries=0
    while len(S)<count and tries<count*50:
        tries+=1
        v=sum(rng.choice(coeffs)*(b**k) for k in scales)
        if 0<v<=B: S.add(v)
    return list(S)

print("Bundling (primes in (n/2,n] per difference): fractal candidates vs baselines")
print(f"{'n':>5} {'generic':>8} {'squares':>8} {'Cantor-b3':>10} {'Cantor-b10':>11} {'hierarch':>9}")
for n in [1000, 2000]:
    P=set(primerange(n//2+1,n+1)); rng=random.Random(0); B=n*n*8
    # generic
    S=rng.sample(range(1,B+1),150); gen=[abs(a-b) for a in S for b in S if a!=b]
    # squares
    rc=int(B**0.5); A=rng.sample(range(1,rc+1),150); sq=[abs(a*a-b*b) for a in A for b in A if a!=b]
    # Cantor base 3, digits {0,1} (classic Cantor set)
    c3=digit_restricted(3,[0,1],int(math.log(B,3))+1,150,rng,B)
    d3=[abs(a-b) for a in c3 for b in c3 if a!=b]
    # Cantor base 10, digits {0,1,2} ('log 10' flavor)
    c10=digit_restricted(10,[0,1,2],int(math.log(B,10))+1,150,rng,B)
    d10=[abs(a-b) for a in c10 for b in c10 if a!=b]
    # hierarchical multi-scale
    h=hierarchical(2,list(range(0,int(math.log(B,2)))),[0,1],150,rng,B)
    dh=[abs(a-b) for a in h for b in h if a!=b]
    print(f"{n:>5} {primes_per(gen,P):>8.3f} {primes_per(sq,P):>8.3f} "
          f"{primes_per(d3,P):>10.3f} {primes_per(d10,P):>11.3f} {primes_per(dh,P):>9.3f}", flush=True)
print()
print("If any fractal column > squares: self-similar structure helps bundling.")
print("If ~generic or below: digit-restriction doesn't aid large-prime divisibility")
print("(likely: fractal sets control ADDITIVE structure, not MULTIPLICATIVE richness")
print("of differences -- which is what covering needs).")
