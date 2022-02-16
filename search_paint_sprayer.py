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

WALL = [(r,c) for r in range(5) for c in range(5)]
WALL = tuple(WALL)
INITIAL_STATE = (WALL)

class PaintGunProblem(SearchProblem):
    def is_goal(self, state):
        return len(state) == 0
    
    def actions(self, state):
        possible_actions = []
        for tile in state:
            tile_row, tile_col = tile
            tiles_list = []
            tiles_to_paint = []
            tiles_list = [(tile_row - 1, tile_col), (tile_row + 1, tile_col), (tile_row, tile_col - 1), (tile_row, tile_col + 1)]
            for adjacent_tile in tiles_list:
                if adjacent_tile in state:
                    tiles_to_paint.append(adjacent_tile)
            tiles_to_paint.append(tile)
            possible_actions.append(tiles_to_paint)

        return possible_actions

    def result(self, state, action):
        tiles_list = action
        state = list(state)

        for tile in tiles_list:
            state.remove(tile)

        state = tuple(state)
        #print(state)
        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Without heuristic
        # return super().heuristic(state)
        
        return len(WALL)/5


METHODS = (
    #breadth_first,
    #depth_first,
    uniform_cost,
    greedy,
    astar
)    
        
for search_algorithm in METHODS:
    print()
    print('=' * 50)
    print("Running:", search_algorithm)
    visor = BaseViewer()
    problem = PaintGunProblem(INITIAL_STATE)
    result = search_algorithm(problem, graph_search = True, viewer = visor)
    #result = astar(problem, graph_search = True, viewer = visor)
    print ('Final State:', result.state)
    print('=' * 50)
    print(' - Statistics:')
    print(' - Amount of actions until goal:', len(result.path()))
    print(' - Raw data:', visor.stats)
    
    for action, state in result.path():
        print("   - Action:", action)
        print("   - Resulting State:", state)
