from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

PROHIBIDO = {
    (0,2),
    (1,3),
    (2,1)
}

ENTRADAS = {
    (0,4),
    (3,2)
}

MOVEMENTS = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0)
]

INITIAL_STATE = ((0,1),(0,1))
#               (Position Robot1, Position Robot2)

GOAL_STATE = ((0,4),(3,2))

class DefensiveRobotsProblem(SearchProblem):
    def is_goal(self, state):
        return set(state) == set(GOAL_STATE)
    
    def actions(self, state):

        possible_actions = []
        for robot_index, robot in enumerate(state):
            for movement in MOVEMENTS:
                robot_row, robot_column = robot
                movement_row, movement_column = movement
                new_row = robot_row + movement_row
                new_column = robot_column + movement_column
                new_position = tuple((new_row,new_column))

                if (0 <= new_row <= 3) and (0 <= new_column <= 4) and (new_position not in PROHIBIDO):
                    possible_actions.append((robot_index,new_position))

        return possible_actions

    def result(self, state, action):
        robot_index, new_position = action
        state = list(state)
        state[robot_index] = new_position
        state = tuple(state)

        #print(state)

        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Without heuristic
        # {'max_fringe_size': 46, 'visited_nodes': 235, 'iterations': 235}
        # return super().heuristic(state)

        # Difference between spawn point and one of the defensive positions
        # {'max_fringe_size': 59, 'visited_nodes': 174, 'iterations': 174}
        pos1, pos2 = state
        pos1_row, pos1_col = pos1
        pos2_row, pos2_col = pos2
        def1, def2 = ENTRADAS
        def1_row, def1_col = def1
        def2_row, def2_col = def2
        
        return abs(pos1_row - def1_row) + abs(pos1_col - def1_col)
        
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
    problem = DefensiveRobotsProblem(INITIAL_STATE)
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