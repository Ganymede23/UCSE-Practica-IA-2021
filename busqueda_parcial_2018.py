from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

INITIAL_STATE = (0,0)
GOAL_STATE = (5,5)

WALLS = [
    (0,1),
    (1,0),(1,4),
    (2,3),
    (3,1),(3,2),(3,5),
    (4,0),(4,2),(4,4),
    (5,2),(5,3)
]

MOVEMENTS = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]

class RobotsImpacientesProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE
    
    def actions(self, state):
        possible_actions = []
        robot_row, robot_col = state
        
        for movement in MOVEMENTS:
            movement_row, movement_column = movement
            new_row = robot_row + movement_row
            new_col = robot_col + movement_column
            new_pos = tuple((new_row,new_col))

            if (0 <= new_row <= 5) and (0 <= new_col <= 5):
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
        new_pos = action
        if new_pos in WALLS:
            return 20
        else:
            return 10
    
    def heuristic(self, state):
        # Sin heuristica
        # greedy:   {'max_fringe_size': 11, 'visited_nodes': 32, 'iterations': 32}
        # astar:    {'max_fringe_size': 7, 'visited_nodes': 36, 'iterations': 36}
        #return super().heuristic(state)

        # Heuristica: cantidad de movimientos restantes x 10
        # greedy:   {'max_fringe_size': 9, 'visited_nodes': 11, 'iterations': 11}
        # astar:    {'max_fringe_size': 9, 'visited_nodes': 31, 'iterations': 31}
        pos_row, pos_col = state
        goal_row, goal_col = GOAL_STATE
        min_amount_of_movements_to_goal = (goal_row - pos_row) + (goal_col - pos_col)
        return min_amount_of_movements_to_goal * 10

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
    problem = RobotsImpacientesProblem(INITIAL_STATE)
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