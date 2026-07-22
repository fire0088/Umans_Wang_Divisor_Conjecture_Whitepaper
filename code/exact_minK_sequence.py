"""
Get as many EXACT min-K values as possible (fast custom search, 0 fixed in S),
then examine whether min-K / (various references) approaches a clean limit.

min-K(n) = smallest K such that some distinct K-set (0 in it WLOG) has its
difference set covering (n/2,n] by divisibility, elements <= B (generous).
"""
import math
from functools import lru_cache

def targets(n): return list(range(n//2+1, n+1))

def covers(S, T):
    diffs = set()
    for i in range(len(S)):
        for j in range(i):
            diffs.add(S[i]-S[j])
    for t in T:
        if not any(d % t == 0 for d in diffs): return False
    return True

def min_K_exact(n, B=None, kcap=14):
    """Exhaustive with strong pruning: 0 in S, elements in [1,B], increasing."""
    T = targets(n)
    if B is None: B = 2*n
    from itertools import combinations
    for K in range(2, kcap+1):
        # search distinct K-1 elements in [1,B] (plus 0)
        # prune: need each target covered; use greedy DFS with coverage tracking
        found = [False]
        Tset = T
        def dfs(chosen, start, covered):
            if found[0]: return
            if len(covered) == len(Tset):
                found[0] = True; return
            if len(chosen) == K:  # includes the fixed 0
                return
            remaining = K - len(chosen)
            for v in range(start, B+1):
                if B+1 - v < remaining: break
                nc = set(covered)
                for c in chosen:
                    d = v - c
                    for t in Tset:
                        if t not in nc and d % t == 0: nc.add(t)
                dfs(chosen+[v], v+1, nc)
                if found[0]: return
        dfs([0], 1, set())
        if found[0]: return K
    return None

print("Exact min-K(n) sequence and candidate limits:")
print(f"{'n':>4} {'|I0|':>5} {'floor':>6} {'minK':>5} {'minK-floor':>10} "
      f"{'minK/sqrt(n)':>12} {'minK/(n/lnn)^.5':>15}")
import time
data=[]
for n in range(12, 60, 2):
    t0=time.time()
    K = min_K_exact(n)
    dt=time.time()-t0
    if K is None or dt>25:
        print(f"{n:>4} (stopped, dt={dt:.0f}s)"); break
    m=len(targets(n))
    per_pair=max(1,int(n**0.45/math.log(n/2)))
    fK=2
    while fK*(fK-1)//2*per_pair<m: fK+=1
    data.append((n,K,fK,m))
    print(f"{n:>4} {m:>5} {fK:>6} {K:>5} {K-fK:>10} {K/math.sqrt(n):>12.3f} "
          f"{K/math.sqrt(n/math.log(n)):>15.3f}", flush=True)

# analyze the sequence
if len(data)>=5:
    print("\nAnalysis of min-K(n):")
    import numpy as np
    ns=np.array([d[0] for d in data]); Ks=np.array([d[1] for d in data])
    # fit exponent
    e=np.polyfit(np.log(ns),np.log(Ks),1)[0]
    print(f"  fitted exponent (log minK / log n): {e:.3f}  (0.5 = sqrt scaling)")
    print(f"  minK-floor sequence: {[d[1]-d[2] for d in data]}")
    print(f"  Does minK-floor grow, or stay bounded? (grow=barrier, bounded=UW-ish)")
