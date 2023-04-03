import pandas as pd
import pylab as plt
import numpy as np
import itertools
import random
import time


def brute_force(cnf):
    literals = set()
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])
 
    literals = list(literals)
    n = len(literals)
    for seq in itertools.product([True,False], repeat=n):
        a = set(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in cnf]):
            return True, a
 
    return False, None

def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            print('LITERAL', literal)
            return literal
 
def dpll(cnf, assignments={}):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
    
    l = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if abs(l) not in c]
    new_cnf = [c.difference({-abs(l)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{abs(l)}})
    if sat:
        return sat, vals
         
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(abs(l))}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{-abs(l)}})
    if sat:
        return sat, vals
 
    return False, None

def random_kcnf(n_literals, n_conjuncts, k=3):
    result = []
    for _ in range(n_conjuncts):
        conj = set()
        for _ in range(k):
            index = random.randint(0, n_literals)
            conj.add((
                str(index).rjust(10, '0'),
                bool(random.randint(0,2)),
            ))
        result.append(conj)
    print(result)
    return result



brute_force_times = []
dpll_times = []
for n_literals in range(16):
    current_brute_force_times = []
    current_dpll_times = []
    for _ in range(100):
        n_conjuncts = random.randint(0, n_literals*6)
        s = random_kcnf(n_literals, n_conjuncts)
        start = time.time()
        brute_force(s)
        stop = time.time()
        current_brute_force_times.append(stop-start)
        start = time.time()
        dpll(s)
        stop = time.time()
        current_dpll_times.append(stop-start)
    brute_force_times.append(np.mean(current_brute_force_times))
    dpll_times.append(np.mean(current_dpll_times))

df = pd.DataFrame(
    {'Number of literals': range(16),
        'Brute Force': brute_force_times,
        'DPLL': dpll_times
    }
)