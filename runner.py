#idea add graph
import numpy as np
import matplotlib.pyplot as plt
from geneticbit import genetic_finderb
from genetic import genetic_findera
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize as pymoo_minimize
import os
import glob
import time


import random

np.random.seed(42)
random.seed(42)

_ref_dirs = get_reference_directions("das-dennis", 1, n_partitions=1)


class _PymooWrapper(Problem):
    def __init__(self, prob):
        lo, hi = prob.bounds
        super().__init__(n_var=1, n_obj=1, xl=np.array([lo]), xu=np.array([hi]))
        self.prob = prob
    def _evaluate(self, X, out, *args, **kwargs):
        out["F"] = self.prob._evaluate(X[:, 0]).reshape(-1, 1)


def nsga3_finder(problem, population):
    algorithm = NSGA3(pop_size=population, ref_dirs=_ref_dirs)
    res = pymoo_minimize(_PymooWrapper(problem), algorithm, ('n_gen', 100), verbose=False)
    return float(res.X[0]), float(res.F[0])


class Problem1:
    def __init__(self):
        self.bounds = (-1, 6)
    def _evaluate(self, x):
        return 10 + x**2 - 10 * np.cos(2 * np.pi * x)
    def solution(self):
        return (0.0, 0.0)


class Problem2:
    def __init__(self):
        self.bounds = (0, 2)
    def _evaluate(self, x):
        return x**2 * np.sin(1 / (x**2 + 0.001)) + 0.3 * x**2 + np.cos(x**2 / 4)
    def solution(self):
        return (0.467373, 0.848231)


class Problem3:
    def __init__(self):
        self.bounds = (0, 10)
    def _evaluate(self, x):
        return np.sin(x**2) + 0.05 * x**2 - np.cos(3 * x)
    def solution(self):
        return (2.137898, -1.752931)


class Problem4:
    def __init__(self):
        self.bounds = (-500, 500)
    def _evaluate(self, x):
        return 418.9829 - x * np.sin(np.sqrt(np.abs(x)))
    def solution(self):
        return (420.968750, 0.000013)


class Problem5:
    def __init__(self):
        self.bounds = (-1, 12)
    def _evaluate(self, x):
        return 1 + x**2 / 4000 - np.cos(x)
    def solution(self):
        return (0.0, 0.0)


class Problem6:
    def __init__(self):
        self.bounds = (-33, 33)
    def _evaluate(self, x):
        return -20 * np.exp(-0.2 * np.sqrt(x**2)) - np.exp(np.cos(2 * np.pi * x)) + 20 + np.e
    def solution(self):
        return (0.0, 0.0)



problems = [Problem1(), Problem2(), Problem3(), Problem4(), Problem5(), Problem6()]
populations = [5,10,20,50,100,150,200]

OUTPUT_DIR = 'figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)
for f in glob.glob(os.path.join(OUTPUT_DIR, '*_error_plot.png')):
    os.remove(f)
# aggiungi tempo 
x = time.time()
for prob, problem in enumerate(problems):
    x_coordinates_bit = []
    y_coordinates_bit = []
    x_coordinates_arit = []
    y_coordinates_arit = []
    
    pop = []
    errora = []
    errorb = []
    errorc = []
    RUNS =5
    for _, population in enumerate(populations):
       print(f"pop: {population}, prob: {prob}")

       run_errora = []
       run_errorb = []
       run_errorc = []
       for _ in range(RUNS):
           xa , ya = genetic_findera(problem,population)
           xb , yb = genetic_finderb(problem,population)
           xc , yc = nsga3_finder(problem,population)
           x_coordinates_arit = (xa-problem.solution()[0])
           y_coordinates_arit = (ya-problem.solution()[1])
           x_coordinates_bit = (xb-problem.solution()[0])
           y_coordinates_bit = (yb-problem.solution()[1])
           run_errora.append(abs(x_coordinates_arit))
           run_errorb.append(abs(x_coordinates_bit))
           run_errorc.append(abs(xc-problem.solution()[0]))

       pop.append(population)
       errora.append(np.mean(run_errora))
       errorb.append(np.mean(run_errorb))
       errorc.append(np.mean(run_errorc))


    plt.figure()
    plt.plot(pop, errora, 'bo-', label='Arithmetic Encoding (|x_error| )')
    plt.plot(pop, errorb, 'ro-', label='Bit Encoding (|x_error||)')
    plt.plot(pop, errorc, 'go-', label='NSGA-III pymoo (|x_error| )')
    plt.yscale('log')
    plt.xlabel('Population Size')
    plt.ylabel('Total Absolute Error (|x - x_optimal| )')
    plt.legend()
    plt.title(type(problem).__name__)
    plt.savefig(os.path.join(OUTPUT_DIR, f'{type(problem).__name__}_error_plot.png'))
    plt.close()

print(time.time() - x)
