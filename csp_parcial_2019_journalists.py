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
    (0,0), (0,1), (0,2), (0,3),
    (1,0), (1,1), (1,2), (1,3),
    (2,0), (2,1), (2,2), (2,3)
]

for var in problem_variables:
    domains[var] = [(1,0), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3)]

# overwriting some key domains
domains['cnn1'] = [(0,1)]                       # cnn have to be on 1st row together
domains['cnn2'] = [(0,2)]                       # cnn have to be on 1st row together
domains['bbc'] = [(0,0), (0,3)]                 # bbc has to be on 1st row and can't be next to fox
domains['fox'] = [(0,0), (0,3)]                 # fox has to be on 1st row and can't be next to bbc
domains['oni'] = [(2,0), (2,1), (2,2), (2,3)]   # onion has to be on last row
domains['rt'].remove((1,1))                     # rt can't seat next or behind cnn
domains['rt'].remove((1,2))                     # rt can't seat next or behind cnn
#domains['msnbc1'] = [(1,1), (1,2), (1,3)]      # msnbc have to be together
#domains['msnbc2'] = [(1,1), (1,2), (1,3)]      # msnbc have to be together
#domains['msnbc3'] = [(1,1), (1,2), (1,3)]      # msnbc have to be together
constraints = []

# constraint: you can't have 2 jouralists on the same seat

def different(variables, values):
    value1, value2 = values
    #print(variables)
    #print(values)    
    return value1 != value2

for var1, var2 in combinations(problem_variables,2):
    constraints.append(((var1, var2), different))

# constraint: msnbc journalists have to be together on same row 
def msnbc_stay_together(variables, values):
    value1, value2, value3 = values

    if (value1[0] == value2[0]) and (value1[0] == value3[0]): # si están en la misma fila
        x = [value1[1],value2[1],value3[1]]
        if x == [1,2,3] or x == [0,1,2]: # si están juntos
            return True
    return False

constraints.append((('msnbc1','msnbc2','msnbc3'), msnbc_stay_together))

# constraint: infobae journalists can't be together 
def infobae_stay_apart(variables, values):
    var1, var2 = variables
    value1, value2 = values
    #if (var1 == 'bae1' or var1 == 'bae2') and (var2 == 'bae1' or var2 == 'bae2'): # si son de infobae
    if (value1[0] == value2[0]): # si están en la misma fila
        if (value1[1] == value2[1]-1 or value1[1] == value2[1]+1): # si están juntos
            return False
    return True

#for var1, var2 in combinations(problem_variables,2):
#    constraints.append(((var1,var2), infobae_stay_apart))
constraints.append((('bae1','bae2'), infobae_stay_apart))

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print('Solution:')
print(solution)