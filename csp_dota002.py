from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

problem_variables = ['slot1','slot2','slot3']
domains = {
    'slot1': [('assault_cuirass',5000),('battlefury',4000),('cloak',500),('hyperstone',2000),('quelling_blade',200),('shadow_blade',3000),('veil_of_discord',2000)],
    'slot2': [('assault_cuirass',5000),('battlefury',4000),('cloak',500),('hyperstone',2000),('quelling_blade',200),('shadow_blade',3000),('veil_of_discord',2000)],
    'slot3': [('battlefury',4000),('veil_of_discord',2000)]
}

constraints = []

def different(variables, values):
    value1, value2 = values
    return value1 != value2

for variable1, variable2 in combinations(problem_variables,2):
    constraints.append(((variable1, variable2), different))

def money_is_enough(variables, values):
    value1, value2, value3 = values
    total_sum = value1[1] + value2[1] + value3[1]
    return total_sum <= 6000

constraints.append((problem_variables, money_is_enough))

def hyperstone_and_shadow_blade(variables, values):
    value1, value2 = values
    has_hyperstone = 'hyperstone' in [value1, value2]
    has_shadow_blade = 'shadow_blade' in [value1, value2]

    if has_hyperstone and has_shadow_blade:
        return False
    return True

def quelling_blade_and_shadow_blade(variables, values):
    value1, value2 = values
    has_quelling_blade = 'quelling_blade' in [value1, value2]
    has_shadow_blade = 'shadow_blade' in [value1, value2]

    if has_quelling_blade and has_shadow_blade:
        return False
    return True

def cloak_and_veil_of_discord(variables, values):
    value1, value2 = values
    has_cloak = 'cloak' in [value1, value2]
    has_veil_of_discord = 'veil_of_discord' in [value1, value2]

    if has_cloak and has_veil_of_discord:
        return False
    return True

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)