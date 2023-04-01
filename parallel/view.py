import random
import timeit
import matplotlib.pyplot as plt
from pysat.solvers import Glucose3
import pandas as pd 
import numpy as np
import threading
import math
from cdcl_self import Solver
import os

df = pd.read_csv("combined.csv")

ax = df.plot(kind="scatter", x="num_vars",y="dpll_time", color="r", label="dpll")
df.plot(kind="scatter", x="num_vars",y="cdcl_time", color="g", label="cdcl", ax=ax)

plt.show()