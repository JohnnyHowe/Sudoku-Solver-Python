from board import Board


class StochasticSolver:
    """ Solve the sudoku at "game.txt" by Stochastic searching. """

    def __init__(self, filename="game.txt", show_solving=False):
        """ Load up the board, solve it. """
        self.board = Board()
        self.board.load_board(filename)

        # print(self.board)
        # print("=" * 21)
        # print(self.board)
        print("NOT IMPLIMENTED YET")

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
    StochasticSolver(show_solving=True)
