


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


    def get_column(self):
        return self.column

    def get_tile_seq(self):
        return self.tile_seq

    def get_row(self):
        return self.row

    def set_tile_seq(self, tile_seq):
        self.tile_seq = tile_seq

    def set_row(self, row):
        self.row = row

    def set_column(self, column):
        self.column = column

