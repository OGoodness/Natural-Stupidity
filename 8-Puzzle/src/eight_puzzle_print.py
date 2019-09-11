# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly
from functools import cmp_to_key

from Board import Board
from State import State
import time
from copy import copy, deepcopy

default_init = [[2, 3, 6], [1, 0, 8], [7, 5, 4]]
#default_init = [[5, 1, 3], [2, 6, 8], [0, 4, 7]]
default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
current = State([[2, 3, 6], [1, 0, 8], [7, 5, 4]])
depth = 0
tiles = 8
openStates = []
closedStates = []


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

        print("Goal State: \n")
        self.goal.print()

        breadth_search(current, self.goal, 0)

        # openStates.clear()
        # closedStates.clear()
        #
        # openStates.append(current)
        # while current != self.goal:
        #     state_walk()
        #     print()
        #     path += 1
        #     current.print()


        print("It took path " + str(path) + " Iterations")
        print("The length of the path is: " + str(current.getDepth()))


def swapPositions(original_tile_seq, row_a, col_a, row_b, col_b):
    tile_seq = deepcopy(original_tile_seq)
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_b], tile_seq[row_a][col_a]
    return tile_seq


def compare(a1=None, a2=None):
    if a1 is not None and a2 is not None:
        if a1.getWeight() > a2.getWeight():
            return 1
        elif a1.getWeight() == a2.getWeight():
            if a1.getDepth() > a2.getDepth():
                return 1
            elif a1.getDepth() < a2.getDepth():
                return -1
            else:
                return 0
        else:
            return -1

def breadth_search(current, goal, depth):
    closedStates = []
    openStates = [current]

    while current != goal:
        print("Depth: " + str(depth))
        nextRow = []
        for i, state in enumerate(openStates):
            closedStates.insert(0, state)
            board = state.getBoard().getTile_seq()[:]

            if state == goal:
                print("Matched")
                current = state
                break

            row = state.getBoard().getRow()
            col = state.getBoard().getColumn()

            # Item Moving Up
            if row - 1 >= 0:
                temp = State(swapPositions(board, row, col, row - 1, col))
                temp.setDepth(current.getDepth() + 1)
                temp.setParent(state)
                nextRow.append(temp)

            # Item Moving Down
            if row + 1 < len(board):
                temp = State(swapPositions(board, row, col, row + 1, col))
                temp.setDepth(current.getDepth() + 1)
                temp.setParent(state)
                nextRow.append(temp)

            # Item Moving Left
            if col - 1 >= 0:
                temp = State(swapPositions(board, row, col, row, col - 1))
                temp.setDepth(current.getDepth() + 1)
                temp.setParent(state)
                nextRow.append(temp)

            # Item Moving Right
            if col + 1 < len(board[0]):
                temp = State(swapPositions(board, row, col, row, col + 1))
                temp.setDepth(current.getDepth() + 1)
                temp.setParent(state)
                nextRow.append(temp)

        nextRow = [x for x in nextRow if x not in closedStates]
        openStates = nextRow[:]
        depth += 1
    current.printPath()


def heuristic_test(state):
    currentboard = state.getBoard().getTile_seq()
    goalboard = default_goal

    # h(1)
    h1 = 0

    for x in range(0, len(currentboard)):
        for y in range(0, len(currentboard)):
            if currentboard[x][y] != goalboard[x][y]:
                h1 = h1 + 1

    #/ (2) Sum of distances out of place
    #// TODO your code start here
    h2 = 0
    diff = 0
    for a in range(0, 9):
        for x in range(0, len(currentboard)):
            for y in range(0, len(currentboard)):
                if currentboard[x][y] == a:
                    ccol = y
                    crow = x
                if goalboard[x][y] == a:
                    gcol = y
                    grow = x

        cdiff = ccol - gcol
        rdiff = crow - grow

        diff = diff + abs(cdiff) + abs(rdiff)
    h2 = diff

#    // (3) 2 x the number of direct tile reversals

    h3 = 0
    cfound = 0
    gfound = 0
    cnewfound = 0
    gnewfound = 0
    reversals = 0
    for z in range(1, 9):
        for x in range(0, len(currentboard)):
            for y in range(0, len(currentboard)):
                if currentboard[x][y] == z:
                    ccol = y
                    crow = x
                    cfound = 1
                if goalboard[x][y] == z:
                    gcol = y
                    grow = x
                    gfound = 1

                if cfound == 1 and gfound == 1:
                    cfound = 0
                    gfound = 0
                    cdiff = ccol - gcol
                    rdiff = crow - grow
                    if abs(cdiff + rdiff) == 1:
                        findvalue = currentboard[grow][gcol]
                        for a in range(0, len(currentboard)):
                            for b in range(0, len(currentboard)):
                                if currentboard[a][b] == findvalue:
                                    cnewcol = b
                                    cnewrow = a
                                    cnewfound = 1
                                if goalboard[a][b] == findvalue:
                                    gnewcol = b
                                    gnewrow = a
                                    gnewfound = 1

                                if cnewfound == 1 and gnewfound == 1:
                                    cnewfound = 0
                                    gnewfound = 0
                                    cnewdiff = abs(cnewcol - gnewcol)
                                    rnewdiff = abs(cnewrow - gnewrow)
                                    if cnewdiff + rnewdiff == 1 and ccol == gnewcol and crow == gnewrow:
                                        reversals = reversals + 1

    h3 = reversals * 2

 #   // set the heuristic value for current state
    state.setWeight(state.getDepth()+h1+h2+h3)


def evaluate_child(flag, child):
    if flag[0] == 1:
        heuristic_test(child)
        openStates.append(child)
    if flag[0] == 2:
        state = openStates[flag[1]]
        if child.depth < state.depth:
            past_path = state.getDepth()
            state.setDepth(child.getDepth())
            state.setWeight(state.getWeight() - (past_path - state.getDepth()))
    if flag[0] == 3:
        state = closedStates[flag[1]]
        if child.depth < state.depth:
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


    depth = 1

    # Item Moving Up
    if row - 1 >= 0:
        print("up")
        temp = State(swapPositions(walk_state, row, col, row - 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Down
    if row + 1 < len(walk_state):
        print("down")
        temp = State(swapPositions(walk_state, row, col, row + 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Left
    if col - 1 >= 0:
        print("left")
        temp = State(swapPositions(walk_state, row, col, row, col - 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Right
    if col + 1 < len(walk_state[0]):
        print("Right")
        temp = State(swapPositions(walk_state, row, col, row, col + 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    openStates.sort(key=cmp_to_key(compare))
    current = openStates[0]


# TODO Add heuristic test

epp = EightPuzzlePrint()
epp.run()
