from threading import activeCount
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

DEPOSIT = 1
ASSEMBLY = 2
MAX_SPEED = 20
DISTANCE = 60

INITIAL_STATE = (DEPOSIT, ((10,7,'Phase 1'),(15,3,'Phase 2'),(20,1,'Phase 3'),(5,0.5,'Sat 1'),(5,1.5,'Sat 2')),())
# bot position - 1 = deposit / 2 = assembly building
# 1st tuple: (list of parts pending to load)
# 2nd tuple: (list of parts delivered)


class RocketAssembly(SearchProblem):
    def is_goal(self, state):
        return len(state[2]) == 5
    
    def actions(self, state):
        possible_actions = []
        bot_pos, pending, delivered = state

        if bot_pos == DEPOSIT: # If the bot is in the deposit
            if len(state[DEPOSIT]) > 1:
                pairs = tuple(combinations(state[DEPOSIT],2))
                for pair in pairs:
                    part1, part2 = pair
                    if part1[1] + part2[1] <= 8: # If the combined weight is equal or less than 8 tons
                        speed = max(part1[0], part2[0])
                        possible_actions.append((speed, pair, ASSEMBLY)) # 2 is the destination (assembly building)
            else:
                part = state[DEPOSIT][0]
                speed = part[0]
                possible_actions.append((speed, part, ASSEMBLY))
        else:
            possible_actions.append((MAX_SPEED, None, DEPOSIT)) # 1 is the destination (deposit)
        
        return possible_actions

    def result(self, state, action):
        state = list(state)
        speed, parts, destination = action
        if parts != None:
            state[1] = list(state[1])
            state[2] = list(state[2])
            if len(parts) == 2:
                for part in parts:
                    state[1].remove(part)
                    state[2].append(part)
            else:
                state[1].remove(parts)
                state[2].append(parts)
            state[1] = tuple(state[1])
            state[2] = tuple(state[2])
        state[0] = destination
        state = tuple(state)
        return state

    def cost(self, state, action, state2):
        speed, _, _ = action
        return speed

    def heuristic(self, state):
        # Without heuristic
        # {'max_fringe_size': 18, 'visited_nodes': 49, 'iterations': 49}
        # return super().heuristic(state)

        # {'max_fringe_size': 18, 'visited_nodes': 46, 'iterations': 46}
        return len(state[1])/2

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
    problem = RocketAssembly(INITIAL_STATE)
    result = search_algorithm(problem, graph_search = True, viewer = visor)
    # result = astar(problem, graph_search = True, viewer = visor)
    print ('Final State:', result.state)
    print('=' * 50)
    print(' - Statistics:')
    print(' - Amount of actions until goal:', len(result.path()))
    print(' - Raw data:', visor.stats)
    
    for action, state in result.path():
        print("   - Action:", action)
        print("   - Resulting State:", state)
    