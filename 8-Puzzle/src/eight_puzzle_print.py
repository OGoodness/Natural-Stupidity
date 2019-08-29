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
    if row - 1 >= 0:
        """
get the 2d array of current 
define a temp 2d array and loop over current.tile_seq
pass the value from current.tile_seq to temp array
¡ü is correspond to (row, col) and (row-1, col)
exchange these two tiles of temp
define a new temp state via temp array
call check_inclusive(temp state)
do the next steps according to flag
if flag = 1 //not in open and closed
begin
assign the child a heuristic value via heuristic_test(temp state);
add the child to open
end;
if flag = 2 //in the open list
if the child was reached by a shorter path
then give the state on open the shorter path
if flag = 3 //in the closed list
if the child was reached by a shorter path then
begin
remove the state from closed;
add the child to open
end;
//TODO your code end here
        """
    if row + 1 < len(walk_state):
        """
        get the 2d array of current 
define a temp 2d array and loop over current.tile_seq
pass the value from current.tile_seq to temp array
¡ü is correspond to (row, col) and (row+1, col)
exchange these two tiles of temp
define a new temp state via temp array
call check_inclusive(temp state)
do the next steps according to flag
if flag = 1 //not in open and closed
begin
assign the child a heuristic value via heuristic_test(temp state);
add the child to open
end;
if flag = 2 //in the open list
if the child was reached by a shorter path
then give the state on open the shorter path
if flag = 3 //in the closed list
if the child was reached by a shorter path then
begin
remove the state from closed;
add the child to open
end;
//TODO your code end here
        """
    if col + 1 < walk_state:
        """
        //TODO your code start here
/**
*get the 2d array of current 
*define a temp 2d array and loop over current.tile_seq
*pass the value from current.tile_seq to temp array
*¡ü is correspond to (row, col) and (row, col+1)
*exchange these two tiles of temp
*define a new temp state via temp array
*call check_inclusive(temp state)
*do the next steps according to flag
*if flag = 1 //not in open and closed
*begin
*assign the child a heuristic value via heuristic_test(temp state);
*add the child to open
*end;
*if flag = 2 //in the open list
*if the child was reached by a shorter path
*then give the state on open the shorter path
*if flag = 3 //in the closed list
*if the child was reached by a shorter path then
*begin
*remove the state from closed;
*add the child to open
*end;
*/
//TODO your code end here
        """

    # TODO python sort

    current[0]
