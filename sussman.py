from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar
)
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

INITIAL_STATE = (('B'),('C','A'),())

GOAL_STATE = ((),(),('A','B','C'))

class SussmanProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL_STATE
    
    def actions(self, state):
        possible_actions = []

        for tower_index, tower in enumerate(state):
            if len(tower) != 0:
                tower = list(tower)
                block = tower[0]
                #tower.remove(block)
                tower = tuple(tower)
                if tower_index == 0:
                    possible_actions.append(tuple((block,0,1)))
                    possible_actions.append(tuple((block,0,2)))
                elif tower_index == 1:
                    possible_actions.append(tuple((block,1,-1)))
                    possible_actions.append(tuple((block,1,1)))    
                else: #tower_index == 2
                    possible_actions.append(tuple((block,2,1)))
                    possible_actions.append(tuple((block,2,0))) 

        return possible_actions

    def result(self, state, action):
        block, old_tower_index, new_tower_index = action
        state = list(state)

        old_tower = list(state[old_tower_index])
        old_tower.remove(block)
        state[old_tower_index] = tuple(old_tower)

        new_tower = list(state[new_tower_index])
        new_tower.insert(0,block)
        state[new_tower_index] = tuple(new_tower)

        state = tuple(state)
        #print(state)
        return state

    def cost(self, state, action, state2):
        return 1

#my_viewer = ConsoleViewer()
problem = SussmanProblem(INITIAL_STATE)
result = astar(problem, graph_search=True)
print(result)
    