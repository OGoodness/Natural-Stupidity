# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly

from Board import Board
from State import State

current = None
depth = 0
tiles = 8
openStates = []
closedState = []


class EightPuzzlePrint:
    default_init = [[2, 3, 6], [1, 4, 8], [7, 5, 0]]
    default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    initial = State(default_init)
    goal = State(default_goal)
    tiles = 8

    def __init__(self, init = default_init, goal_set = default_goal, tile = tiles):
        super()
        self.initial = State(init)
        self.goal = State(goal_set)
        self.tiles = tile

    def start(self):
        global current, goal
        current = self.initial
        tiles = 8

        # Try code thread thing


    def run(self):
        print("Start State: \n")
        path = 0
        while current != self.goal:
            state_walk()
            print()
            path += 1
            current.print()

        print("It took path"+ str(path) +" Iterations")
        print("The length of the path is: " + str(current.getDepth()))






def swapPositions(board, row_a, col_a, row_b, col_b):
    tile_seq = board.getTile_seq()
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_a], tile_seq[row_a][col_b]
    board.setTile_seq(tile_seq)
    board.setRow(row_b)
    board.setColumn(col_a)


def heuristic_test():
    # heuristic_test
    print("heuristic_test")

def open():
    # Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
    print("Compare path to duplicate state, if shorter then give state on open, the shorter path")

def close():
    # Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
    print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")

#check if the generated state is in open or closed
#the purpose is to avoid a circle
def check_inclusive(s):
    in_open = 0
    in_closed = 0
    ret = [-1, -1]

    for i in openStates:
        temp = i

        if temp == s:
            in_open = 1
            ret[1] = i
            break

    for x in closedState:
        temp = x

        if temp == s:
            in_closed = 1
            ret[1] = x
            break

    if in_open == 0 and in_closed == 0:
        heuristic_test()
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        open()
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        close()
        ret[0] = 3
    return ret


def state_walk():
    global current
    #closedState.append(current)
    #openStates.remove(current)
    walk_state = current.getBoard()

    row = walk_state.getRow()
    col = walk_state.getColumn()


    # TODO I can't seem to find where this is created in the normal code, it shouldbe +=
    depth = 1

    #Item Moving Down
    if row - 1 >= 0:
        swapPositions(walk_state, row, col, row-1, col)
        check = check_inclusive(walk_state)

    #Item Moving Up
    if row + 1 < len(walk_state.getTile_seq()):
        swapPositions(walk_state, row, col, row+1, col)
        check = check_inclusive(walk_state)

    #Item Moving Right
    if col + 1 < len(walk_state.getTile_seq()[0]):
        swapPositions(walk_state, row, col, row, col+1)
        check = check_inclusive(walk_state)

    # Item Moving Left
    if col - 1 >= 0:
        swapPositions(walk_state, row, col, row, col-1)
        check = check_inclusive(walk_state)

    #openStates.sort(compare)
    current = openStates[0]



#TODO Add heuristic test

epp = EightPuzzlePrint()
epp.start()
epp.run()

