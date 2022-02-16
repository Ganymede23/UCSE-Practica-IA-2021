from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

INITIAL_STATE = (0,0,0)
GOAL_STATE = (5,1,8)

class AlienStarshipProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE
    
    def actions(self, state):
        possible_actions = []

        for x in range(0,4):
            value1, value2, value3 = state
            aux = 0

            if x == 0:      #red
                value1 += 3
                if (0 <= value1 <= 9):
                    possible_actions.append(('red',value1,-1))
            elif x == 1:    #green
                value1 -= 2
                if (0 <= value1 <= 9):
                    possible_actions.append(('green',value1,-1))
            elif x == 2:    #yellow
                aux = value1
                value1 = value2
                value2 = aux
                possible_actions.append(('yellow',value1,value2))
            elif x == 3:    #cyan
                aux = value2
                value2 = value3
                value3 = aux
                possible_actions.append(('cyan',value2,value3))

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
        # return super().heuristic(state)
        # {'max_fringe_size': 126, 'visited_nodes': 908, 'iterations': 908}

        # Heuristica: cantidad de casillas que faltan para llegar al goal
        # {'max_fringe_size': 146, 'visited_nodes': 724, 'iterations': 724}
        value1, value2, value3 = state
        goal1, goal2, goal3 = GOAL_STATE
        x = 0
        if value1 != goal1:
            x += 1
        if value2 != goal2:
            x += 1
        if value3 != goal3:
            x += 1
        
        return x

METHODS = (
    #breadth_first,
    depth_first,
    #uniform_cost,
    greedy,
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