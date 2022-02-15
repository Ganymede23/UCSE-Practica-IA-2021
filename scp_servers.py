from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

problem_variables = ['limpiador','convertidor','entrenador','almacenador','graficador','servidor']

REQUIREMENTS = {
    # [CPU, RAM]
    'limpiador': [2,10],
    'convertidor': [5,20],
    'entrenador': [2,14],
    'almacenador': [1,1],
    'graficador': [2,2],
    'servidor': [2,8]
}

SERVERS = {
    # [CPU, RAM]
    'tesla': [8,32,0],
    'goedel': [4,16,1],
    'bohr': [4,16,0],
}

domains = {
    'limpiador': ['tesla','bohr'],
    'convertidor': ['tesla'],
    'entrenador': ['goedel'],
    'almacenador': ['tesla','goedel','bohr'],
    'graficador': ['tesla','goedel','bohr'],
    'servidor': ['tesla','bohr']
}

constraints = []

def meet_requirements(variables, values):
    task1, task2 = variables
    serv1, serv2 = values
    task1_cpu = REQUIREMENTS[task1][0]
    task1_ram = REQUIREMENTS[task1][1]
    task2_cpu = REQUIREMENTS[task2][0]
    task2_ram = REQUIREMENTS[task2][1]
    if serv1 == serv2: # Si el servidor es el mismo
        server_cpu = SERVERS[serv1][0]
        server_ram = SERVERS[serv1][1]
        return(task1_cpu + task2_cpu <= server_cpu) and (task1_ram + task2_ram <= server_ram)
    return True

for task1, task2 in combinations(problem_variables, 2):
    constraints.append(((task1,task2),meet_requirements))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)