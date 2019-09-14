# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly
from functools import cmp_to_key

from Board import Board
from State import State
import time
from copy import copy, deepcopy

default_init = [[2, 3, 6], [1, 4, 8], [7, 5, 0]]
# default_init = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
# default_init = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
# default_init = [[2, 1, 3], [5, 4, 0], [7, 8, 6]]
default_goal = [[1, 2, 3], [5, 8, 6], [0, 7, 4]]
current = State([[2, 3, 6], [1, 0, 8], [7, 5, 4]])
depth = 0
tiles = 8
openStates = []
closedStates = []


class EightPuzzlePrint:
    initial = State(default_init)
    goal = State(default_goal)
    tiles = 8

    def __init__(self, init=default_init, goal=default_goal, tile=tiles):
        global current
        super()
        self.initial = State(init)
        self.goal = State(goal)
        self.tiles = tile
        current = self.initial

        # Try code thread thing

    def run(self):
        global current
        print("Start State: \n")
        path = 0
        current_holder = current
        current.print()

        print("Goal State: \n")
        self.goal.print()

        breadth_search(current, self.goal, 0)

        openStates.clear()
        closedStates.clear()

        current = current_holder
        openStates.append(current)
        while current != self.goal:
            state_walk()
            # print()
            path += 1
            # current.print()
            if len(openStates) % 500 == 0:
                print(len(openStates))
                print(str(len(closedStates)) + "\n")
            if len(closedStates) % 500 == 0:
                print(len(openStates))
                print(str(len(closedStates)) + "\n")

        print(current.print())
        print("It took path " + str(path) + " Iterations")
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
        openStates = nextRow[:]
        depth += 1
    current.printPath()

# Gets heuristic value for heuristic search
def heuristic_test(state):

    #Gets parameter state board and goalboard
    currentboard = state.getBoard().getTile_seq()
    goalboard = default_goal

    # h(1) Counts tiles that are out of place
    h1 = 0

    # Iterates through currentboard
    for x in range(0, len(currentboard)):
        for y in range(0, len(currentboard)):
            # If currentboard is not in goalboard location add h1
            if currentboard[x][y] != goalboard[x][y]:
                h1 = h1 + 1

    # / (2) Sum of tile distances out of place
    diff = 0
    # Iterates through goalboard
    for i in range(0, len(goalboard)):
        for j in range(0, len(goalboard)):
            #Sets goalboard location values
            gcol = i
            grow = j
            # Iterates through currentboard
            for x in range(0, len(currentboard)):
                for y in range(0, len(currentboard)):
                    # If currentboard value equals goalboard value set current location values
                    if currentboard[x][y] == goalboard[i][j]:
                        ccol = y
                        crow = x

        # Calculating difference between currentboard and goalboard locations
        cdiff = ccol - gcol
        rdiff = crow - grow

        diff = diff + abs(cdiff) + abs(rdiff)
    h2 = diff

    #    // (3) Finds direct reversal value in current board state
    reversals = 0
    # Iterate through currentboard
    for y in range(0, len(currentboard)):
        for x in range(0, len(currentboard)):
            # If reaches right end of board and is NOT on the bottom of the board
            if x == 2 and y != 2:
                # If currentboard value belongs in the tile below
                if currentboard[x][y] == default_goal[x][y + 1] and currentboard[x][y] != 0:
                    # If the value below belongs in the tile above increments reversal
                    if currentboard[x][y + 1] == default_goal[x][y]:
                        reversals = reversals + 1
            # If on the bottom of the board, but not on the right side yet
            elif y == 2 and x != 2:
                # currentboard value checking to see if it belongs to the right tile
                if currentboard[x][y] == default_goal[x + 1][y] and currentboard[x][y] != 0:
                    # If belongs to the right tile, checks if the right tiles belongs where currentboard value is located
                    if currentboard[x + 1][y] == default_goal[x][y]:
                        reversals = reversals + 1
            # If not on a border of the board
            elif y != 2 and x != 2:
                # Checks tile to the right if it belongs there
                if currentboard[x][y] == default_goal[x + 1][y] and currentboard[x][y] != 0:
                    #If it does it checks if tile to the right belongs where current tile is
                    if currentboard[x + 1][y] == default_goal[x][y]:
                        reversals = reversals + 1
                #Checks tile below if it belongs there
                if currentboard[x][y] == default_goal[x][y + 1] and currentboard[x][y] != 0:
                    #If it does it checks if tile below belongs where current tile is
                    if currentboard[x][y + 1] == default_goal[x][y]:
                        reversals = reversals + 1

    h3 = reversals * 2

    # Returns calculated heuristic values
    state.setWeight(state.getDepth() + h1 + h2 + h3)


# This file will determine if the child needs to be added to open,
def evaluate_child(flag, child):
    # Gets the heuristic value for child and adds it to open state.
    if flag[0] == 1:
        heuristic_test(child)
        openStates.append(child)

    # If the value is an open state and the path is better the state value will be updated.
    if flag[0] == 2:
        state = openStates[flag[1]]
        if child.depth < state.depth:
            past_path = state.getDepth()
            state.setDepth(child.getDepth())
            state.setWeight(state.getWeight() - (past_path - state.getDepth()))

    # If the value is a closed state and the path is better it remove the value from the closed state and adds the better state to open
    if flag[0] == 3:
        state = closedStates[flag[1]]
        if child.depth < state.depth:
            closedStates.remove(state)
            openStates.append(child)


# check if the generated state is in open or closed
# the purpose is to avoid a circle
def check_inclusive(state):
    in_open = 0
    in_closed = 0
    # ret[0] is a flag, ret[1] is the index of the value that needs to be changed
    ret = [-1, -1]

    # Determines if a value in open states needs to be changed
    index_open = 0
    for open_state in openStates:
        if open_state == state:
            in_open = 1
            ret[1] = index_open
            break
        index_open += 1

    # Determines if a value in closed needs to be changed
    index_closed = 0
    for closed_state in closedStates:
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


# Performs the heuristic test
def state_walk():
    global current
    closedStates.append(current)
    openStates.remove(current)

    # Sets walk state to the current board til seq
    walk_state = current.getBoard().getTile_seq()[:]

    # Gets the location of the 0 tile
    row = current.getBoard().getRow()
    col = current.getBoard().getColumn()

    # Item Moving Up
    if row - 1 >= 0:
        # print("up")
        temp = State(swapPositions(walk_state, row, col, row - 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Down
    if row + 1 < len(walk_state):
        # print("down")
        temp = State(swapPositions(walk_state, row, col, row + 1, col))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Left
    if col - 1 >= 0:
        # print("left")
        temp = State(swapPositions(walk_state, row, col, row, col - 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Item Moving Right
    if col + 1 < len(walk_state[0]):
        # print("Right")
        temp = State(swapPositions(walk_state, row, col, row, col + 1))
        temp.setDepth(current.getDepth() + 1)
        flag = check_inclusive(temp)
        evaluate_child(flag, temp)

    # Sorts the open states and iterates to the current value
    openStates.sort(key=cmp_to_key(compare))
    current = openStates[0]


epp = EightPuzzlePrint()
epp.run()
