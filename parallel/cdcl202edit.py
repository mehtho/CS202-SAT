"""
SAT solver using CDCL
"""
import os
import time
from collections import deque
import random

TRUE = 1
FALSE = 0
UNASSIGN = -1

class Solver:

    def __init__(self, testcase, max_literal):
        self.cnf = self.process_test_case(testcase)
        self.vars = set(range(1, max_literal + 1))
        self.learnts = set()
        self.assigns = dict.fromkeys(list(self.vars), UNASSIGN)
        self.level = 0
        self.nodes = dict((k, ImplicationNode(k, UNASSIGN)) for k in list(self.vars))
        self.branching_vars = set()
        self.branching_history = {}  # level -> branched variable
        self.propagate_history = {}  # level -> propagate variables list
        self.branching_count = 0
    
    def process_test_case(self, testcase):
        cnf = set()
        for clause in testcase:
            cnf.add(frozenset(map(int, clause)))
        return cnf

    def solve(self):
        """
        Returns True if SAT, False if UNSAT
        :return: whether there is a solution
        """
        while not self.are_all_variables_assigned():
            conflict_clause = self.unit_propagate()
            if conflict_clause:
                # there is a conflict in unit propagation
                level, learnt_clause = self.conflict_analyze(conflict_clause)
                if level < 0:
                    return False
                self.learnts.add(learnt_clause)
                self.backtrack(level)
                self.level = level
            else:
                # branching
                self.level += 1
                self.branching_count += 1
                var, val = self.pick_branching_variable()
                self.assigns[var] = val
                self.branching_vars.add(var)
                self.branching_history[self.level] = var
                self.propagate_history[self.level] = deque()
                self.update_graph(var)
        return True


    def compute_value(self, literal):
        """
        Compute the value of the literal (could be -/ve or +/ve) from
        `assignment`. Returns -1 if unassigned
            :param literal: an int, can't be 0
            :returns: value of the literal
        """
        value = self.assigns[abs(literal)]
        value = value if value == UNASSIGN else value ^ (literal < 0)
        return value

    def compute_clause(self, clause):
        values = list(map(self.compute_value, clause))
        value = UNASSIGN if UNASSIGN in values else max(values)
        return value

    def is_unit_clause(self, clause):
        """
        Checks if clause is a unit clause. If and only if there is
        exactly 1 literal unassigned, and all the other literals having
        value of 0.
            :param clause: set of ints
            :returns: (is_clause_a_unit, the_literal_to_assign, the clause)
        """
        values = []
        unassigned = None

        for literal in clause:
            value = self.compute_value(literal)
            values.append(value)
            unassigned = literal if value == UNASSIGN else unassigned

        check = ((values.count(FALSE) == len(clause) - 1 and
                  values.count(UNASSIGN) == 1) or
                 (len(clause) == 1
                  and values.count(UNASSIGN) == 1))
        return check, unassigned

    def update_graph(self, var, clause=None):
        node = self.nodes[var]
        node.value = self.assigns[var]
        node.level = self.level

        # update parents
        if clause:  # clause is None, meaning this is branching, no parents to update
            for v in [abs(lit) for lit in clause if abs(lit) != var]:
                node.parents.append(self.nodes[v])
                self.nodes[v].children.append(node)
            node.clause = clause

    def unit_propagate(self):
        """
        A unit clause has all of its literals but 1 assigned to 0. Then, the sole
        unassigned literal must be assigned to value 1. Unit propagation is the
        process of iteratively applying the unit clause rule.
        :return: None if no conflict is detected, else return the literal
        """
        while True:
            propagate_queue = deque()
            for clause in [x for x in self.cnf.union(self.learnts)]:
                c_val = self.compute_clause(clause)
                if c_val == TRUE:
                    continue
                if c_val == FALSE:
                    return clause
                else:
                    is_unit, unit_lit = self.is_unit_clause(clause)
                    if not is_unit:
                        continue
                    prop_pair = (unit_lit, clause)
                    if prop_pair not in propagate_queue:
                        propagate_queue.append(prop_pair)
            if not propagate_queue:
                return None

            for prop_lit, clause in propagate_queue:
                prop_var = abs(prop_lit)
                self.assigns[prop_var] = TRUE if prop_lit > 0 else FALSE
                self.update_graph(prop_var, clause=clause)
                try:
                    self.propagate_history[self.level].append(prop_lit)
                except KeyError:
                    pass  # propagated at level 0

    def get_unit_clauses(self):
        return list(filter(lambda x: x[0], map(self.is_unit_clause, self.cnf)))

    def are_all_variables_assigned(self):
        all_assigned = all(var in self.assigns for var in self.vars)
        none_unassigned = not any(var for var in self.vars if self.assigns[var] == UNASSIGN)
        return all_assigned and none_unassigned

    def all_unassigned_vars(self):
        return filter(
            lambda v: v in self.assigns and self.assigns[v] == UNASSIGN,
            self.vars)
            
    def pick_branching_variable(self):
        """
        Pick a variable to assign a value.
        :return: variable, value assigned
        """
        var = next(self.all_unassigned_vars())
        return var, TRUE

    def conflict_analyze(self, conf_cls):
        """
        Analyze the most recent conflict and learn a new clause from the conflict.
        - Find the cut in the implication graph that led to the conflict
        - Derive a new clause which is the negation of the assignments that led to the conflict
        Returns a decision level to be backtracked to.
        :param conf_cls: (set of int) the clause that introduces the conflict
        :return: ({int} level to backtrack to, {set(int)} clause learnt)
        """
        def next_recent_assigned(clause):
            """
            According to the assign history, separate the latest assigned variable
            with the rest in `clause`
            :param clause: {set of int} the clause to separate
            :return: ({int} variable, [int] other variables in clause)
            """
            for v in reversed(assign_history):
                if v in clause or -v in clause:
                    return v, [x for x in clause if abs(x) != abs(v)]

        def find_cut_in_implication_graph(self, conf_cls, assign_history):
            pool_lits = conf_cls
            done_lits = set()
            curr_level_lits = set()
            prev_level_lits = set()

            while True:
                for lit in pool_lits:
                    if self.nodes[abs(lit)].level == self.level:
                        curr_level_lits.add(lit)
                    else:
                        prev_level_lits.add(lit)

                if len(curr_level_lits) == 1:
                    break

                last_assigned, others = self.next_recent_assigned(curr_level_lits, assign_history)

                done_lits.add(abs(last_assigned))
                curr_level_lits = set(others)

                pool_clause = self.nodes[abs(last_assigned)].clause
                pool_lits = [l for l in pool_clause if abs(l) not in done_lits] if pool_clause is not None else []

            return curr_level_lits, prev_level_lits
        
        if self.level == 0:
            return -1, None

        assign_history = [self.branching_history[self.level]] + list(self.propagate_history[self.level])

        curr_level_lits, prev_level_lits = self.find_cut_in_implication_graph(conf_cls, assign_history)

        learnt = frozenset([l for l in curr_level_lits.union(prev_level_lits)])
        if prev_level_lits:
            level = max([self.nodes[abs(x)].level for x in prev_level_lits])
        else:
            level = self.level - 1

        print(learnt)
        return level, learnt

    def backtrack(self, level):
        """
        Non-chronologically backtrack ("back jump") to the appropriate decision level,
        where the first-assigned variable involved in the conflict was assigned
        """
        self.backtrack_nodes(level)
        self.branching_vars = set([var for var in self.vars 
                                   if (self.assigns[var] != UNASSIGN and len(self.nodes[var].parents) == 0)])

        levels = list(self.propagate_history.keys())
        for k in levels:
            if k <= level:
                continue
            del self.branching_history[k]
            del self.propagate_history[k]
            
    def backtrack_nodes(self, level):
        """
        Remove all nodes with level greater than `level` and reset their values.
        """
        for var, node in self.nodes.items():
            if node.level <= level:
                node.children[:] = [child for child in node.children if child.level <= level]
            else:
                node.value = UNASSIGN
                node.level = -1
                node.parents = []
                node.children = []
                node.clause = None
                self.assigns[node.variable] = UNASSIGN

class ImplicationNode:
    """
    Represents a node in an implication graph. Each node contains
    - its value
    - its implication children (list)
    - parent nodes (list)
    """
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        self.level = -1
        self.parents = []
        self.children = []
        self.clause = None

# -1 2 3 -4 -5 
testcase = [[1, 2, -3], [-1, 2, 3], [2, 3],[-1],[1,2,3,4,5],[5,4,-3,-2,-1],[-4],[-5]]
solver = Solver(testcase, 5)
if solver.solve():
    print("SAT: ")
    for var in sorted(solver.assigns.keys()):
        value = solver.assigns[var]
        print(f"{-var if value == 0 else var}", end= " ")
else:
    print("UNSAT")