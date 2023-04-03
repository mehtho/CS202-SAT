from compare import dpll, naive
import random
import timeit
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import threading
import math
from cdcl202 import Solver
import os

test_case = []
num = 60
f = open("cases/" + str(num) +".cnf", "r")
for line in f:
    test_case.append([int(x) for x in line.split()])
print(test_case)

print(dpll(test_case, []))

cnf = set()
for clause in test_case:
    cnf.add(frozenset(map(int, clause)))
    solver = Solver(cnf, num)

print(solver.solve())

print(naive(test_case))