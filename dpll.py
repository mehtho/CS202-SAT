import random

def generate_test_case(num_vars, num_clauses, clause_length):
    test_case = []
    for _ in range(num_clauses):
        clause = []
        for _ in range(clause_length):
            var = random.randint(1, num_vars)
            negated = random.choice([True, False])
            clause.append(-var if negated else var)
        test_case.append(clause)
    return test_case


def dpll(clauses, assignment):
    if not clauses:
        return True, assignment
    if any(not clause for clause in clauses):
        return False, None

    unassigned_var = None
    for clause in clauses:
        for literal in clause:
            var = abs(literal)
            if var not in assignment:
                unassigned_var = var
                break
        if unassigned_var:
            break

    new_clauses = [clause[:] for clause in clauses]
    for value in [True, False]:
        assignment[unassigned_var] = value
        simplified_clauses = simplify_clauses(new_clauses, unassigned_var, value)
        sat, solution = dpll(simplified_clauses, assignment)
        if sat:
            return True, solution
        del assignment[unassigned_var]

    return False, None


def simplify_clauses(clauses, var, value):
    simplified_clauses = []
    for clause in clauses:
        new_clause = []
        for literal in clause:
            if literal == var and value or literal == -var and not value:
                break
            if literal != var and literal != -var:
                new_clause.append(literal)
        else:
            simplified_clauses.append(new_clause)
    return simplified_clauses


def main():
    num_vars = 100
    num_clauses = 10
    clause_length = 10
    test_case = generate_test_case(num_vars, num_clauses, clause_length)
    print("Generated test case (CNF):", test_case)
    
    sat, assignment = dpll(test_case, {})
    if sat:
        print("Satisfiable")
        print("Assignment:", assignment)
    else:
        print("Unsatisfiable")


if __name__ == "__main__":
    main()
