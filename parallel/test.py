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

test_case = set()
num = 60
f = open("cases/" + str(num) +".cnf", "r")
for line in f:
    test_case.add(frozenset({int(x) for x in line.split()}))

print(dpll(test_case))

cnf = set()
for clause in test_case:
    cnf.add(frozenset(map(int, clause)))
    solver = Solver(cnf, num)

print(solver.solve())

print(naive(test_case))