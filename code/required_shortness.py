"""
The naive lattice-CRT fails: typical coordinate ~ e^{n^{(1+alpha)/2}} > budget
e^{n^alpha}. Our construction needs a SPECIAL lattice whose short vectors beat the
Minkowski average. Quantify EXACTLY how short: what's the required gap, and is it
compatible with what number fields can deliver (bounded root-discriminant towers)?

The BSSZ construction uses fields with discriminant Delta_K <= C^d (root-disc
bounded). The unit lattice there has covolume = regulator R_K <= Delta_K <= C^d,
and dimension d-1, so its vectors are ~ (C^d)^{1/d} = C = O(1). THAT's the magic:
in a bounded-root-disc field, the unit lattice has O(1)-size basis vectors despite
large covolume-per-... wait, covol C^d over d dims = C per dim = O(1). 

So the question for US: can we route our K^2/2 congruences through such a field so
the solution inherits the O(1)-per-dimension shortness? Compute the required vs
available shortness.
"""
import math
from sympy import primerange

print("Required 'shortness' vs what bounded-root-discriminant fields give:")
print(f"{'alpha':>6} {'n':>7} {'naive coord exp':>16} {'need coord exp':>15} {'gap to close':>13}")
for alpha in [0.3, 0.4]:
    for n in [10**4, 10**6, 10**8]:
        P=list(primerange(n//2+1,n+1))
        logQ=sum(math.log(p) for p in P)
        per_pair=max(1,int(n**alpha/math.log(n/2)))
        K=2
        while K*(K-1)//2*per_pair<len(P): K+=1
        naive_coord_log = logQ/K                 # Minkowski average
        need_coord_log = n**alpha                # budget
        naive_exp=math.log(naive_coord_log)/math.log(n)
        need_exp=math.log(need_coord_log)/math.log(n)
        gap = naive_coord_log/need_coord_log     # factor the field must save
        print(f"{alpha:>6} {n:>7.0e} {naive_exp:>16.3f} {need_exp:>15.3f} {gap:>13.1f}x", flush=True)
    print()
print("The field must make the solution SHORTER than Minkowski-average by the 'gap'")
print("factor. In BSSZ, bounded-root-disc fields give O(1)-per-dimension vectors,")
print("saving a factor ~ (covol)^{1/dim} / O(1). Our gap grows polynomially in n,")
print("so we'd need field dimension d ~ K ~ n^{(1-alpha)/2} AND root-disc bounded.")
print("Martinet towers give bounded root-disc for d->infinity -- SO THE DIMENSION IS")
print("AVAILABLE. The real question: can OUR specific congruences be embedded so the")
print("unit-lattice shortness applies to THEM. That's the crux of our theorem.")
