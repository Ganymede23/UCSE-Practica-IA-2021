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

PARK_GRID = [(r,c) for r in range(5) for c in range(5)]
problem_variables = PARK_GRID

domains = {}
for variable in problem_variables:
    domains[variable] = ['trees','nests','games','sidewalks','grass']
    if variable[0] == 0:
        domains[variable].remove('sidewalks')

def adjacent(grid1, grid2):
    r1,c1 = grid1
    r2,c2 = grid2
    return abs(r1-r2) + abs(c1-c2) == 1

def adjacent_vertically(grid1, grid2):
    r1,c1 = grid1
    r2,c2 = grid2
    if c1 == c2:  
        return abs(r1-r2) == 1
    return False

constraints = []

def more_green(variables, values):
    sidewalk_counter = 0
    green_counter = 0
    nests_counter = 0
    games_counter = 0
    for value in values:
        if value == 'sidewalks':
            sidewalk_counter += 1
        elif value == 'trees' or value == 'grass':
            green_counter += 1
        elif value == 'nests':
            nests_counter += 1
        else:
            games_counter += 1

    return green_counter > sidewalk_counter and sidewalk_counter > 1 and nests_counter > 0 and games_counter > 0
    # nests, sidewalk and games counters added to the return to force algorithm to use a few of those

constraints.append((problem_variables, more_green))

def nests_away_from_sidewalks_and_games(variables, values):
    value1, value2 = values
    grid1, grid2 = variables
    if adjacent(grid1, grid2):
        if 'nests' in [value1, value2]:
            if 'sidewalks' in [value1, value2] or 'games' in [value1, value2]:
                return False
    return True

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1,variable2), nests_away_from_sidewalks_and_games))

def different_stuff_on_adjacent(variables, values):
    value1, value2 = values
    grid1, grid2 = variables
    if adjacent(grid1, grid2):
        return value1 != value2
    return True

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1,variable2), different_stuff_on_adjacent))

def trees_north_of_sidewalk(variables, values):
    value1, value2 = values
    grid1, grid2 = variables
    if 'sidewalk' in [value1, value2]:
        if adjacent_vertically(grid1, grid2):
            if value1 == 'sidewalk':
                return value2 == 'trees'
            else:
                return value1 == 'trees'
    return True

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1,variable2), trees_north_of_sidewalk))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
inicio = datetime.now()
segundos = (datetime.now() - inicio).total_seconds()
print(f"Tiempo total: {segundos}s")
pprint(solution)