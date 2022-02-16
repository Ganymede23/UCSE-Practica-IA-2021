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

INITIAL_STATE = (('w','w','e','e','c','c'),(),())

class PresidentsProblem(SearchProblem):
    def is_goal(self, state):
        return len(state[2]) == 6
    
    def actions(self, state):
        possible_actions = []

        room1, room2, room3 = state
        rooms = [room1, room2, room3]

        for index, room in enumerate(rooms):
            if len(room) == 1:
                possible_actions.append(room[0],index+1)
            elif len(room) > 1:
                couples = tuple(combinations(room),2)
                for couple in couples:
                 
            else:
                pass

        return possible_actions

    def result(self, state, action):
        button, new_value1, new_value2 = action
        state = list(state)
        if button == 'red':
            state[0] = new_value1
        elif button == 'green':
            state[0] = new_value1
        elif button == 'yellow':
            state[0] = new_value1
            state[1] = new_value2
        elif button == 'cyan':
            state[1] = new_value1
            state[2] = new_value2
        state = tuple(state)
        #print(state)
        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Sin heuristica
        return super().heuristic(state)


METHODS = (
    #breadth_first,
    #depth_first,
    #uniform_cost,
    #greedy,
    astar
)    
        
for search_algorithm in METHODS:
    print()
    print('=' * 50)
    print("Running:", search_algorithm)
    visor = BaseViewer()
    problem = AlienStarshipProblem(INITIAL_STATE)
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