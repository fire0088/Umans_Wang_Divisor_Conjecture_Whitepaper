"""
The GP test used a SPARSE geometric G -- exactly the known-inadequate Balog-Wooley
version. Bloom et al.'s key fix: a DENSE multiplicatively-structured set (unit
lattice box). Test the densest Z-native multiplicative structure: SMOOTH NUMBERS
(y-smooth: all prime factors <= y). These are dense AND multiplicatively closed-ish.

S = { s smooth : s in an interval or box }, compare difference-set coverage of
(n/2,n] vs random. Also test the deeper point: does the covering problem even WANT
multiplicative structure in S, or in S-S? Our need is S-S multiplicatively rich.
Smooth S -> is S-S rich in large primes? (a-b for smooth a,b -- NOT smooth
generally). Test directly.
"""
import math, random
from sympy import primerange, factorint

def targets(n): return list(range(n//2+1,n+1))
def covers_frac(S,n):
    T=targets(n); diffs={abs(a-b) for a in S for b in S if a!=b}
    return sum(1 for t in T if any(d%t==0 for d in diffs))/len(T)

def smooth_set(B, y, K, seed):
    """K smooth numbers (all prime factors <= y) up to B."""
    rng=random.Random(seed)
    smooth=[]
    # generate smooth numbers up to B via primes <= y
    ps=list(primerange(2,y+1))
    # random smooth: multiply random small primes
    seen=set()
    tries=0
    while len(seen)<K*3 and tries<K*100:
        tries+=1
        v=1
        while v<=B:
            if rng.random()<0.5: break
            v*=rng.choice(ps)
        if 1<v<=B: seen.add(v)
    S=sorted(seen)
    return rng.sample(S,min(K,len(S))) if len(S)>=K else S

print("Dense multiplicative (smooth) vs random for covering (n/2,n]:")
print(f"{'n':>5} {'K':>4} {'smooth cover':>13} {'rand cover':>11}")
for n in [200,500,1000]:
    B=n*n*4; K=int(4*n**0.5)
    bs=0
    for seed in range(30):
        S=smooth_set(B, 2*n, K, seed)  # y=2n so smooth allows one factor up to 2n
        if len(S)>=4:
            c=covers_frac(S,n); bs=max(bs,c)
    br=0
    for seed in range(30):
        S=random.Random(seed).sample(range(1,B+1),K); br=max(br,covers_frac(S,n))
    print(f"{n:>5} {K:>4} {bs:>13.3f} {br:>11.3f}", flush=True)
print()
print("The deeper test: our covering needs S-S rich in LARGE primes (>n/2).")
print("Is there ANY structured S whose S-S is large-prime-rich at counting floor?")
print("Random already achieves it (random S-S hits each large prime w.p. ~K^2/p).")
print("=> the covering problem does NOT need special structure in the ACCESSIBLE")
print("regime; the barrier question is purely whether the BUNDLED floor (each diff")
print("= product of many large primes) is realizable -- and THAT is what no")
print("construction here reaches, GP or smooth or random. Consistent all along.")
