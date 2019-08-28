class State:
    tile_seq = [[]];
    depth = 0;
    weight = 0;

    def __init__(self, tile_seq, depth, weight):
        super();
        self.tile_seq = tile_seq;
        self.depth = depth;
        self.weight = weight;

    def getWeight(self):
        return self.weight;

    def gettile_seq(self):
        return self.tile_seq;

    def getDepth(self):
        return self.depth;

    def settile_seq(self, tile_seq):
        self.tile_seq = tile_seq;

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


