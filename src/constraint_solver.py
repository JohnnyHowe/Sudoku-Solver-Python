from board import Board


class ContraintSolver:
    """ Solve the sudoku by treating it as a constraint problem. """

    def __init__(self, filename="game.txt", show_solving=False):
        """ Load up the board, solve it. """
        self.board = Board()
        self.board.load_board(filename)

        # print(self.board)
        # print("=" * 21)
        self.solve()
        # print(self.board)
        # print("NOT IMPLIMENTED YET")


    def solve(self):
        """ Solve the sudoku at self.board.
        Makes a list of possible numbers for each cell.
        if a definite choice is found, the effected options must be updated.
        """
        print(self.board)
        print("=" * 21)
        candidates = self.get_candidates()
        inserts = self.insert_definite_candidates(candidates)
        while inserts != 0:
            print(self.board)
            print("=" * 21)
            candidates = self.get_candidates()
            inserts = self.insert_definite_candidates(candidates)
        # print(candidates)
        for pos, candidates in candidates.items():
            print(str(pos) + ": " + str(candidates))

    @staticmethod
    def first_blank(board):
        """ Find the position of the first blank spot on the board.
        Parameters:
            board (Board): game board to find first blank on.
        Returns:
            position (tuple): (x, y) of first blank. If board is not blank, None is return
        """
        for y in range(9):
            for x in range(9):
                number = board.get_board_item(x, y)
                if number is None:
                    return x, y
        return None


if __name__ == "__main__":
    ContraintSolver(show_solving=True)
