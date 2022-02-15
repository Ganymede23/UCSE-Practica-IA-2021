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

problem_variables = [(f,c) for f in range(5) for c in range(5)]
print(problem_variables)

ROW0 = [(0,c) for c in range(5)]
ROW1 = [(1,c) for c in range(5)]
ROW2 = [(2,c) for c in range(5)]
ROW3 = [(3,c) for c in range(5)]
ROW4 = [(4,c) for c in range(5)]

COL0 = [(r,0) for r in range(5)]
COL1 = [(r,1) for r in range(5)]
COL2 = [(r,2) for r in range(5)]
COL3 = [(r,3) for r in range(5)]
COL4 = [(r,4) for r in range(5)]

domains = {}
for variable in problem_variables:
    domains[variable] = ['red','white','blue','green']

constraints = []

def check_row(variables,values):
    grid = variables
    for index1, cell1 in enumerate(grid):
        for index2, cell2 in enumerate(grid):
            if cell1 != cell2 and abs(cell1[0]-cell2[0]) == 0: #If they are not the same cell and they are on the same row
                return values[index1] == values[index2]

def check_col(variables,values):
    pass

def different_corners(variables,values):
    check_row(variables,values)

    grid = variables
    for index1, cell1 in enumerate(grid):
        for index2, cell2 in enumerate(grid):
            if cell1 != cell2 and abs(cell1[0]-cell2[0]) == 0: #If they are not the same cell and they are on the same row
                if values[index1] == values[index2]:
                    for index3, cell3 in enumerate(grid):
                        if cell2 != cell3 and abs(cell2[1]-cell3[1]) == 0: #If they are not the same cell and they are on the same column
                            if values[index2] == values[index3]:
                                for index4, cell4 in enumerate(grid):
                                    if cell3 != cell4 and abs(cell3[0]-cell4[0]) == 0: #If they are not the same cell and they are on the same row
                                        if values[index3] == values[index4]:
                                            if values[index4] == values[index1]:
                                                return False
    return True

constraints.append((problem_variables, different_corners))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
inicio = datetime.now()
segundos = (datetime.now() - inicio).total_seconds()
print(f"Tiempo total: {segundos}s")
pprint(solution)