class State:
    board = None
    depth = 0;
    weight = 0;

    def __init__(self, board, depth = 0, weight = 0):
        super();
        self.board = board
        self.depth = depth;
        self.weight = weight;

    def getWeight(self):
        return self.weight;

    def getDepth(self):
        return self.depth;

    def getBoard(self):
        return self.board;

    def setBoard(self, board):
        self.board = board;

    def setDepth(self, depth):
        self.depth = depth;

    def setWeight(self, weight):
        self.weight = weight;

    def equals(self):
        op = self.gettile_seq();

        for i in len(op):
            for j in len(op[i]):
                if self.tile_seq[i][j] != op[i][j]:
                    return False;
        return True;



