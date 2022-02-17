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

ZOMBIES = ((1,0), (1,1), (1,2), (1,3), (2,3))
OBSTACLES = {(0,1), (0,2), (1,4), (2,1), (3,1), (3,3), (4,3)}
SAFE_HOUSE = (4,4)
SPAWN_POINT = (0,0)
AMMO = 3
HP = 100

MOVEMENTS = {
    (1,0), (-1,0), (0,1), (0,-1)
}

INITIAL_STATE = (SPAWN_POINT, HP, AMMO, ZOMBIES)

class ZombieSurvivalGame(SearchProblem):
    def is_goal(self, state):
        human, hp, ammo, zombies = state
        return human == SAFE_HOUSE and hp > 0
    
    def actions(self, state):
        possible_actions = []
        human, hp, ammo, zombies = state
        human_row, human_col = human
        for move in MOVEMENTS:
            move_row, move_col = move
            new_row = human_row + move_row
            new_col = human_col + move_col
            new_pos = (new_row, new_col)
            if (0 <= new_row <= 4) and (0 <= new_col <= 4) and new_pos not in OBSTACLES:
                if new_pos in zombies: 
                    if ammo > 0:
                        possible_actions.append(('shoot', new_pos, hp))
                    else:
                        if hp > 30:
                            possible_actions.append(('fight', new_pos, hp - 30))
                else:
                    possible_actions.append(('move', new_pos, hp))

        return possible_actions

    def result(self, state, action):
        # human, hp, ammo, zombies = state
        _, _, _, zombies = state
        action_type, new_pos, hp = action 

        state = list(state)

        if action_type == 'shoot':
            state[0] = new_pos
            state[2] -= 1
            zombies = list(zombies)
            zombies.remove(new_pos)
        elif action_type == 'fight':
            state[0] = new_pos
            state[1] = hp
        elif action_type == 'move':
            state[0] = new_pos
        
        state = tuple(state)
        return state

    def cost(self, state, action, state2):
        action_type, _, _ = action
        if action_type == 'shoot':
            return 20
        elif action_type == 'fight':
            return 10
        elif action_type == 'move':
            return 5

    def heuristic(self, state):
        # Without heuristic
        # {'max_fringe_size': 17, 'visited_nodes': 62, 'iterations': 62}
        # return super().heuristic(state)

        # Heuristic: Manhattan
        # {'max_fringe_size': 16, 'visited_nodes': 56, 'iterations': 56}
        human, _, _, _ = state
        human_row, human_col = human
        safe_row, safe_col = SAFE_HOUSE
        return abs(human_row - safe_row) + abs(human_col - safe_col)

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
    problem = ZombieSurvivalGame(INITIAL_STATE)
    result = search_algorithm(problem, graph_search = True, viewer = visor)
    #result = astar(problem, graph_search = True, viewer = visor)
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