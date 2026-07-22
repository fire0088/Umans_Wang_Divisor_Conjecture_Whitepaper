"""
Test perfect-squares idea: S = {a_1^2, ..., a_K^2}. Then differences factor:
  a_i^2 - a_j^2 = (a_i - a_j)(a_i + a_j).
A prime p covers via this difference iff p | (a_i-a_j) OR p | (a_i+a_j) -- TWO
chances per pair instead of one. Question: does this factored structure cover
(n/2,n] with FEWER elements than generic sets, especially in the bundled regime?

Two things to measure:
1. Coverage of (n/2,n] by squares-difference-set vs generic, at matched K.
2. The KEY structural question: does (a_i-a_j)(a_i+a_j) BUNDLE large primes better?
   i.e. is a squared difference more likely to be divisible by MULTIPLE primes
   in (n/2,n] than a generic difference of the same size?
"""
import math, random
from sympy import primerange, factorint

def targets(n): return list(range(n//2+1,n+1))
def covers_frac(diffs,n):
    T=targets(n)
    return sum(1 for t in T if any(d%t==0 for d in diffs))/len(T)

def square_diffs(A):
    S=[a*a for a in A]
    return {abs(x-y) for x in S for y in S if x!=y}
def generic_diffs(S):
    return {abs(x-y) for x in S for y in S if x!=y}

print("[1] Coverage: squares vs generic at matched K, matched magnitude budget")
print(f"{'n':>5} {'K':>4} {'sq cover':>9} {'generic cover':>14}")
for n in [200, 500, 1000]:
    B=n*n*4          # magnitude budget for the ELEMENTS (squares must be <= B)
    rootB=int(B**0.5)
    K=int(4*n**0.5)
    best_sq=0; best_gen=0
    for seed in range(40):
        rng=random.Random(seed)
        A=rng.sample(range(1,rootB+1), min(K,rootB))  # roots -> squares <= B
        best_sq=max(best_sq, covers_frac(square_diffs(A),n))
    for seed in range(40):
        rng=random.Random(seed)
        S=rng.sample(range(1,B+1), K)
        best_gen=max(best_gen, covers_frac(generic_diffs(S),n))
    print(f"{n:>5} {K:>4} {best_sq:>9.3f} {best_gen:>14.3f}", flush=True)

print()
print("[2] Bundling: avg # primes in (n/2,n] dividing a squared-diff vs generic")
print("    (both of similar magnitude) -- does factoring help carry more primes?")
print(f"{'n':>5} {'sq primes/diff':>15} {'generic primes/diff':>20}")
for n in [500, 1000, 2000]:
    P=set(primerange(n//2+1,n+1))
    B=n*n*4; rootB=int(B**0.5); rng=random.Random(0)
    # squared diffs
    A=rng.sample(range(1,rootB+1), 200)
    sq=[abs(a*a-b*b) for a in A for b in A if a!=b]
    sqp=[sum(1 for p in factorint(d) if p in P) for d in random.sample(sq,min(500,len(sq)))]
    # generic diffs of same magnitude
    S=rng.sample(range(1,B+1), 200)
    gen=[abs(a-b) for a in S for b in S if a!=b]
    genp=[sum(1 for p in factorint(d) if p in P) for d in random.sample(gen,min(500,len(gen)))]
    print(f"{n:>5} {sum(sqp)/len(sqp):>15.3f} {sum(genp)/len(genp):>20.3f}", flush=True)
print()
print("If sq primes/diff > generic: factoring (a-b)(a+b) genuinely bundles large")
print("primes better -> squares are a REAL structural aid toward the bundled floor.")
