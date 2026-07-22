"""
Test the Bloom-Sawin-Schildkraut-Zhelezov PRINCIPLE in Z: build S = G*P where
G is multiplicatively structured (small product set) and P additively structured
(small sum set), and see if S-S covers (n/2,n] by divisibility with FEWER
elements than random -- i.e. does the GP structure help realize the covering?

Their G = unit box (mult structure), P = integer box (add structure). In Z the
cleanest analogue:
  G = geometric-like / smooth-number set (multiplicative structure)
  P = arithmetic progression / interval (additive structure)
  S = { g*p : g in G, p in P }

The KEY question for US: we need S-S divisible by many primes in (n/2,n]. In GP,
differences g1 p1 - g2 p2. Do these hit large primes well? Test coverage vs random
at matched |S|, in the CORRECT regime (elements allowed up to e^{n^alpha}).

Honest guard against the regime trap: use B large enough that bundling is POSSIBLE
(B >> n^2 so a difference CAN carry >=2 large primes), and report whether GP beats
random at equal K.
"""
import math, random
from sympy import primerange, factorint

def targets(n): return list(range(n//2+1, n+1))

def covers_frac(S, n):
    T=targets(n)
    diffs={abs(a-b) for a in S for b in S if a!=b}
    cov=0
    for t in T:
        if any(d % t==0 for d in diffs): cov+=1
    return cov/len(T)

def make_GP(n, K, B, seed):
    """S = G*P, G smooth/geometric (mult), P interval (add). |S|~K."""
    rng=random.Random(seed)
    g=int(round(K**0.5)); p=int(round(K**0.5))
    # G: geometric-ish multiplicative set
    r=rng.choice([2,3,2,3,5])
    G=[r**i for i in range(g)]
    # P: short arithmetic progression (additive box)
    d=rng.randint(1, max(2,B//(max(G)*p)))
    a0=rng.randint(1, max(2, B//max(G)))
    P=[a0+i*d for i in range(p)]
    S=sorted({gg*pp for gg in G for pp in P if gg*pp<=B})
    return S

def make_random(n, K, B, seed):
    rng=random.Random(seed)
    if B<=10**7:
        return rng.sample(range(1,B+1),min(K,B))
    return [rng.randint(1,B) for _ in range(K)]

print("GP construction vs random: coverage of (n/2,n] at matched size")
print("(B chosen large so bundling is POSSIBLE -- avoiding the no-bundling trap)")
print(f"{'n':>5} {'K':>4} {'B':>10} {'GP cover':>9} {'rand cover':>11} {'GP |S|':>7} {'rand|S|':>8}")
for n in [200, 500, 1000]:
    B=n*n*4  # big enough for a difference to carry 2+ primes >n/2
    K=int(4*n**0.5)
    best_gp=0; best_rand=0; gpsize=0; randsize=0
    for seed in range(40):
        Sg=make_GP(n,K,B,seed)
        if len(Sg)>=4:
            cg=covers_frac(Sg,n)
            if cg>best_gp: best_gp=cg; gpsize=len(Sg)
    for seed in range(40):
        Sr=make_random(n,K,B,seed)
        cr=covers_frac(Sr,n)
        if cr>best_rand: best_rand=cr; randsize=len(Sr)
    print(f"{n:>5} {K:>4} {B:>10} {best_gp:>9.3f} {best_rand:>11.3f} {gpsize:>7} {randsize:>8}", flush=True)
print()
print("If GP cover > rand cover at similar |S|: the multiplicative-additive")
print("structure HELPS cover -> supports the Bloom et al. construction as a route")
print("to a UW solution. If GP <= rand: the naive Z analogue doesn't capture it.")
