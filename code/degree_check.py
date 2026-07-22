"""
Honest check of the field degree d(n) our reduction needs vs what BSSZ deliver.

Our claim (main paper): d ~ K = n^{(1-alpha)/2}.
BSSZ scaling: d ~ log|A| (degree logarithmic in the set size).

Compute both, and the key question: how many short vectors does a degree-d
bounded-root-disc unit lattice supply (rank d-1), vs how many independent short
directions we need (~K, one per coordinate/constraint)?
"""
import math

print(f"{'alpha':>6} {'n':>9} {'K=n^((1-a)/2)':>14} {'log n':>7} {'log K':>7} {'K/log n':>10}")
for alpha in [0.3, 0.4, 0.45]:
    for n in [10**4, 10**6, 10**8, 10**12]:
        K = n**((1-alpha)/2)
        print(f"{alpha:>6} {n:>9.0e} {K:>14.1f} {math.log(n):>7.1f} {math.log(K):>7.1f} {K/math.log(n):>10.1f}")
    print()

print("The gap between the two degree claims:")
print("  d ~ K = n^{(1-alpha)/2}  (what I wrote) -- POLYNOMIAL in n")
print("  d ~ log|A| ~ log n       (BSSZ actual scaling) -- LOGARITHMIC in n")
print("  ratio K / log n grows without bound (see last column): these are NOT the")
print("  same regime. My d ~ K is larger than BSSZ-degree by a polynomial factor.")
print()
print("Rank of degree-d unit lattice = d-1 short directions available.")
print("We need to place K coordinates satisfying K constraints -> naively ~K")
print("independent short directions. So:")
print("  - If d ~ log n (BSSZ): only ~log n short directions -> CANNOT place")
print("    K = n^{(1-a)/2} >> log n coordinates independently. GAP.")
print("  - To get K short directions we'd need d ~ K = n^{(1-a)/2}, but BSSZ only")
print("    PROVE bounded-root-disc towers exist for all d (Martinet), and the")
print("    O(1)-per-dim shortness at that degree is exactly their result -- BUT they")
print("    build ONE set of size |A| with degree ~log|A|; using degree ~K means")
print("    |A| ~ e^K, a DIFFERENT (larger) object than they analyze.")
print()
print("HONEST VERDICT: the degree scaling is unresolved. d~K was stated too")
print("confidently. Martinet towers DO provide bounded-root-disc fields at every")
print("degree d (including d~K), so the FIELDS exist; but whether their unit lattice")
print("gives K usable independent short directions for OUR K constraints is exactly")
print("the open descent question -- NOT settled by citing BSSZ's log-degree result.")
