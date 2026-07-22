"""
Much faster exact min-K(n) via bitmask coverage + aggressive pruning, so the
exact sequence can reach n~50-70 and the floor-gap trend becomes visible.

Key speedups vs the old version:
  - targets -> bit positions; coverage is an int bitmask, OR to combine.
  - precompute, for each candidate difference d, the mask of targets it covers.
  - branch & bound: track best coverage; prune when even covering all remaining
    targets is impossible with the elements left.
  - 0 fixed in S (translation invariance).
"""
import math, time, sys

def targets(n): return list(range(n//2+1, n+1))

def min_K_fast(n, B=None, kcap=16, time_budget=60):
    T = targets(n)
    if B is None: B = 2*n
    idx = {t:i for i,t in enumerate(T)}
    full = (1<<len(T)) - 1
    # diff_mask[d] = bitmask of targets dividing d, for d in 1..B
    diff_mask = [0]*(B+1)
    for d in range(1, B+1):
        m = 0
        for t in T:
            if d % t == 0: m |= (1<<idx[t])
        diff_mask[d] = m
    t_start = time.time()
    # For a chosen set (with 0), coverage = OR over pairs of diff_mask[|a-b|].
    # DFS adding elements in increasing order; maintain coverage incrementally.
    def search(K):
        # elements list starts [0]; add increasing values in [1,B]
        best = [0]
        stop = [False]
        def dfs(elems, cov, start):
            if stop[0]: return False
            if cov == full: return True
            if len(elems) == K: return False
            if time.time()-t_start > time_budget: stop[0]=True; return False
            remaining_slots = K - len(elems)
            # optimistic prune: even if every remaining element covered ALL
            # currently-uncovered targets, need at least... (weak but cheap):
            # if no room left, fail (handled above).
            for v in range(start, B+1):
                if B+1 - v < remaining_slots: break
                nc = cov
                for e in elems:
                    nc |= diff_mask[v-e]
                # only recurse if v ADDS coverage or we still have slack slots
                if dfs(elems+[v], nc, v+1): return True
                if stop[0]: return False
            return False
        return dfs([0], 0, 1)
    for K in range(2, kcap+1):
        if time.time()-t_start > time_budget: return None, "timeout"
        if search(K): return K, "exact"
    return None, "none"

print("Fast exact min-K(n): floor-gap trend")
print(f"{'n':>4} {'floor':>6} {'minK':>5} {'gap':>4} {'time':>7}")
gaps=[]
for n in range(12, 72, 2):
    t0=time.time()
    K,note = min_K_fast(n, time_budget=40)
    dt=time.time()-t0
    if K is None:
        print(f"{n:>4} stopped ({note}, {dt:.0f}s)"); break
    m=len(targets(n)); per_pair=max(1,int(n**0.45/math.log(n/2)))
    fK=2
    while fK*(fK-1)//2*per_pair<m: fK+=1
    gaps.append((n,K-fK))
    print(f"{n:>4} {fK:>6} {K:>5} {K-fK:>4} {dt:>6.1f}s", flush=True)
print(f"\ngap sequence: {[g for _,g in gaps]}")
if len(gaps)>=8:
    maxgap=max(g for _,g in gaps)
    frac=sum(1 for _,g in gaps if g>=1)/len(gaps)
    print(f"max gap seen: {maxgap}   fraction with gap>=1: {frac:.2f}")
    print("gap staying in {0,1} => bounded (pro-UW). gap reaching 2,3,... => drift (barrier).")
