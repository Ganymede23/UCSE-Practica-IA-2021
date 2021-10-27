from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)


problem_variables = ['cnn1','cnn2','bbc','fox','oni','rt','msnbc1','msnbc2','msnbc3','bae1','bae2']

domains = {}

SEATS = [
    (1,  2,  3,  4),
    (5,  6,  7,  8),
    (9,  10, 11, 12)
]

for var in problem_variables:
    domains[var] = [5,6,7,8,9,10,11,12]

# overwriting some key domains
domains['cnn1'] = [2]                    # cnn have to be on 1st row together
domains['cnn2'] = [3]                    # cnn have to be on 1st row together
domains['bbc'] = [1]                     # bbc has to be on 1st row and can't be next to fox
domains['fox'] = [4]                     # fox has to be on 1st row and can't be next to bbc
domains['oni'] = [9,10,11,12]   # onion has to be on last row
domains['rt'].remove(6)                  # rt can't seat next or behind cnn
domains['rt'].remove(7)                  # rt can't seat next or behind cnn
#domains['msnbc1'] = [5]                  # msnbc have to be together
#domains['msnbc2'] = [6]                  # msnbc have to be together
#domains['msnbc3'] = [7]                  # msnbc have to be together
constraints = []

# constraint: you can't have 2 jouralists on the same seat

def different(variables, values):
    value1, value2 = values
    print(variables)
    print(values)    
    return value1 != value2

for var1, var2 in combinations(problem_variables,2):
    constraints.append(((var1, var2), different))

# constraint: msnbc journalists have to be together on same row 


# constraint: infobae journalists can't be together 
def infobae_stay_apart(variables, values):
    var1, var2 = variables
    value1, value2 = values
    if (var1 == 'bae1' or var1 == 'bae2') and (var2 == 'bae1' or var2 == 'bae2'): # si son de infobae
        if (value1 in SEATS[1] and value2 in SEATS[1]) or (value1 in SEATS[2] and value2 in SEATS[2]): # si están en la misma fila
            if (value1 == value2 + 1 or value1 == value2 - 1): # si están juntos
                return False
    return True

for var1, var2 in combinations(problem_variables,2):
    constraints.append(((var1,var2), infobae_stay_apart))


problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)