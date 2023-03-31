import random
from pysat.solvers import Glucose3

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

num_vars = 3
num_clauses = 30
clause_length = 3
test_case = generate_test_case(num_vars, num_clauses, clause_length)

# Instantiate the CDCL solver (Glucose3 in this case)
solver = Glucose3()

# Add clauses to the solver
for clause in test_case:
    solver.add_clause(clause)

# Solve the problem
solution = solver.solve()

print(test_case)
if solution:
    print("SATISFIABLE")
    print(solver.get_model())
else:
    print("UNSATISFIABLE")

# Clean up the solver instance
solver.delete()

# false 
# [(1, 2), (2, -2), (2, -1), (2, -2), (-2, -1), (1, -2), (2, -2), (1, -1), (2, -2), (1, 2)]
#[(1, 2), (-2, -1), (1, -1), (-2, -1), (1, -1), (1, -1), (1, -2), (2, -1), (1, -2), (2, -2)]
# [(2, 3, -2), (1, 2, 3), (1, 2, 3), (1, -3, -1), (2, -3, -2), (1, 2, 3), (1, 2, -1), (3, -2, -1), (2, 3, -3), (2, 3, -1), (1, 2, 3), (1, -3, -2), (1, 2, -1), (1, 2, -2), (-3, -1, -2), (3, -2, -1), (2, -3, -2), (1, 3, -2), (1, 2, -3), (2, -3, -1), (1, -3, -1), (2, 3, -2), (1, 3, -1), (3, -3, -1), (1, 3, -3), (1, 3, -3), (1, -3, -1), (2, 3, -2), (1, 2, -2), (1, -1, -2)]