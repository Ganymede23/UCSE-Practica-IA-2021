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

GRID = [(r,c) for r in range(7) for c in range(6)]
ROADS = []
RACKS = [(0,0),(1,0),(2,0),(4,0),(5,0),(6,0),(0,2),(1,2),(2,2),(4,2),(5,2),(6,2),(0,4),(1,4),(2,4),(4,4),(5,4),(6,4)]
IO = [(3,5)]
for cell in GRID:
    if cell not in RACKS:
        ROADS.append(cell)

MOVEMENTS = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0)
]

INITIAL_STATE = ((3,5), (), (('C1', (0, 1)), ('C2', (1, 1)), ('C3', (2, 5)), ('C4', (5,3)), ('C5', (0,3))))
# pos robot, list of loaded boxes, list of pending boxes

class AmagonProblem(SearchProblem):
    def is_goal(self, state):
        _, loaded_boxes, pending_boxes = state
        return len(loaded_boxes) + len(pending_boxes) == 0
    
    def actions(self, state):
        possible_actions = []
        deposit_coordinates = []
        bot_pos, loaded_boxes, pending_boxes = state
        bot_row, bot_col = bot_pos
        if len(loaded_boxes) > 0:
            for loaded_box in loaded_boxes:
                deposit_coordinates = []
                deposit_coordinates.append(loaded_box[1])            
        if bot_pos == (3,5) and len(loaded_boxes) < 2 and len(pending_boxes) > 0:
            # If bot is in I/O, has space to load at least 1 and there is at least 1 box to load
            boxes_to_load = []
            if len(loaded_boxes) == 1:          # If there is space for only one
                boxes_to_load.append(pending_boxes[0])
            else: #len(loaded_boxes) == 2       # If there is space for two
                if len(pending_boxes) == 1:     # If there is one to load
                    boxes_to_load.append(pending_boxes[0])
                else:                           # If there are two or more to load
                    boxes_to_load.append(pending_boxes[0])
                    boxes_to_load.append(pending_boxes[1])
            possible_actions.append(('Load', boxes_to_load))
        elif bot_pos in deposit_coordinates:
            possible_actions.append(('Unload', bot_pos))
        else:
            for move in MOVEMENTS:
                move_row, move_col = move
                new_row = bot_row + move_row
                new_col = bot_col + move_col
                new_pos = tuple((new_row, new_col))

                if (0 <= new_row <= 6) and (0 <= new_col <= 5):
                    possible_actions.append(('Move', new_pos))


        return possible_actions

    def result(self, state, action):
        action_type, data = action
        bot_pos, loaded_boxes, pending_boxes = state
        state = list(state)
        if action_type == 'Move':
            bot_pos = list(bot_pos)
            bot_pos = data
            bot_pos = tuple(bot_pos)
            state[0] = bot_pos
        elif action_type == 'Unload':
            loaded_boxes = list(loaded_boxes)
            for loaded_box in loaded_boxes:
                if loaded_box[1] == bot_pos:
                    loaded_boxes.remove(loaded_box)
            loaded_boxes = tuple(loaded_boxes)
            state[1] = loaded_boxes
        else:
            loaded_boxes = list(loaded_boxes)
            pending_boxes = list(pending_boxes)
            if len(data) == 1: #Just one box to load
                pending_boxes.remove(data[0])
                loaded_boxes.append(data[0]) 
            else:
                for box in data:
                    pending_boxes.remove(box)
                    loaded_boxes.append(box) 
            loaded_boxes = tuple(loaded_boxes)
            pending_boxes = tuple(pending_boxes)
            state[1] = loaded_boxes
            state[2] = pending_boxes
        state = tuple(state)

        return state

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        # Without heuristic
        # {'max_fringe_size': 39, 'visited_nodes': 635, 'iterations': 635}
        # return super().heuristic(state)

        # {'max_fringe_size': 42, 'visited_nodes': 578, 'iterations': 578}
        return len(state[1]) + len(state[2])



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
    problem = AmagonProblem(INITIAL_STATE)
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