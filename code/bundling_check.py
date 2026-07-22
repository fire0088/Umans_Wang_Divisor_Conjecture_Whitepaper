"""
Honest check: at these small n, does the optimal set actually BUNDLE primes
(multiple large primes per difference), or is it just covering ~1 target per
difference (K^2 ~ n, i.e. sqrt(n) regime, NOT the bundled counting floor)?

If no bundling, the 'gap vs counting floor' comparison is meaningless -- the
floor formula assumes bundling that doesn't happen at this n. The barrier
question only lives in the bundled regime.
"""
import math
from sympy import primerange

def targets(n): return list(range(n//2+1,n+1))

# For each n, the counting floor assumed per_pair = n^alpha/ln(n/2) primes bundled
# per difference. Measure the ACTUAL max primes-in-(n/2,n] per difference possible
# with differences <= 2n.
print("Does bundling actually happen at these n? (differences <= 2n)")
print(f"{'n':>4} {'budget e^n^a':>13} {'max diff=2n':>12} {'primes/diff assumed':>20} {'primes/diff POSSIBLE':>21}")
for n in [20, 34, 100, 1000, 10000]:
    alpha=0.45
    budget=math.exp(n**alpha)
    maxdiff=2*n
    assumed=max(1,int(n**alpha/math.log(n/2)))
    # a difference d<=2n divisible by primes in (n/2,n]: d can be at most ONE such
    # prime (since two primes >n/2 multiply to >n^2/4 >> 2n). So POSSIBLE bundling
    # of large primes with small differences = 1!
    # Bundling needs d up to budget e^{n^a}, not 2n. Check when budget > n^2/4
    # (room for 2 large primes):
    room_for_2 = budget > (n/2)**2
    print(f"{n:>4} {budget:>13.1f} {maxdiff:>12} {assumed:>20} "
          f"{'1 (diff<=2n!)' if not room_for_2 else '>=2':>21}", flush=True)
print()
print("KEY: with differences <= 2n (as in the exact search), a difference can be")
print("divisible by AT MOST ONE prime > n/2 (two would exceed n^2/4 > 2n). So the")
print("exact search NEVER bundles large primes -- it's in the K^2~n (sqrt n) regime.")
print("The bundled counting floor n^{(1-a)/2} requires differences up to e^{n^a} >>")
print("2n, i.e. MUCH larger n before it kicks in. So the n<=34 'gap' compares to a")
print("floor formula whose bundling assumption is FALSE at those n.")
print()
print("Honest consequence: the exact search used B=2n, forcing the sqrt-n regime.")
print("To test the REAL barrier question we must allow B up to e^{n^a} (bundling),")
print("which is exactly where the search explodes AND where the magnitude lives.")
