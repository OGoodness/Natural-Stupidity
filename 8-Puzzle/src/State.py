from Board import Board


class State:
    board = None
    depth = 0
    weight = 0
    parent = None


    def __init__(self, board, depth=0, weight=0):
        super()
        self.board = Board(board)
        self.depth = depth
        self.weight = weight
        self.path = [self]

    def getWeight(self):
        return self.weight

    def getPath(self):
        return self.path

    def getDepth(self):
        return self.depth

    def getParent(self):
        return self.parent


    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def setParent(self, state):
        self.parent = state

    def setDepth(self, depth):
        self.depth = depth

    def setWeight(self, weight):
        self.weight = weight
    # TODO: make print path function work. I may not be setting path correctly
    def printPath(self):
        path_array = [self]
        current = self
        while True:
            parent = current.getParent()
            if not isinstance(parent, State):
                break
            path_array.append(parent)
            current = parent



        for i, state in reversed(list(enumerate(path_array))):
            state.print()
            print()
    def __eq__(self, other):
        return self.getBoard().getTile_seq() == other.getBoard().getTile_seq()

    def __ne__(self, other):
        return self.getBoard().getTile_seq() != other.getBoard().getTile_seq()

    def compare(self, a2):
        if self.getWeight() > a2.getWeight():
            return 1
        elif self.getWeight() == a2.getWeight():
            if self.getDepth() > a2.getDepth():
                return 1
            else:
                return 0
        else:
            return -1

    def equals(self):
        op = self.gettile_seq()

        for i in len(op):
            for j in len(op[i]):
                if self.tile_seq[i][j] != op[i][j]:
                    return False
        return True;

    def print(self):
        for i in self.getBoard().getTile_seq():
            for j in i:
                print(str(j) + " ", end=" ")
            print()
