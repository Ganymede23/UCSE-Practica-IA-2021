import time
from datetime import datetime
from itertools import combinations
from pprint import pprint

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

problem_variables = [(0,0),(1,0),(1,1),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2),(3,3)]

#          (0,0)
#       (1,0)(1,1)
#    (2,0)(2,1)(2,2)  
# (3,0)(3,1)(3,2)(3,3)

domains = {}
for var in problem_variables:
    domains[var] = [n for n in range(51)]
    domains[var].remove(0)

BASE_CELLS = {
    (0,0): [(1,0),(1,1)],
    (1,0): [(2,0),(2,1)],
    (1,1): [(2,1),(2,2)],
    (2,0): [(3,0),(3,1)],
    (2,1): [(3,1),(3,2)],
    (2,2): [(3,2),(3,3)],
    (3,0): [],
    (3,1): [],
    (3,2): [],
    (3,3): []
}

constraints = []

def all_diff(variables, values):
    value1, value2 = values
    return value1 != value2

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1,variable2), all_diff))

def sum_cells(variables, values):
    var1, var2, var3 = variables
    val1, val2, val3 = values
    if var2 in BASE_CELLS[var1] and var3 in BASE_CELLS[var1]:
        return val1 == val2 + val3
    return True

for variable1, variable2, variable3 in combinations(problem_variables,3):
    constraints.append(((variable1,variable2,variable3), sum_cells))

inicio = datetime.now()
problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
segundos = (datetime.now() - inicio).total_seconds()
print(f"Tiempo total: {segundos}s")
pprint(solution)