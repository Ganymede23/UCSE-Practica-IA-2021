from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

problem_variables = ['central','aux_a','aux_b']

domains = {
    'central': ['estandar1','estandar2','estandar3','costanera','ciclovialandia','42dejulio'],
    'aux_a': ['42dejulio','estandar1','estandar2','costanera','aeroclub'],
    'aux_b': ['estandar1','estandar2','estandar3','costanera','42dejulio','ciclovialandia']
}

ADYACENTES = {
    'industrial': ['estandar1', 'estandar3'],
    'estandar1': ['estandar2','industrial','estandar3','costanera','centro'],
    'estandar2': ['42dejulio','centro','estandar1'],
    'estandar3': ['industrial','costanera','estandar1'],
    'costanera': ['estandar1','estandar3','centro','aeroclub'],
    'aeroclub': ['centro','costanera'],
    'ciclovialandia': ['centro','42dejulio','quintas'],
    'quintas': ['ciclovialandia'],
    '42dejulio': ['ciclovialandia','centro','estandar2']
}

constraints = []

def allDiff(variables, values):
    value1, value2 = values
    return value1 != value2

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1,variable2),allDiff))

def estaciones_no_adyacentes(variables, values):
    value1, value2 = values
    if value1 in ADYACENTES[value2]:
        return False
    return True

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)


