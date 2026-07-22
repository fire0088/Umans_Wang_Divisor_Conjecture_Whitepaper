"""
Clean version: forbid degenerate zero differences (require s_i != t_j whenever
cell (i,j) is assigned a prime). Then measure the TRUE min-magnitude of a VALID
bipartite cover, and honestly compare to the row-product bound. This removes the
all-zeros artifact that contaminated K=2.
"""
import math, random
from collections import defaultdict
from sympy import primerange

def exact_bipartite_valid(K, primes, seed=0, cap=None):
    rng=random.Random(seed)
    cells=[(i,j) for i in range(K) for j in range(K)]; rng.shuffle(cells)
    cell=defaultdict(list)
    for idx,p in enumerate(primes): cell[cells[idx%len(cells)]].append(p)
    edges=[(i,j,math.prod(ps)) for (i,j),ps in cell.items()]
    assigned=set((i,j) for (i,j) in cell.keys())
    Q=math.prod(primes)
    if cap is None: cap=int(Q**0.5)+30
    best=[None]; V=2*K
    def rec(v, vals, cm):
        if best[0] is not None and cm>=best[0][0]: return
        if v==V:
            S=vals[:K]; T=vals[K:]
            if len(set(S))==K and len(set(T))==K:
                # require nonzero diff on every assigned cell
                for (i,j) in assigned:
                    if S[i]==T[j]: return
                best[0]=(cm,list(vals))
            return
        for x in range(cap+1):
            if best[0] is not None and max(cm,x)>=best[0][0]: break
            ok=True
            for (i,j,m) in edges:
                si=i; tj=K+j
                if v==si and vals[tj] is not None and (x-vals[tj])%m!=0: ok=False;break
                if v==tj and vals[si] is not None and (vals[si]-x)%m!=0: ok=False;break
            if v<K:
                if x in vals[:v]: ok=False
            else:
                if x in vals[K:v]: ok=False
            if ok:
                vals[v]=x; rec(v+1,vals,max(cm,x)); vals[v]=None
    rec(0,[None]*V,0)
    return best[0], Q

print("VALID bipartite (nonzero diffs enforced) min-magnitude vs bounds:")
print(f"{'K':>3} {'#pr':>4} {'validMin':>9} {'log(min)':>9} {'0.5logQ':>9} {'logQ/K':>8} {'beats logQ/K?':>14}")
for K in [2,3]:
    for npr in [K*K, K*K+2]:
        primes=list(primerange(3,120))[:npr]
        if len(primes)<npr: continue
        r,Q=exact_bipartite_valid(K,primes,cap=int(math.prod(primes)**0.5)+25)
        if r is None:
            print(f"{K:>3} {npr:>4} {'none':>9}"); continue
        cm,vals=r; lm=math.log(cm+1)
        beats = lm < math.log(Q)/K
        print(f"{K:>3} {npr:>4} {cm:>9} {lm:>9.2f} {0.5*math.log(Q):>9.2f} {math.log(Q)/K:>8.2f} "
              f"{str(beats):>14}", flush=True)
print()
print("This is the HONEST test: valid (nonzero-diff) bipartite covers only. If they")
print("still beat logQ/K, the S-T slack is real (not degenerate). If not, the earlier")
print("finding was the artifact and S-T offers no genuine magnitude advantage.")
