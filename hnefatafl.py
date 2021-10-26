from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

INITIAL_STATE = (3,3)

BORDERS = []

for x in range(0,7):
    BORDERS.append((0,x))
    BORDERS.append((6,x))
    BORDERS.append((x,0))
    BORDERS.append((x,6))

MOVEMENTS = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]

SOLDIERS = [(0,0),(0,1),(0,4),
            (1,4),
            (2,0),
            (3,1),(3,6),
            (4,0),
            (6,3),(6,5)]

SOLDIERS_RANGE = []

for soldier in SOLDIERS:
    soldier_row, soldier_col = soldier
    for soldier_move in MOVEMENTS:
        soldier_move_row, soldier_move_col = soldier_move
        soldier_range = (soldier_row + soldier_move_row, soldier_col + soldier_move_col)
        SOLDIERS_RANGE.append(soldier_range)

class HnefataflProblem(SearchProblem):
    def is_goal(self, state):
        return state in BORDERS
    
    def actions(self, state):
        possible_actions = []
        king_row, king_col = state
        for move in MOVEMENTS:
            move_row, move_col = move
            new_row = king_row + move_row
            new_col = king_col + move_col
            new_pos = (new_row,new_col)
            if new_pos not in SOLDIERS_RANGE:
                possible_actions.append(new_pos)

        return possible_actions

    def result(self, state, action):
        new_pos = action
        state = list(state)

        state = new_pos

        state = tuple(state)
        #print(state)
        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # return 1
        king_row, king_col = state
        king_pos = (king_row, king_col)
        # (3,3)
        min_distance_right =  6 - king_col
        min_distance_left = king_col            # == king_col - 0
        min_distance_top = king_row             # == king_row - 0
        min_distance_botton = 6 - king_row
        min_distance = min(list((min_distance_right,min_distance_left,min_distance_top,min_distance_botton)))
        return(min_distance)


METHODS = (
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)    
        
for search_algorithm in METHODS:
    print()
    print('=' * 50)
    print("Running:", search_algorithm)
    visor = BaseViewer()
    problem = HnefataflProblem(INITIAL_STATE)
    result = search_algorithm(problem, graph_search = True, viewer = visor)
    print ('Final State:', result.state)
    print('=' * 50)
    print(' - Statistics:')
    print(' - Amount of actions until goal:', len(result.path()))
    print(' - Raw data:', visor.stats)
    '''
    for action, state in result.path():
        print("   - Action:", action)
        print("   - Resulting State:", state)
    '''