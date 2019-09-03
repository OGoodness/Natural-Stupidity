# TODO: Optimize code, it's a little messy
# TODO: Current varioable needs to be set initially, need to implement sorting, need to print out properly

from Board import Board
from State import State

current = None
goal = None
tiles = 8
openStates = []
closedState = []


class EightPuzzlePrint:
    default_init = Board([[2, 3, 6], [1, 4, 8], [7, 5, 0]], 3, 3)
    default_goal = Board([[1, 2, 3], [4, 5, 6], [7, 8, 0]], 3, 3)
    initial = State(default_init)
    goalA = State(default_goal)
    tiles = 8

    def __init__(self, init = default_init, goal = default_goal, tile = tiles):
        super()
        self.initial = init
        self.goalA = goal
        self.tiles = tile

    def start(self):

        init_board = Board([[2, 3, 6], [1, 4, 8], [7, 5, 0]], 3, 3)
        init = State(init_board, 0, 0)

        goal_board = Board([[1, 2, 3], [4, 5, 6], [7, 8, 0]], 3, 3)
        goal = State(goal_board, 0, 0)

        initial = init
        goalA = goal


        tiles = 8

        # Try code thread thing


    def run(self):
        print("Start State: \n")
        path = 0
        while current != goal:
            state_walk()
            print()
            path += 1
        print("It took path"+ str(path) +" Iterations")
        print("The length of the path is: " + str(current.getDepth()))

        test = goal.getBoard().getTile_seq()

        for i in len(test):
            for j in len(test[i]):
                print(test[i][j]+" ")
            print("\n")
        print("Goal State")


epp = EightPuzzlePrint()
epp.start()
epp.run()

def __eq__(self, other):
    return self.getBoard().getTile_seq() == other.getBoard().getTile_seq()
def __eq__(self, other):
    return self.getBoard().getTile_seq() != other.getBoard().getTile_seq()

def swapPositions(state, row_a, col_a, row_b, col_b):
    tile_seq = state.getTile_seq()
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_a], tile_seq[row_a][col_b]
    state.setTile_seq(tile_seq)
    state.setRow(row_b)
    state.setColumn(col_a)


#check if the generated state is in open or closed
#the purpose is to avoid a circle
def check_inclusive(s):
    in_open = 0
    in_closed = 0
    ret = [-1, -1]

    for i in openStates:
        temp = i
        # TODO: Need .Equals()
        if temp == s:
            in_open = 1
            ret[1] = i
            break

    for x in closedState:
        temp = x
        # TODO: Need .Equals()
        if temp == s:
            in_closed = 1
            ret[1] = x
            break

    if in_open == 0 and in_closed == 0:
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        ret[0] = 3
    print(ret)
    return ret


def state_walk():
    closedState.add(current)
    openStates.remove(current)
    walk_state = current.getTile_seq()

    row = walk_state.getRow()
    col = walk_state.getRow()


    # TODO I can't seem to find where this is created in the normal code, it shouldbe +=
    depth = 1

    #Item Moving Down
    if row - 1 >= 0:
        swapPositions(walk_state, row, col, row-1, col)
        check = check_inclusive(walk_state)
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 2:

            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 3:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")



    #Item Moving Up
    if row + 1 < len(walk_state):
        swapPositions(walk_state, row, col, row+1, col)
        check = check_inclusive(walk_state)
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 2:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 3:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")



    #Item Moving Right
    if col + 1 < walk_state:
        swapPositions(walk_state, row, col, row, col+1)
        check = check_inclusive(walk_state)
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 2:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 3:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")


        # Item Moving Left
    if col - 1 < walk_state:
        swapPositions(walk_state, row, col, row, col-1)
        check = check_inclusive(walk_state)
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 2:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 3:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")



    openStates.sort(compare)
    current = openStates[0]

#TODO Add heuristic test


def compare(a1, a2):
    if ai.getWeight() > a2.getWeight():
        return  1
    elif a1.getWeight() == a2.getWeight():
        if a1.getDepth() > a2.getDepth():
            return 1
        else:
            return 0
    else:
        return  -1

