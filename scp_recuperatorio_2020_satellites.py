from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    HIGHEST_DEGREE_VARIABLE,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)

SLOTS = ['S1', 'S2', 'S3','MS1','MS2'] #variables

SATS = { #dominios
    'Arab': ('N',300),
    'Bio': ('M',60),
    'Comms': ('N',700),
    'Micro': ('M',80),
    'Nu': ('M',40),
    'Radar': ('N',400),
    'Super': ('N',500),
    'Test': ('M',30),
    'XSat': ('N',600),
}

NORMALES = ['Arab','Comms','Radar','Super','XSat']

problem_variables = SLOTS

domains={
    'MS1': ['Bio','Micro','Comms','Nu','Test'],
    'MS2': ['Bio','Micro','Comms','Nu','Test'],
    'S1': ['Arab','Comms','Super','XSat','Bio','Micro','Comms','Nu','Test'],
    'S2': ['Arab','Comms','Super','XSat','Bio','Micro','Comms','Nu','Test'],
    'S3': ['Arab','Comms','Radar','XSat','Bio','Micro','Comms','Nu','Test']
}

constraints=[]

def weight(variables, values):
    s1, s2, s3, ms1, ms2 = values
    total_weight = SATS[s1][1]+SATS[s2][1]+SATS[s3][1]+SATS[ms1][1]+SATS[ms2][1]
    print(total_weight)
    return total_weight <= 1500

constraints.append((problem_variables,weight))

def different(variables,values):
    value1,value2 = values
    return value1 != value2

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), different))

def XSat_not_under_MicroComms(variables, values):
    value1, value2 = values
    var1, var2 = variables
    if var1 == 's1' and var2 == 'ms1':
        if value1 == 'XSat':
            return value2 != 'Micro'
    if var1 == 's2' and var2 == 'ms2':
        if value1 == 'XSat':
            return value2 != 'Micro'
    return True

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), XSat_not_under_MicroComms))

def TestSat_not_above_midsize(variables, values):
    value1, value2 = values
    var1, var2 = variables
    if var1 == 's1' and var2 == 'ms1':
        if value2 == 'Test':
            return value1 not in NORMALES
    if var1 == 's2' and var2 == 'ms2':
        if value2 == 'Test':
            return value1 not in NORMALES
    return True

for variable1, variable2 in combinations(problem_variables, 2):
    constraints.append(((variable1, variable2), TestSat_not_above_midsize))    

problem = CspProblem(problem_variables, domains, constraints)
solution = backtrack(problem)

print("Solution:")
print(solution)