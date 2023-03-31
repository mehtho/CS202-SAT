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

def naive(formula):
    for i in range(2**len(formula[0])):
        assignment = [int(x) for x in bin(i)[2:].zfill(len(formula[0]))]
        
        satisfied = True
        for clause in formula:
            clause_satisfied = False
            for literal in clause:
                if literal > 0 and assignment[abs(literal)-1] == 1:
                    clause_satisfied = True
                    break
                elif literal < 0 and assignment[abs(literal)-1] == 0:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                satisfied = False
                break
                
        if satisfied:
            return True, [literal if assignment[abs(literal)-1] else -literal for literal in formula[0]]
            
    print("FAIL")
    return False, None


num_vars = 2
num_clauses = 2
clause_length = 2
test_case = generate_test_case(num_vars, num_clauses, clause_length)
result, assignment = naive(test_case)
print(test_case)
print("Satisfiable:", result)
print("Assignment:", assignment)