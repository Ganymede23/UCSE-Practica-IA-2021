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

#my_viewer = ConsoleViewer()
problem = DefensiveRobotsProblem(INITIAL_STATE)
result = astar(problem, graph_search=True)
print(result)
    