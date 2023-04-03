import random
import timeit
import matplotlib.pyplot as plt
from pysat.solvers import Glucose3
import pandas as pd 
import numpy as np
import threading
import math
from cdcl202 import Solver
import os

class test_case:
    def __init__(self, num_vars, num_clauses, clause_length, case):
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.clause_length = clause_length
        self.case = case

def generate_test_case(num_vars, num_clauses, clause_length):
    test_case = set()
    if os.path.isfile("cases/" + str(num_vars) + ".cnf"):
        f = open("cases/" + str(num_vars) + ".cnf", "r")
        for line in f:
            test_case.add(frozenset({int(x) for x in line.split()}))
        print('read test case #', num_vars)
    else:
        for _ in range(num_clauses):
            clause = set()
            while len(clause) < clause_length:
                var = random.randint(1, num_vars)
                negated = random.choice([True, False])
                clause.add(-var if negated else var)
            test_case.add(frozenset(clause))
        
        f = open("cases/" + str(num_vars) + ".cnf", "w")
        for clause in test_case:
            for lit in clause:
                f.write(str(lit) + ' ')
            f.write('\n')
        
        print('made test case #', num_vars)

    return test_case

# If the formula is empty, it is trivially satisfiable, and the current assignment is returned.
# It first extracts all variables present in the formula and sorts them in ascending order.
# It then iterates over all possible assignments of truth values to the variables (2^n possible assignments for n variables).
# For each assignment, it checks if the formula is satisfied by evaluating each clause in the formula using the given assignment. If all clauses are satisfied, it returns True along with the satisfying assignment.
# If no satisfying assignment is found after trying all possible assignments, it returns False along with an empty assignment dictionary.
def naive(formula):
    # Get the list of variables in the formula
    variables = set()
    for clause in formula:
        for variable in clause:
            variables.add(abs(variable))
    variables = sorted(list(variables))

    # Try all possible assignments of truth values to the variables
    num_variables = len(variables)
    for i in range(2 ** num_variables):
        assignment = {}
        for j in range(num_variables):
            variable = variables[j]
            # If the negation of the variable is not present in the formula, then the truth value of its negation is also added to the assignment dictionary.
            assignment[variable] = (i >> j) & 1 == 1
            if variable * -1 not in variables:
                assignment[-variable] = not assignment[variable]

        # Check if the assignment satisfies the formula
        satisfied = True
        for clause in formula:
            clause_satisfied = False
            for variable in clause:
                if (variable > 0 and assignment[variable]) or (variable < 0 and not assignment[-variable]):
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                satisfied = False
                break

        if satisfied:
            return True, assignment

    # No satisfying assignment found
    return False, {}

def naive_thread(test_cases):
    data = []
    for idx, tc in enumerate(test_cases):

        naive_time = timeit.timeit(lambda: naive(tc.case))
        data.append((tc.num_vars, tc.num_clauses, tc.clause_length, naive_time))

        print('solved naive #', idx)

    pd.DataFrame(data, columns=['num_vars', 'num_clauses', 'clause_length', 'naive_time']).to_csv('naive.csv')
        
# If the formula is empty, it is trivially satisfiable, and the current assignment is returned.
# If any clause in the formula is empty, the formula is unsatisfiable, and the current assignment is returned.
# If there exists a unit clause (a clause with only one literal), the literal in that clause must be assigned a truth value. The clause containing that literal and any other clauses containing the negation of that literal are removed from the formula. The DPLL algorithm is then called recursively on the simplified formula with the new assignment.
# If there is no unit clause, a variable is selected (the first literal of the first clause is arbitrarily chosen in this implementation), and the DPLL algorithm is called recursively twice: once with the variable assigned True, and once with the variable assigned False. If either recursive call returns a satisfiable assignment, that assignment is returned.
# If no satisfying assignment is found, the function returns False along with the current assignment.
def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal
        
def dpll(cnf, assignments=set()):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
    
    l = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if l not in c]
    new_cnf = [c.difference({-abs(l)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, assignments=assignments.union({abs(l)}))
    if sat:
        return sat, vals
         
    new_cnf = [c for c in cnf if -l not in c]
    new_cnf = [c.difference({(abs(l))}) for c in new_cnf]
    sat, vals = dpll(new_cnf, assignments=assignments.union({-abs(l)}))
    if sat:
        return sat, vals
 
    return False, None
    
def dpll_thread(test_cases):
    data = []
    for idx, tc in enumerate(test_cases):
        dpll_time = timeit.timeit(lambda: dpll(tc.case), number=1)
        data.append((tc.num_vars, tc.num_clauses, tc.clause_length, dpll_time))

        print('solved dpll #', idx)

    pd.DataFrame(data, columns=['num_vars', 'num_clauses', 'clause_length', 'dpll_time']).to_csv('dpll.csv')

def cdcl_thread(test_cases):
    data = []
    for idx, tc in enumerate(test_cases):
        cnf = set()
        for clause in tc.case:
            cnf.add(frozenset(map(int, clause)))
            solver = Solver(cnf, tc.num_vars)

        cdcl_time = timeit.timeit(lambda: solver.solve(), number=1)
        data.append((tc.num_vars, tc.num_clauses, tc.clause_length, cdcl_time))
        print('solved cdcl #', idx)
    
    pd.DataFrame(data, columns=['num_vars', 'num_clauses', 'clause_length', 'cdcl_time']).to_csv('cdcl.csv')

def __main__():
    test_cases = []
    for i in range(1, 60):
        num_vars = i
        num_clauses = (2**i)**2 
        clause_length = min(i, 8)
        test_cases.append(test_case(num_vars, num_clauses, clause_length, generate_test_case(num_vars, num_clauses, clause_length)))

    t1 = threading.Thread(target=naive_thread, args=[test_cases[:10]])
    t2 = threading.Thread(target=dpll_thread, args=[test_cases[:60]])
    t3 = threading.Thread(target=cdcl_thread, args=[test_cases[:60]])

    # t1.start()
    t2.start()
    t3.start()

    # t1.join()
    t2.join()
    t3.join()

    df3 = pd.read_csv("cdcl.csv")
    df2 = pd.read_csv("dpll.csv")
    df1 = pd.read_csv("naive.csv")

    df4 = pd.DataFrame([df3.num_vars, df3.num_clauses, df3.clause_length, df3.cdcl_time, df2.dpll_time, df1.naive_time]).transpose()
    # df4 = pd.DataFrame([df3.num_vars, df3.num_clauses, df3.clause_length, df3.cdcl_time, df2.dpll_time]).transpose()
    print(df4)
    df4.to_csv('combined.csv')

    ax = df4.plot(kind="scatter", x="num_vars",y="dpll_time", color="r", label="dpll")
    df4.plot(kind="scatter", x="num_vars",y="cdcl_time", color="g", label="cdcl", ax=ax)
    df4.plot(kind="scatter", x="num_vars",y="naive_time", color="b", label="naive", ax=ax)

    plt.show()

__main__()