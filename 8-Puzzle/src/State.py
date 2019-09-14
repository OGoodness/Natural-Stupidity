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

    def get_weight(self):
        return self.weight

    def get_path(self):
        return self.path

    def get_depth(self):
        return self.depth

    def get_parent(self):
        return self.parent

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

    def set_parent(self, state):
        self.parent = state

    def set_depth(self, depth):
        self.depth = depth

    def set_weight(self, weight):
        self.weight = weight

    # TODO: make print path function work. I may not be setting path correctly
    def printPath(self):
        path_array = [self]
        current = self
        while True:
            parent = current.get_parent()
            if not isinstance(parent, State):
                break
            path_array.append(parent)
            current = parent

        for i, state in reversed(list(enumerate(path_array))):
            state.print()
            print()

    def __eq__(self, other):
        return self.get_board().get_tile_seq() == other.get_board().get_tile_seq()

    def __ne__(self, other):
        return self.get_board().get_tile_seq() != other.get_board().get_tile_seq()

    def print(self):
        for i in self.get_board().get_tile_seq():
            for j in i:
                print(str(j) + " ", end=" ")
            print()
