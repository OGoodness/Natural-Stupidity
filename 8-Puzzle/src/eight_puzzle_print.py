# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly

from Board import Board
from State import State
import time
from copy import copy, deepcopy

current = None
depth = 0
tiles = 8
openStates = []
closedStates = []
default_init = [[2, 3, 6], [1, 0, 8], [7, 5, 4]]
default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


class EightPuzzlePrint:
    initial = State(default_init)
    goal = State(default_goal)
    tiles = 8

    def __init__(self, init=default_init, goal_set=default_goal, tile=tiles):
        global current
        super()
        self.initial = State(init)
        self.goal = State(goal_set)
        self.tiles = tile
        current = self.initial

        # Try code thread thing

    def run(self):
        print("Start State: \n")
        path = 0
        current.print()

        openStates.append([current])
        while current != self.goal:
            state_walk()
            print()
            path += 1
            current.print()
            time.sleep(10)

        print("It took path" + str(path) + " Iterations")
        print("The length of the path is: " + str(current.getDepth()))


def swapPositions(original_tile_seq, row_a, col_a, row_b, col_b):
    tile_seq = deepcopy(original_tile_seq)
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_b], tile_seq[row_a][col_a]
    return tile_seq


def compare(a1, a2):
    if a1.getWeight() > a2.getWeight():
        return 1
    elif a1.getWeight() == a2.getWeight():
        if a1.getDepth() > a2.getDepth():
            return 1
        else:
            return 0
    else:
        return -1


def heuristic_test():
    # heuristic_test
    print()


def evaluate_child(flag, child):
    if flag[0] == 1:
        heuristic_test(child)
        openStates.append(child)
    if flag[0] == 2:
        state = openStates[flag[1]]
        past_path = state.getDepth()
        state.setDepth(child.getDepth())
        state.setWeight(state.getWeight() - (past_path - state.getDepth()))
    if flag[0] == 3:
        closedStates.remove(child)
        openStates.append(child)


# check if the generated state is in open or closed
# the purpose is to avoid a circle
def check_inclusive(state):
    in_open = 0
    in_closed = 0
    ret = [-1, -1]

    index_open = 0
    for open_state in openStates:
        if open_state == state:
            in_open = 1
            ret[1] = index_open
            index_open += 1
            break

    index_closed = 0
    for closed_state in closedStates:
        if closed_state == state:
            in_closed = 1
            ret[1] = index_closed
            index_closed += 1
            break

    if in_open == 0 and in_closed == 0:
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        ret[0] = 3
    return ret


def state_walk():
    global current
    closedStates.append(current)
    openStates.remove(current)
    walk_state = current.getBoard().getTile_seq()[:]
    moves = {}

    row = current.getBoard().getRow()
    col = current.getBoard().getColumn()
    current.print()

    # TODO I can't seem to find where this is created in the normal code, it shouldbe +=
    depth = 1
    # TODO FIX THE PYTHON LIST POINTING TO SAME OBJECT
    # Item Moving Up
    if row - 1 >= 0:
        print("UP")
        temp = swapPositions(walk_state, row, col, row - 1, col)
        print(temp)
        moves.update({"up": State(temp)})
        flag = check_inclusive(walk_state)
        evaluate_child(flag)

    # Item Moving Down
    if row + 1 < len(walk_state):
        print("down")
        temp = swapPositions(walk_state, row, col, row + 1, col)
        moves.update({"down": State(temp)})
        evaluate_child(flag)

    # Item Moving Left
    if col - 1 >= 0:
        print("left")
        temp = swapPositions(walk_state, row, col, row, col - 1)
        moves.update({"left": State(temp)})
        evaluate_child(flag)

    # Item Moving Right
    if col + 1 < len(walk_state[0]):
        print("Right")
        temp = swapPositions(walk_state, row, col, row, col + 1)
        moves.update({"right": State(temp)})
        evaluate_child(flag)

    current.setChildren(moves)
    # openStates.sort(compare)
    current = openStates[0]


# TODO Add heuristic test

epp = EightPuzzlePrint()
epp.run()
