from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

problem_variables = [
    'sopaperizador','inhibidor_cuantico','monitorimatic',
    'regulador_entropia','generador_antimateria',
    'derretidor_iones','compilador_resultados','explotador_conejillos']

domains = {
    'sopaperizador': [3,4,5,6,7,8],
    'inhibidor_cuantico': [4,5,6,7,8],
    'monitorimatic': [1],
    'regulador_entropia': [2,3,4,5,6,7,8],
    'generador_antimateria': [5,6,7,8],
    'derretidor_iones': [4,5,6,7,8],
    'compilador_resultados': [6,7,8],
    'explotador_conejillos': [2,3,4,5,6,7,8],
}

constraints = []

#------------------------------------------------------------

def alldiff(variables, values):
    value1, value2 = values
    return value1 != value2

for var1, var2 in combinations(problem_variables,2):
    constraints.append(((var1,var2), alldiff))

#------------------------------------------------------------

def regulador_entropia_before_sopaperizador(variables, values):
    value_regulador, value_sopaperizador = values
    return value_regulador < value_sopaperizador

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('regulador_entropia','sopaperizador'), regulador_entropia_before_sopaperizador))

#------------------------------------------------------------

def generador_antimateria_after_sopaperizador(variables, values):
    value_generador, value_sopaperizador = values
    return value_generador > value_sopaperizador

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('generador_antimateria','sopaperizador'), generador_antimateria_after_sopaperizador))

#------------------------------------------------------------

def derretidor_iones_before_generador(variables, values):
    value_derretidor, value_generador = values
    return value_derretidor < value_generador 

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('derretidor_iones','generador_antimateria'), derretidor_iones_before_generador))

#------------------------------------------------------------

def derretidor_iones_after_sopaperizador(variables, values):
    value_derretidor, value_sopaperizador = values
    return value_derretidor > value_sopaperizador 

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('derretidor_iones','sopaperizador'), derretidor_iones_after_sopaperizador))

#------------------------------------------------------------

def compilador_after_derretidor(variables, values):
    value_compilador, value_derretidor = values
    return value_compilador > value_derretidor

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('compilador_resultados','derretidor_iones'), compilador_after_derretidor))

#------------------------------------------------------------

def compilador_after_generador(variables, values):
    value_compilador, value_generador = values
    return value_compilador > value_generador

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('compilador_resultados','generador_antimateria'), compilador_after_generador))

#------------------------------------------------------------

def explotador_before_regulador(variables, values):
    value_explotador, value_regulador = values
    return value_explotador < value_regulador

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('explotador_conejillos','regulador_entropia'), explotador_before_regulador))

#------------------------------------------------------------

def explotador_before_inhibidor(variables, values):
    value_explotador, value_inhibidor = values
    return value_explotador < value_inhibidor

for var1, var2 in combinations(problem_variables, 2):
    constraints.append((('explotador_conejillos','inhibidor_cuantico'), explotador_before_inhibidor))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)