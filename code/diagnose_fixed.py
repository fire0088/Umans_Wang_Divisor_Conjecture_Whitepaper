"""
FIXED diagnosis: the previous version treated CBC timeout as 'not feasible at
this K' and advanced to larger K, INFLATING true-min-K (manufacturing the
barrier). Fix: for each K report Optimal / Infeasible / TIMEOUT explicitly.
The floor is only 'unreachable' if the floor K is PROVEN INFEASIBLE. If it times
out, we know nothing -- must say so.
"""
import math, pulp
from sympy import primerange

def status_at_K(n, K, B, time_limit=30):
    targets=list(range(n//2+1,n+1))
    pool=list(range(0,B+1))
    prob=pulp.LpProblem("f",pulp.LpMinimize)
    x={a:pulp.LpVariable(f"x{a}",cat="Binary") for a in pool}
    prob+=0; prob+=pulp.lpSum(x.values())==K
    for i in targets:
        ors=[]
        for a in pool:
            for b in pool:
                if a>b and (a-b)%i==0:
                    y=pulp.LpVariable(f"y_{i}_{a}_{b}",cat="Binary")
                    prob+=y<=x[a]; prob+=y<=x[b]; ors.append(y)
        if not ors: return "model_infeasible"
        prob+=pulp.lpSum(ors)>=1
    prob.solve(pulp.PULP_CBC_CMD(msg=0,timeLimit=time_limit))
    return pulp.LpStatus[prob.status]  # Optimal / Infeasible / Not Solved(=timeout)

print("HONEST per-K status (Optimal=feasible, Infeasible=proven none, Not Solved=timeout)")
print(f"{'n':>4} {'floorK':>7} {'status@floorK':>14} {'status@floorK+1':>16} {'status@floorK+2':>16}")
for n in [24, 30, 40]:
    targets=list(range(n//2+1,n+1))
    alpha=0.45; per_pair=max(1,int(n**alpha/math.log(n/2)))
    fK=2
    while fK*(fK-1)//2*per_pair<len(targets): fK+=1
    s0=status_at_K(n,fK,2*n,time_limit=25)
    s1=status_at_K(n,fK+1,2*n,time_limit=25)
    s2=status_at_K(n,fK+2,2*n,time_limit=25)
    print(f"{n:>4} {fK:>7} {s0:>14} {s1:>16} {s2:>16}", flush=True)
print()
print("Barrier conclusion is valid ONLY if status@floorK == 'Infeasible' (PROVEN).")
print("If it's 'Not Solved' (timeout), the earlier 'floor unreachable' was the")
print("CBC-timeout bug again, and we have NOT shown the floor is unreachable.")
