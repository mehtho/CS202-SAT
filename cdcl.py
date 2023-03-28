import random
from collections import defaultdict

class Solver:
    def __init__(self, clauses):
        self.clauses = clauses
        self.assigns = {}
        self.level = defaultdict(set)
        self.reason = {}
        self.decision_level = 0

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

    def unit_propagate(self):
        while True:
            new_assigns = []
            for clause in self.clauses:
                unassigned_literals = [lit for lit in clause if lit not in self.assigns]
                if not unassigned_literals:
                    continue
                
                if any(-lit in self.assigns and self.assigns[-lit] for lit in clause):
                    continue

                if len(unassigned_literals) == 1:
                    lit = unassigned_literals[0]
                    if -lit in self.assigns and not self.assigns[-lit]:
                        return False, clause
                    self.assigns[lit] = True
                    self.level[self.decision_level].add(lit)
                    self.reason[lit] = clause
                    new_assigns.append(lit)
            if not new_assigns:
                break
        return True, None

    def analyze_conflict(self, conflict_clause):
        new_clause = conflict_clause[:]
        learned_literals = set()
        num_literals_at_current_level = 0
        while True:
            for lit in new_clause:
                if lit not in learned_literals:
                    learned_literals.add(lit)
                    if self.decision_level in self.level and lit in self.level[self.decision_level]:
                        num_literals_at_current_level += 1
                        reason_clause = self.reason[lit]
                        new_clause = [l for l in new_clause if l != lit] + [l for l in reason_clause if l != -lit]
            if num_literals_at_current_level == 1:
                break
            num_literals_at_current_level = 0
            learned_literals.clear()
        return new_clause

    def backtrack(self, learned_clause):
        highest_decision_level = 0
        for lit in learned_clause:
            for level in self.level:
                if -lit in self.level[level]:
                    highest_decision_level = max(highest_decision_level, level)
                    break

        for level in range(highest_decision_level + 1, self.decision_level + 1):
            for lit in self.level[level]:
                del self.assigns[lit]
                del self.reason[lit]
            del self.level[level]

        self.decision_level = highest_decision_level
        return learned_clause

    def decide(self):
        unassigned_vars = {abs(lit) for clause in self.clauses for lit in clause} - {abs(lit) for lit in self.assigns}
        if unassigned_vars:
            var = random.choice(list(unassigned_vars))
            self.decision_level += 1
            self.assigns[var] = True
            self.level[self.decision_level].add(var)
            return True
        return False

    def cdcl(self):
        while True:
            success, conflict_clause = self.unit_propagate()
           
