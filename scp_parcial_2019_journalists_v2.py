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

problem_variables = ['cnn1','cnn2','fox','bbc','oni','msn1','msn2','msn3','rto','inf1','inf2']

domains = {
    'cnn1': [(0,1),(0,2)],
    'cnn2': [(0,1),(0,2)],
    'fox': [(0,0)],
    'bbc': [(0,3)],
    'oni': [(2,0),(2,1),(2,2),(2,3)],
    'msn1': [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)],
    'msn2': [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)],
    'msn3': [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)],
    'rto': [(1,0),(1,3),(2,0),(2,1),(2,2),(2,3)],
    'inf1': [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)],
    'inf2': [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
}

constraints = []

def different_seats(variables, values):
    seat1, seat2 = values
    return seat1 != seat2

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1,variable2), different_seats))

def msnbc_adjacent(variables, values):
    seat1, seat2, seat3 = values
    r1,c1 = seat1
    r2,c2 = seat2
    r3,c3 = seat3
    return (abs(r1-r2) + abs(c1-c2) == 1) and (abs(r2-r3) + abs(c2-c3) == 1)

constraints.append((('msn1','msn2','msn3'), msnbc_adjacent))

def infobae_not_adjacent(variables, values):
    seat1, seat2 = values
    r1,c1 = seat1
    r2,c2 = seat2
    if abs(r1-r2) + abs(c1-c2) == 1:
        return False
    return True

constraints.append((('inf1','inf2'), infobae_not_adjacent))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
inicio = datetime.now()
segundos = (datetime.now() - inicio).total_seconds()
print(f"Tiempo total: {segundos}s")
pprint(solution)