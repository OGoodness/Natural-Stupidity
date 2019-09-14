# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly
from functools import cmp_to_key

from State import State
import time
from copy import deepcopy

#Default initial state
default_init = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
#Default goal state
default_goal = [[1, 2, 3], [5, 8, 6], [0, 7, 4]]

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

        # Try code thread thing

    def run(self):
        print("Start State: \n")
        self.initial.print()

        print("Goal State: \n")
        self.goal.print()

        timeStampBreadthStart = time.time()*1000.0
        breadth_search_start(self)
        timeStampBreadthEnd = time.time()*1000.0
        print("The total time for breadth first search is: " + str(timeStampBreadthEnd-timeStampBreadthStart))

        timeStampHeuristicStart = time.time()*1000.0
        #heuristic_search_start(self)
        timeStampHeuristicEnd = time.time()*1000.0
        print("The total time for heuristic first search is: " + str(timeStampHeuristicEnd-timeStampHeuristicStart))




def heuristic_search_start(self):
    openStates = []
    closedStates = []
    path = 0
    current = self.current
    goal = self.goal

    openStates.append(current)
    while current != goal:
        state_walk(openStates, closedStates, current)
        # print()
        path += 1
        # current.print()
        if len(openStates) % 500 == 0:
            print(len(openStates))
            print(str(len(closedStates)) + "\n")
        if len(closedStates) % 500 == 0:
            print(len(openStates))
            print(str(len(closedStates)) + "\n")
        current = openStates[0]
    current.print()
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


def breadth_search_start(self):
    depth = 0
    current = self.current
    goal = self.goal
    closedStates = []
    openStates = [current]

    while current != goal:
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

    print("Depth: " + str(depth))
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

    # / (2) Sum of distances out of place
    # // TODO your code start here
    diff = 0
    for i in range(0, len(goalboard)):
        for j in range(0, len(goalboard)):
            gcol = i
            grow = j
            for x in range(0, len(currentboard)):
                for y in range(0, len(currentboard)):
                    if currentboard[x][y] == goalboard[i][j]:
                        ccol = y
                        crow = x


        cdiff = ccol - gcol
        rdiff = crow - grow

        diff = diff + abs(cdiff) + abs(rdiff)
    h2 = diff

    #    // (3) 2 x the number of direct tile reversals

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
    state.setWeight(state.getDepth() + h1 + h2 + h3)


def evaluate_child(flag, child, openStates, closedStates):
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
def check_inclusive(state, openStates, closedStates):
    in_open = 0
    in_closed = 0
    ret = [-1, -1]

    index_open = 0
    for open_state in openStates:
        if open_state == state:
            in_open = 1
            ret[1] = index_open
            break
        index_open += 1

    index_closed = 0
    for closed_state in closedStates:
        if closed_state == state:
            in_closed = 1
            ret[1] = index_closed
            break
        index_closed += 1

    if in_closed == 1 and in_open == 1:
        print("Why")
    if in_open == 0 and in_closed == 0:
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        ret[0] = 3
    return ret


def state_walk(openStates, closedStates, current):
    closedStates.append(current)
    openStates.remove(current)
    walk_state = current.getBoard().getTile_seq()[:]

    row = current.getBoard().getRow()
    col = current.getBoard().getColumn()

    # Item Moving Up
    if row - 1 >= 0:
        # print("up")
        temp = State(swapPositions(walk_state, row, col, row - 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp, openStates, closedStates)
        evaluate_child(flag, temp, openStates, closedStates)

    # Item Moving Down
    if row + 1 < len(walk_state):
        # print("down")
        temp = State(swapPositions(walk_state, row, col, row + 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp, openStates, closedStates)
        evaluate_child(flag, temp, openStates, closedStates)

    # Item Moving Left
    if col - 1 >= 0:
        # print("left")
        temp = State(swapPositions(walk_state, row, col, row, col - 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp, openStates, closedStates)
        evaluate_child(flag, temp, openStates, closedStates)

    # Item Moving Right
    if col + 1 < len(walk_state[0]):
        # print("Right")
        temp = State(swapPositions(walk_state, row, col, row, col + 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp, openStates, closedStates)
        evaluate_child(flag, temp, openStates, closedStates)

    openStates.sort(key=cmp_to_key(compare))
    #current = openStates[0]


# TODO Add heuristic test

epp = EightPuzzlePrint()
epp.run()
