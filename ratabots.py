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

ENTRANCE = {
    (3,5)
}

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
        return state == GOAL_STATE
    
    def actions(self, state):
        possible_actions = []
        
        ratabot_pos, meals = state
        ratabot_row, ratabot_col = ratabot_pos

        for move in MOVEMENTS:
            move_row, move_col = move
            new_row = ratabot_row + move_row
            new_col = ratabot_col + move_col
            new_pos = tuple((new_row,new_col))

            if (0 <= new_row <= 5) and (0 <= new_col <= 5) and (new_pos not in WALLS):
                possible_actions.append(new_pos)
        
        return possible_actions

    def result(self, state, action):

        new_pos = action
        ratabot_pos, meals = state
        
        state = list(state)
        state[0] = new_pos #reemplaza la posición

        if new_pos in meals:
            meals = list(meals)
            meals.remove(new_pos) #quita la comida
            meals = tuple(meals)
            state[1] = meals #reemplaza la tupla de comidas
        
        state = tuple(state)

        print(state)

        return state

    def cost(self, state, action, state2):
        return 1

#my_viewer = ConsoleViewer()
problem = RatabotsProblem(INITIAL_STATE)
result = astar(problem, graph_search=True)
print("Goal node:", result)

print("Path from initial state to goal:")
for action, state in result.path():
    print("Action:", action)
    print("State:", state)
    