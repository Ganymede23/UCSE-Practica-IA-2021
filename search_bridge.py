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
from math import ceil

INITIAL_STATE = ((10,30,60,80,120),(),0,300)
#GOAL_STATE = ((),(10,30,60,80,120),0,_)

class BridgeProblem(SearchProblem):
    def is_goal(self, state):
        return len(state[1]) == 5   #5 personas del otro lado
    
    def actions(self, state):
        possible_actions = []
        people_left, people_right, flashlight_pos, battery = state

        if flashlight_pos == 0:
            couples = tuple(combinations(state[flashlight_pos],2))   #genera todas las combinaciones de personas del lado donde esté la linterna
            for couple in couples:
                if max(couple) <= state[3]:
                    possible_actions.append(couple)
        else: #flashlight_pos == 1
            for person in people_right:
                if person <= state[3]:
                    possible_actions.append((person,))

        return possible_actions

    def result(self, state, action):
        persons = action
        people_left, people_right, flashlight_pos, battery = state
        people_left = list(people_left)
        people_right = list(people_right)
        state = list(state)
        
        if len(persons) == 2:
            for person in persons:
                people_left.remove(person)
                people_right.append(person)
            flashlight_pos = 1
        else:
            people_right.remove(persons[0])
            people_left.append(persons[0])
            flashlight_pos = 0
        battery -= max(persons)

        state[0] = tuple(people_left)
        state[1] = tuple(people_right)
        state[2] = flashlight_pos
        state[3] = battery
        state = tuple(state)
        #print(state)
        return state

    def cost(self, state, action, state2):
        return max(action)

    def heuristic(self, state):
        personas_izq, personas_der, segundos_linterna, lado_linterna = state
        # Sin heurística:
        # return 0
        # {'max_fringe_size': 256, 'visited_nodes': 477, 'iterations': 477}

        # Heurística: la persona más rápida de la izquierda
        # {'max_fringe_size': 235, 'visited_nodes': 228, 'iterations': 228}
        # if personas_izq: #Si hay personas en la izq
        #     return min(personas_izq)
        # return 0

        # Heurística: la persona más rápida de la izquierda * cantidad de viajes estimados
        # {'max_fringe_size': 233, 'visited_nodes': 209, 'iterations': 209}
        if personas_izq:
            cantidad_viajes = ceil(len(personas_izq) / 2) # ceil redondea para arriba (5/2 = 3)
            persona_mas_veloz = min(personas_izq)
            return persona_mas_veloz * cantidad_viajes
        else:
            return 0
        

my_viewer = BaseViewer()
problem = BridgeProblem(INITIAL_STATE)
result = astar(problem, graph_search=True, viewer=my_viewer)

print("Goal node:", result)
print("Path from initial state to goal:")
for action, state in result.path():
    print("Action:", action)
    print("State:", state)
    
print("Stats:", my_viewer.stats)