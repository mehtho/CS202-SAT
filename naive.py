import random

def generate_test_case(num_vars, num_clauses, clause_length):
    test_case = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < clause_length:
            var = random.randint(1, num_vars)
            negated = random.choice([True, False])
            clause.add(-var if negated else var)
        test_case.append(list(clause))
    return test_case


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


num_vars = 2
num_clauses = 2
clause_length = 2
test_case = generate_test_case(num_vars, num_clauses, clause_length)
result, assignment = naive(test_case)
print(test_case)
print("Satisfiable:", result)
print("Assignment:", assignment)