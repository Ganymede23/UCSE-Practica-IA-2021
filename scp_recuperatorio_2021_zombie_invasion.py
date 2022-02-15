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

problem_variables = ['z1','z2','z3','z4','z5','p1','p2','p3','p4','p5','p6','p7','protagonist','safe_zone']

ESQUINAS = [(0,0),(0,4),(4,0),(4,4)]

domains = {}
for variable in ['z1','z2','z3','z4','z5','p1','p2','p3','p4','p5','p6','p7']:
    domains[variable] = [(f,c) for f in range(5) for c in range(5)]
domains['protagonist'] = ESQUINAS
domains['safe_zone'] = ESQUINAS

constraints = []

def adjacent(value1, value2):
    f1, c1 = value1
    f2, c2 = value2
    return (abs(f1-f2) + abs(c1-c2)) == 1

def different(variables, values):
    value1, value2 = values
    return value1 != value2

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), different))

def protagonist_far_away_from_safe_zone(variables, values):
    value1, value2 = values
    f1, c1 = value1
    f2, c2 = value2
    if abs(f1-f2) == 4 and abs(c1-c2) == 4:
        return True

constraints.append((('protagonist','safe_zone'), protagonist_far_away_from_safe_zone))

def zombies_away_from_safe_zone(variables, values):
    safe_zone_pos, *zombie_list = values
    for zombie in zombie_list:
        if adjacent(safe_zone_pos,zombie):
            return False
    return True    

constraints.append((('safe_zone', 'z1', 'z2', 'z3', 'z4', 'z5'), zombies_away_from_safe_zone))


def zombies_not_too_close(variables, values):
    zombie_list = values
    amount = 0
    
    for zombie1 in zombie_list:
        amount = 0
        for zombie2 in zombie_list:
            if adjacent(zombie1,zombie2):
                amount += 1
            if amount > 2:
                return False
    return True    

constraints.append((('z1', 'z2', 'z3', 'z4', 'z5'), zombies_not_too_close))

def wall_next_to_safe_zone(variables, values):
    safe_zone_pos, *wall_list = values
    amount = 0
    for wall in wall_list:
        if adjacent(safe_zone_pos,wall):
            amount += 1
    if amount == 1:
        return True
    else:
        return False    

constraints.append((('safe_zone','p1','p2','p3','p4','p5','p6','p7'), wall_next_to_safe_zone))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
inicio = datetime.now()
segundos = (datetime.now() - inicio).total_seconds()
print(f"Tiempo total: {segundos}s")
pprint(solution)