


class Board:
    tile_seq = []
    row = 0
    column = 0

    def __init__(self, tile_seq):
        super()
        empty_tile = [x for x in tile_seq if 0 in x][0]
        empty_tile = (tile_seq.index(empty_tile), empty_tile.index(0))
        self.tile_seq = tile_seq
        self.row = empty_tile[0]
        self.column = empty_tile[1]


    def getColumn(self):
        return self.column

    def getTile_seq(self):
        return self.tile_seq

    def getRow(self):
        return self.row

    def setTile_seq(self, tile_seq):
        self.tile_seq = tile_seq

    def setRow(self, row):
        self.row = row

    def setColumn(self, column):
        self.column = column

    def equals(self):
        op = self.getTile_seq()

        for i in len(op):
            for j in len(op[i]):
                if self.tile_seq[i][j] != op[i][j]:
                    return False
        return True

