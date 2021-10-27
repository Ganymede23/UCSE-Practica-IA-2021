from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


problem_variables = ['central', 'aux_a', 'aux_b']

domains = {
    'central': ['estandar1','estandar2','estandar3','42dejulio','costanera','ciclovialandia'],
    'aux_a': ['estandar1','estandar2','42dejulio','costanera','aeroclub'],
    'aux_b': ['estandar1','estandar2','estandar3','42dejulio','costanera','ciclovialandia']
}

NEIGHBORHOODS = {
    'industrial': ['estandar1','estandar3'],
    'estandar1': ['centro','costanera','estandar3','industrial','estandar2'],
    'estandar2': ['42dejulio','centro','estandar1'],
    'estandar3': ['costanera','estandar1','industrial'],
    'centro': ['aeroclub','ciclovialandia','42dejulio','estandar2','estandar1','costanera'],
    'costanera': ['aeroclub','centro','estandar1','estandar3'],
    'aeroclub': ['centro','costanera'],
    'ciclovialandia': ['42dejulio','centro','quintas'],
    '42dejulio': ['ciclovialandia','centro','estandar2'],
    'quintas': ['ciclovialandia']
}

constraints = []

# constraint: you can't have 2 stations on the same neighborhood

def different(variables, values):
    improv1, improv2 = values
    return improv1 != improv2

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), different))

# constraint: you can't have stations on adjacent neighborhoods 

def stations_not_on_adjacent_neighborhoods(variables, values):
    nbhd1, nbhd2 = values
    return(nbhd1 not in NEIGHBORHOODS[nbhd2])

for var1, var2 in combinations(problem_variables, 2):
    constraints.append(((var1,var2), stations_not_on_adjacent_neighborhoods))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)