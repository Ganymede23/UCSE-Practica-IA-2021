from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

WALLS = {
    (0,3), (0,5),
    (1,1), (1,3),
    (2,2), (2,4),
    (3,0),
    (4,1), (4,3), (4,5),
    (5,3)
}

ENTRANCE = (3,5)

MEALS = {
    (1,2),
    (3,4),
    (4,0)
}

MOVEMENTS = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0)
]

INITIAL_STATE = ((0,0),((1,2),(3,4),(4,0)))
#               (Position Ratabot,(Meal1,Meal2,Meal3))

GOAL_STATE = ((3,5),tuple())

class RatabotsProblem(SearchProblem):
    def is_goal(self, state):
        return state[0] == ENTRANCE and state[1] == tuple()
    
    def actions(self, state):
        possible_actions = []
        
        bot_pos, meals = state
        bot_row, bot_col = bot_pos
        for x in MOVEMENTS:
            new_row = bot_row + x[0]
            new_col = bot_col + x[1]
            if (0 <= new_row <= 5) and (0 <= new_col <= 5):
                new_pos = (new_row, new_col)
                possible_actions.append(new_pos)
        
        return possible_actions

    def result(self, state, action):
        new_pos = action
        bot_pos, meal_list = state
        state = list(state)
        meal_list = list(meal_list)
        if new_pos in meal_list:
            meal_list.remove(new_pos)
        meal_list = tuple(meal_list)
        state[0] = new_pos
        state[1] = meal_list
        state = tuple(state)

        #print(state)

        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Sin heurística:
        # {'max_fringe_size': 37, 'visited_nodes': 252, 'iterations': 252}
        # return super().heuristic(state)

        # Heuristica: Cantidad de comidas+1
        # {'max_fringe_size': 45, 'visited_nodes': 218, 'iterations': 218}
        bot_pos, meal_list = state
        return len(meal_list)+1

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
    problem = RatabotsProblem(INITIAL_STATE)
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