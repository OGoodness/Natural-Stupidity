from Board import Board


class State:
    board = None
    depth = 0
    weight = 0

    # Not needed
    # children = {"up": None, "down": None, "left": None, "right": None,}

    def __init__(self, board, depth=0, weight=0):
        super()
        self.board = Board(board)
        self.depth = depth
        self.weight = weight

    def getWeight(self):
        return self.weight

    def getDepth(self):
        return self.depth

    def getBoard(self):
        return self.board

    # Not needed
    # def getChildren(self):
    #    return self.children

    def setBoard(self, board):
        self.board = board

    def setDepth(self, depth):
        self.depth = depth

    def setWeight(self, weight):
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

        self.weight = weight

    # def setChildren(self, children):
    #    self.children = children

    def __eq__(self, other):
        return self.getBoard().getTile_seq() == other.getBoard().getTile_seq()

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
