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


def dpll(formula, assignment):
    if not formula:
        return True, assignment
    
    if any(not clause for clause in formula):
        return False, assignment
    
    unit_clauses = [c for c in formula if len(c) == 1]
    if unit_clauses:
        unit = unit_clauses[0][0]
        new_formula = [[l for l in c if l != -unit] for c in formula if unit not in c]
        return dpll(new_formula, assignment + [unit])
    
    variable = abs(formula[0][0])
    
    for value in [variable, -variable]:
        new_formula = [[l for l in c if l != -value] for c in formula if value not in c]
        result, new_assignment = dpll(new_formula, assignment + [value])
        if result:
            return result, new_assignment

    return False, assignment

num_vars = 2
num_clauses = 2
clause_length = 2
test_case = generate_test_case(num_vars, num_clauses, clause_length)
result, assignment = dpll(test_case, [])
print(test_case)
print("Satisfiable:", result)
print("Assignment:", assignment)