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
    default_init = Board([[2, 3, 6], [1, 4, 8], [7, 5, 0]], 2, 2)
    default_goal = Board([[1, 2, 3], [4, 5, 6], [7, 8, 0]], 2, 2)
    initial = State(default_init)
    goalA = State(default_goal)
    tiles = 8

    def __init__(self, init = default_init, goal = default_goal, tile = tiles):
        super()
        self.initial = init
        self.goalA = goal
        self.tiles = tile

    def start(self):
        global current, goal
        init_board = Board([[2, 3, 6], [1, 4, 8], [7, 5, 0]], 2, 2)
        init = State(init_board, 0, 0)

        goal_board = Board([[1, 2, 3], [4, 5, 6], [7, 8, 0]], 2, 2)
        goal = State(goal_board, 0, 0)

        current = init
        tiles = 8

        # Try code thread thing


    def run(self):
        print("Start State: \n")


        path = 0
        while current != goal:
            state_walk()
            print()
            path += 1
            test = current.getBoard().getTile_seq()
            for i in test:
                for j in i:
                    print(str(j) + " ", end=" ")
                print()
        print("It took path"+ str(path) +" Iterations")
        print("The length of the path is: " + str(current.getDepth()))




def __eq__(self, other):
    return self.getBoard().getTile_seq() == other.getBoard().getTile_seq()
def __ne__(self, other):
    return self.getBoard().getTile_seq() != other.getBoard().getTile_seq()

def swapPositions(board, row_a, col_a, row_b, col_b):
    tile_seq = board.getTile_seq()
    tile_seq[row_a][col_a], tile_seq[row_b][col_b] = tile_seq[row_b][col_a], tile_seq[row_a][col_b]
    board.setTile_seq(tile_seq)
    board.setRow(row_b)
    board.setColumn(col_a)


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
    return ret


def state_walk():
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
    if row + 1 < len(walk_state.getTile_seq()):
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
    if col + 1 < len(walk_state.getTile_seq()[0]):
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
    if col - 1 >= 0:
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



#    current[0] = openStates[0]
epp = EightPuzzlePrint()
epp.start()
epp.run()
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

