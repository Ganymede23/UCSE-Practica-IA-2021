from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer
from itertools import combinations

INITIAL_STATE = (0,0,0)
GOAL_STATE = (5,1,8)

class AlienStarship(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE
    
    def actions(self, state):
        possible_actions = []
        new_value = 0
        cell1, cell2, cell3 = state

        # Red (+3)
        new_value = cell1 + 3
        if 0 <= new_value <= 9:
            possible_actions.append(('Red', new_value))
        # Green (-2)
        new_value = cell1 - 2
        if 0 <= new_value <= 9:
            possible_actions.append(('Green', new_value))
        # Yellow (Swap 1 and 2)
        possible_actions.append(('Yellow', -1))
        # Blue (Swap 2 and 3)
        possible_actions.append(('Blue', -1))

        return possible_actions

    def result(self, state, action):
        cell1, cell2, cell3 = state
        state = list(state)
        action_type, data = action
        aux = 0
        if action_type == 'Red':
            state[0] = data
        elif action_type == 'Green':
            state[0] = data
        elif action_type == 'Yellow':
            aux = state[0]
            state[0] = state[1]
            state[1] = aux
        else: #Blue
            aux = state[1]
            state[1] = state[2]
            state[2] = aux
        state = tuple(state)

        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Without heuristic
        # {'max_fringe_size': 126, 'visited_nodes': 908, 'iterations': 908}
        # return super().heuristic(state)

        # {'max_fringe_size': 131, 'visited_nodes': 715, 'iterations': 715}
        h = 0
        for cell in state:
            if cell not in GOAL_STATE:
                h += 1
        return h

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
    problem = AlienStarship(INITIAL_STATE)
    #result = search_algorithm(problem, graph_search = True, viewer = visor)
    result = astar(problem, graph_search = True, viewer = visor)
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