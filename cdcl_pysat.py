import random
import timeit
from pysat.solvers import Solver

def generate_test_case(num_vars, num_clauses, clause_length):
    test_case = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < clause_length:
            var = random.randint(1, num_vars)
            negated = random.choice([True, False])
            clause.add(-var if negated else var)
        test_case.append(tuple(clause))
    return test_case

var =13
num_vars = var
num_clauses = 2**var * 2**var
clause_length = var
test_case = generate_test_case(num_vars, num_clauses, clause_length)

# Instantiate the CDCL solver (Glucose3 in this case)
solver = Solver(name ="g3",bootstrap_with=None, use_timer=True)

# Add clauses to the solver
for clause in test_case:
    solver.add_clause(clause)

# Solve the problem
time = timeit.timeit(lambda: solver.solve(), number = 1)
solution = solver.solve()
start_time = solver.time()
# print(test_case)
if solution:
    print("SATISFIABLE")
    print(solver.get_model())
    print(time)
else:
    print("UNSATISFIABLE")

# Clean up the solver instance
solver.delete()

# false 
# [(1, 2), (2, -2), (2, -1), (2, -2), (-2, -1), (1, -2), (2, -2), (1, -1), (2, -2), (1, 2)]
#[(1, 2), (-2, -1), (1, -1), (-2, -1), (1, -1), (1, -1), (1, -2), (2, -1), (1, -2), (2, -2)]
# [(2, 3, -2), (1, 2, 3), (1, 2, 3), (1, -3, -1), (2, -3, -2), (1, 2, 3), (1, 2, -1), (3, -2, -1), (2, 3, -3), (2, 3, -1), (1, 2, 3), (1, -3, -2), (1, 2, -1), (1, 2, -2), (-3, -1, -2), (3, -2, -1), (2, -3, -2), (1, 3, -2), (1, 2, -3), (2, -3, -1), (1, -3, -1), (2, 3, -2), (1, 3, -1), (3, -3, -1), (1, 3, -3), (1, 3, -3), (1, -3, -1), (2, 3, -2), (1, 2, -2), (1, -1, -2)]