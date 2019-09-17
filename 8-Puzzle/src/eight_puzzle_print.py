# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly
from functools import cmp_to_key

from State import State
import time
from copy import deepcopy

#Default initial state
default_init = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
#Default goal state
default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#Number of blocks in Eight Puzzle
tiles = 8


class EightPuzzlePrint:
    current = None
    initial = None
    goal = None
    tiles = 0

    def __init__(self, init=default_init, goal=default_goal, tile=tiles):
        super()
        self.initial = State(init)
        self.goal = State(goal)
        self.tiles = tile
        self.current = State(init)


    def run(self):
        print("Start State: \n")
        self.initial.print()

        print("Goal State: \n")
        self.goal.print()

        time_stamp_breadth_start = time.time()*1000.0
        breadth_search_start(self)
        time_stamp_breadth_end = time.time()*1000.0
        print("The total time for breadth first search in (millisecond) is: " + str(time_stamp_breadth_end-time_stamp_breadth_start) + "\n\n")

        time_stamp_heuristic_start = time.time()*1000.0
        heuristic_search_start(self)
        time_stamp_heuristic_end = time.time()*1000.0
        print("The total time for heuristic first search in (milisecond) is: " + str(time_stamp_heuristic_end-time_stamp_heuristic_start))


def breadth_search_start(self):
    depth = -1
    current = self.current
    goal = self.goal
    closed_states = []
    open_states = [current]

    while current != goal:
        next_row = []
        depth += 1
        for i, state in enumerate(open_states):
            closed_states.insert(0, state)
            board = state.get_board().get_tile_seq()[:]

            if state == goal:
                current = state
                break

            row = state.get_board().get_row()
            col = state.get_board().get_column()

            # Item Moving Up
            if row - 1 >= 0:
                temp = State(swap_positions(board, row, col, row - 1, col))
                temp.set_depth(current.get_depth() + 1)
                temp.set_parent(state)
                next_row.append(temp)

            # Item Moving Down
            if row + 1 < len(board):
                temp = State(swap_positions(board, row, col, row + 1, col))
                temp.set_depth(current.get_depth() + 1)
                temp.set_parent(state)
                next_row.append(temp)

            # Item Moving Left
            if col - 1 >= 0:
                temp = State(swap_positions(board, row, col, row, col - 1))
                temp.set_depth(current.get_depth() + 1)
                temp.set_parent(state)
                next_row.append(temp)

            # Item Moving Right
            if col + 1 < len(board[0]):
                temp = State(swap_positions(board, row, col, row, col + 1))
                temp.set_depth(current.get_depth() + 1)
                temp.set_parent(state)
                next_row.append(temp)
        next_row = [x for x in next_row if x not in closed_states]
        open_states = next_row[:]

    print("It took " + str(len(closed_states)) + " Iterations")
    print("The length of the path is: " + str(depth))


def heuristic_search_start(self):
    open_states = []
    closed_states = []
    path = 0
    current = self.current
    goal = self.goal

    open_states.append(current)
    while current != goal:
        state_walk(open_states, closed_states, current)
        path += 1
        if len(open_states) % 500 == 0:
            print(len(open_states))
            print(str(len(closed_states)) + "\n")
        if len(closed_states) % 500 == 0:
            print(len(open_states))
            print(str(len(closed_states)) + "\n")
        current = open_states[0]
    current.print()
    print("It took path " + str(path) + " Iterations")
    print("The length of the path is: " + str(current.get_depth()))




# Gets heuristic value for heuristic search
def heuristic_test(state):

    #Gets parameter state board and goal_board
    current_board = state.get_board().get_tile_seq()
    goal_board = default_goal

    # h(1) Counts tiles that are out of place
    h1 = 0

    # Iterates through current_board
    for x in range(0, len(current_board)):
        for y in range(0, len(current_board)):
            # If current_board is not in goal_board location add h1
            if current_board[x][y] != goal_board[x][y]:
                h1 = h1 + 1

    # / (2) Sum of tile distances out of place
    diff = 0
    # Iterates through goal_board
    for i in range(0, len(goal_board)):
        for j in range(0, len(goal_board)):
            #Sets goal_board location values
            gcol = i
            grow = j
            # Iterates through current_board
            for x in range(0, len(current_board)):
                for y in range(0, len(current_board)):
                    # If current_board value equals goal_board value set current location values
                    if current_board[x][y] == goal_board[i][j]:
                        ccol = y
                        crow = x

        # Calculating difference between current_board and goal_board locations
        cdiff = ccol - gcol
        rdiff = crow - grow

        diff = diff + abs(cdiff) + abs(rdiff)
    h2 = diff

    #    // (3) Finds direct reversal value in current board state
    reversals = 0
    # Iterate through current_board
    for y in range(0, len(current_board)):
        for x in range(0, len(current_board)):
            # If reaches right end of board and is NOT on the bottom of the board
            if x == 2 and y != 2:
                # If current_board value belongs in the tile below
                if current_board[x][y] == default_goal[x][y + 1] and current_board[x][y] != 0:
                    # If the value below belongs in the tile above increments reversal
                    if current_board[x][y + 1] == default_goal[x][y]:
                        reversals = reversals + 1
            # If on the bottom of the board, but not on the right side yet
            elif y == 2 and x != 2:
                # current_board value checking to see if it belongs to the right tile
                if current_board[x][y] == default_goal[x + 1][y] and current_board[x][y] != 0:
                    # If belongs to the right tile checks if the right tiles belongs where current_board value is located
                    if current_board[x + 1][y] == default_goal[x][y]:
                        reversals = reversals + 1
            # If not on a border of the board
            elif y != 2 and x != 2:
                # Checks tile to the right if it belongs there
                if current_board[x][y] == default_goal[x + 1][y] and current_board[x][y] != 0:
                    # If it does it checks if tile to the right belongs where current tile is
                    if current_board[x + 1][y] == default_goal[x][y]:
                        reversals = reversals + 1
                # Checks tile below if it belongs there
                if current_board[x][y] == default_goal[x][y + 1] and current_board[x][y] != 0:
                    # If it does it checks if tile below belongs where current tile is
                    if current_board[x][y + 1] == default_goal[x][y]:
                        reversals = reversals + 1

    h3 = reversals * 2

    # Returns calculated heuristic values
    state.set_weight(state.get_depth() + h1 + h2 + h3)


# check if the generated state is in open or closed
# the purpose is to avoid a circle
def check_inclusive(state, open_states, closed_states):
    in_open = 0
    in_closed = 0
    # ret[0] is a flag, ret[1] is the index of the value that needs to be changed
    ret = [-1, -1]

    # Determines if a value in open states needs to be changed
    index_open = 0
    for open_state in open_states:
        if open_state == state:
            in_open = 1
            ret[1] = index_open
            break
        index_open += 1

    # Determines if a value in closed needs to be changed
    index_closed = 0
    for closed_state in closed_states:
        if closed_state == state:
            in_closed = 1
            ret[1] = index_closed
            break
        index_closed += 1

    # Sets the flag
    if in_open == 0 and in_closed == 0:
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        ret[0] = 3
    return ret


def state_walk(open_states, closed_states, current):
    closed_states.append(current)
    open_states.remove(current)

    # Sets walk state to the current board til seq
    walk_state = current.get_board().get_tile_seq()[:]

    # Gets the location of the 0 tile
    row = current.get_board().get_row()
    col = current.get_board().get_column()

    # Item Moving Up
    if row - 1 >= 0:
        # print("up")
        temp = State(swap_positions(walk_state, row, col, row - 1, col))
        temp.set_depth(current.get_depth() + 1)
        flag = check_inclusive(temp, open_states, closed_states)
        evaluate_child(flag, temp, open_states, closed_states)

    # Item Moving Down
    if row + 1 < len(walk_state):
        # print("down")
        temp = State(swap_positions(walk_state, row, col, row + 1, col))
        temp.set_depth(current.get_depth() + 1)
        flag = check_inclusive(temp, open_states, closed_states)
        evaluate_child(flag, temp, open_states, closed_states)

    # Item Moving Left
    if col - 1 >= 0:
        # print("left")
        temp = State(swap_positions(walk_state, row, col, row, col - 1))
        temp.set_depth(current.get_depth() + 1)
        flag = check_inclusive(temp, open_states, closed_states)
        evaluate_child(flag, temp, open_states, closed_states)

    # Item Moving Right
    if col + 1 < len(walk_state[0]):
        # print("Right")
        temp = State(swap_positions(walk_state, row, col, row, col + 1))
        temp.set_depth(current.get_depth() + 1)
        flag = check_inclusive(temp, open_states, closed_states)
        evaluate_child(flag, temp, open_states, closed_states)

    # Sorts the open states and iterates to the current value
    open_states.sort(key=cmp_to_key(compare))



def evaluate_child(flag, child, open_states, closed_states):
    if flag[0] == 1:
        heuristic_test(child)
        open_states.append(child)

    # If the value is an open state and the path is better the state value will be updated.
    if flag[0] == 2:
        state = open_states[flag[1]]
        if child.depth < state.depth:
            past_path = state.get_depth()
            state.set_depth(child.get_depth())
            state.set_weight(state.get_weight() - (past_path - state.get_depth()))

    # If the value is a closed state and the path is better it remove the value from the closed state and adds the better state to open
    if flag[0] == 3:
        state = closed_states[flag[1]]
        if child.depth < state.depth:
            closed_states.remove(state)
            open_states.append(child)



def swap_positions(original_tile_seq, row_a, col_a, row_b, col_b):
    tile_seq = deepcopy(original_tile_seq)
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_b], tile_seq[row_a][col_a]
    return tile_seq



def compare(a1, a2):
    if a1.get_weight() > a2.get_weight():
        return 1
    elif a1.get_weight() == a2.get_weight():
        if a1.get_depth() > a2.get_depth():
            return 1
        elif a1.get_depth() < a2.get_depth():
            return -1
        else:
            return 0
    else:
        return -1



test_boards = []
# # 7 moves
# test_boards.append([[1, 0, 5], [4, 3, 2], [7, 8, 6]])
# # 5 moves
# test_boards.append([[1, 5, 2], [4, 8, 3], [7, 0, 6]])
#
# # 10 moves
# test_boards.append([[1, 6, 0], [5, 3, 2], [4, 7, 8]])
#
# # 9 moves
# test_boards.append([[1, 6, 2], [4, 3, 8], [7, 0, 5]])
test_boards.append([[2, 3, 1], [0, 4, 6], [7, 5, 8]])
test_boards.append(([[2, 3, 6], [1, 4, 8], [7, 5, 0]]))

#Goal
goal_boards = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


for i, board in enumerate(test_boards):
    epp = EightPuzzlePrint(board, goal_boards, 8)
    epp.run()
    print("\n ============================= \n")
