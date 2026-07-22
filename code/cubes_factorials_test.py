"""
Two ideas:
[A] Difference of cubes done RIGHT: a^3-b^3=(a-b)(a^2+ab+b^2). The quadratic
    factor is a distinct large object. Also test sum/mixed: does the 2-factor
    structure help even if raw magnitude hurt higher powers? Compare bundling of
    the (a-b)(a^2+ab+b^2) form specifically, and also 2-var forms that factor
    MORE: a^6-b^6=(a-b)(a+b)(a^2+ab+b^2)(a^2-ab+b^2) -- FOUR factors.
[B] Factorials: sets built from factorial-smooth numbers. n! is maximally smooth.
    Test if factorial-based S or differences bundle large primes in (n/2,n] well.
    (Note: primes in (n/2,n] do NOT divide small factorials -- they only appear in
     m! for m>=p>n/2. So factorials may be BAD for LARGE-prime coverage. Test.)
"""
import math, random
from sympy import primerange, factorint

def primes_per(diffs, P, sample=400):
    if not diffs: return 0.0
    ds=random.sample(diffs, min(sample,len(diffs)))
    return sum(sum(1 for p in factorint(d) if p in P) for d in ds)/len(ds)

print("[A] Factorization structure: which FORM bundles large primes best?")
print(f"{'n':>5} {'gener.':>7} {'(a-b)(a+b)':>11} {'a^3-b^3':>8} {'a^6-b^6(4fac)':>13}")
for n in [1000, 2000]:
    P=set(primerange(n//2+1,n+1)); rng=random.Random(0); B=n*n*8
    # generic
    S=rng.sample(range(1,B+1),150); gen=[abs(a-b) for a in S for b in S if a!=b]
    # squares: keep a^2-b^2 <= B => a<=sqrt(B)
    rc2=int(B**0.5); A2=rng.sample(range(1,rc2+1),150)
    sq=[abs(a*a-b*b) for a in A2 for b in A2 if a!=b]
    # cubes: a^3-b^3<=B => a<=B^(1/3)
    rc3=max(3,int(B**(1/3))); A3=rng.sample(range(2,rc3+1),min(120,rc3-2))
    cb=[abs(a**3-b**3) for a in A3 for b in A3 if a!=b]
    # 6th: a^6-b^6<=B => a<=B^(1/6), factors into 4 pieces
    rc6=max(3,int(B**(1/6))); A6=list(range(2,rc6+1))
    s6=[abs(a**6-b**6) for a in A6 for b in A6 if a!=b] if rc6>3 else []
    print(f"{n:>5} {primes_per(gen,P):>7.3f} {primes_per(sq,P):>11.3f} "
          f"{primes_per(cb,P):>8.3f} {primes_per(s6,P):>13.3f}", flush=True)

print()
print("[B] Factorials: do factorial-based differences cover LARGE primes (n/2,n]?")
print(f"{'n':>5} {'fact-diff primes/diff':>22} {'note':>30}")
for n in [500, 1000]:
    P=set(primerange(n//2+1,n+1)); B=n*n*8
    # factorials up to <= B
    facts=[]; f=1; k=1
    while f<=B:
        k+=1; f*=k
        if f<=B: facts.append(f)
    fd=[abs(a-b) for a in facts for b in facts if a!=b]
    pp=primes_per(fd,P) if fd else 0
    # how many primes in (n/2,n] could POSSIBLY divide a factorial <= B?
    # p | m! iff m>=p; and m!<=B means m<= ~ (small). So max prime in any factorial<=B:
    maxm=k
    coverable=sum(1 for p in P if p<=maxm)
    print(f"{n:>5} {pp:>22.3f} {'max m with m!<=B is '+str(maxm)+', primes<=m: '+str(coverable):>30}", flush=True)
print()
print("Factorial note: a prime p>n/2 divides m! only if m>=p. But m!<=B=n^2*8 forces")
print("m small (~10-12), so NO prime >n/2 divides any factorial in range. Factorials")
print("are USELESS for large-prime covering -- they're smooth in SMALL primes only.")
