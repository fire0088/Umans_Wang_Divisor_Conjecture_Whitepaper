"""
CRITICAL honesty check: is the 'small bipartite solution' actually a VALID COVER,
or a degenerate one that satisfies the congruences trivially (T~0, S~small) WITHOUT
actually covering the primes with DISTINCT nonzero differences?

The covering requires: for each prime p (in cell (i,j)), p | (s_i - t_j), AND this
must be a genuine covering of (n/2,n]. If s_i=t_j (both small/equal), then
s_i - t_j = 0, and p|0 trivially -- but a ZERO difference does NOT cover p in the
UW sense (need s-t nonzero, since we're covering divisors of actual differences).

Re-examine: does the exact solver's 'small solution' have s_i - t_j = 0 (degenerate)
or genuinely nonzero multiples of m_ij? If zero, the whole 'S-T slack' finding is
the degenerate-cover artifact (like the all-zeros construction caught earlier)!
"""
import math, random
from collections import defaultdict
from sympy import primerange

def exact_bipartite_checked(K, primes, seed=0, cap=None):
    rng=random.Random(seed)
    cells=[(i,j) for i in range(K) for j in range(K)]; rng.shuffle(cells)
    cell=defaultdict(list)
    for idx,p in enumerate(primes): cell[cells[idx%len(cells)]].append(p)
    edges=[(i,j,math.prod(ps)) for (i,j),ps in cell.items()]
    Q=math.prod(primes)
    if cap is None: cap=int(Q**0.5)+30
    best=[None]; V=2*K
    def rec(v, vals, cm):
        if best[0] is not None and cm>=best[0][0]: return
        if v==V:
            S=vals[:K]; T=vals[K:]
            if len(set(S))==K and len(set(T))==K:
                best[0]=(cm, list(vals))
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
    return best[0], edges, cell

print("Is the small bipartite solution a VALID cover or a DEGENERATE (zero-diff) one?")
for K in [2,3]:
    primes=list(primerange(3,120))[:K*K]
    result, edges, cell = exact_bipartite_checked(K,primes,cap=int(math.prod(primes)**0.5)+20)
    if result is None: print(f"K={K}: none"); continue
    cm, vals = result
    S=vals[:K]; T=vals[K:]
    print(f"\nK={K}: S={S}, T={T}, maxElt={cm}")
    # Check each assigned prime: is it covered by a NONZERO difference?
    degenerate=0; valid=0
    for (i,j),ps in cell.items():
        d = S[i]-T[j]
        for p in ps:
            if d==0:
                degenerate+=1
            elif d%p==0:
                valid+=1
            else:
                print(f"    !! prime {p} in cell ({i},{j}) NOT covered: s-t={d}")
    print(f"    primes covered by NONZERO diff: {valid}; by ZERO diff (degenerate): {degenerate}")
    if degenerate>0:
        print(f"    => DEGENERATE: {degenerate} primes 'covered' by s_i=t_j (zero diff,")
        print(f"       invalid). The 'S-T slack' is the all-zeros artifact AGAIN.")
    else:
        print(f"    => VALID: all primes covered by genuine nonzero differences.")
