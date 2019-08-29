# TODO set equal to state

from . import State

current = None
tiles = 8
openStates = None
closedState = None


class EightPuzzlePrint:
    initial = State.State()
    goalA = State.State()
    tiles = 8

    def __init__(self):
        super()

    def __init__(self, ini, goal, tile):
        super()
        self.initial = ini
        self.goalA = goal
        self.tiles = tile

    class Start:
        init_tile = {{2, 3, 6}, {1, 4, 8}, {7, 5, 0}}
        init = State.State(init_tile, 0)

        goal_tile = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}
        goal = State.State(goal_tile, 0)

        initial = init
        goalA = goal

        tiles = 8

        # Try code thread thing


epp = EightPuzzlePrint()
epp.Start()


#check if the generated state is in open or closed
#the purpose is to avoid a circle
def check_inclusive(s):
    in_open = 0
    in_closed = 0
    ret = {-1, -1}

    for i in openStates:
        temp = i
        if (temp == s):
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
        ret[0] = 1
    elif in_open == 1 and in_closed == 0:
        ret[0] = 2
    elif in_open == 0 and in_closed == 1:
        ret[0] = 3

    return ret

def swapPositions(state, row_a, col_a, row_b, col_b):
    state[row_a][col_a], state[row_b][col_b] = state[row_b][col_a], state[row_a][col_b]
    return state

def state_walk():
    closedState.add(current)
    openStates.add(current)
    walk_state = current.getTile_seq()

    row = 0
    col = 0

    for i in range(0, len(walk_state)):
        for j in range(0, len(walk_state[i])):
            if walk_state[i][j] == 0:
                row = i
                col = j
                break
    # TODO I can't seem to find where this is created in the normal code, it shouldbe +=
    depth = 1
    #Item Moving Down
    if row - 1 >= 0:
        swapPositions(walk_state, row, col, row-1, col)
        check = check_inclusive()
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 1:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 1:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")



    #Item Moving Up
    if row + 1 < len(walk_state):
        swapPositions(walk_state, row, col, row+1, col)
        check = check_inclusive()
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 1:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 1:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")


    #Item Moving Right
    if col + 1 < walk_state:
        swapPositions(walk_state, row, col, row, col+1)
        check = check_inclusive()
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 1:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 1:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")


        # Item Moving Left
    if col - 1 < walk_state:
        swapPositions(walk_state, row, col, row, col-1)
        check = check_inclusive()
        if check == 1:
            #heuristic_test
            print("heuristic_test")
        elif check == 1:
            #Open. Compare path to duplicate state, if shorter then give state on open, the shorter path
            print("Compare path to duplicate state, if shorter then give state on open, the shorter path")
        elif check == 1:
            #Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open
            print("Closed. Compare to ones in closed, if shorter then remove statre from closed and add the child to open")






    #TODO python sort

    current[0]
