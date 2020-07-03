from board import Board

class BacktrackSolver:
    """ Solve the sudoku at "game.txt" by backtracking. """

    def __init__(self, filename="game.txt"):
        """ Load up the board, solve it. """
        self.board = Board()
        self.board.load_board()
        print(self.board)
        # self.solve()
        print("\nSolving\n")
        print(self.board)

    def solve(self):
        """ Do the solving. """
        self.backtrack(self.board)

    def backtrack(self, board):
        """ Given the game board, solve it with backtracking

        Parameters:
            board (Board): game board to backtrack from
        """
        pos = BacktrackSolver.first_blank(board)
        for number in range(1, 10):
            board.set_board_item(number, pos[0], pos[1])

    @staticmethod
    def first_blank(board):
        """ Find the position of the first blank spot on the board.
        Parameters:
            board (Board): game board to find first blank on.
        Returns:
            position (tuple): (x, y) of first blank. If board is not blank, None is return
        """
        for x in range(9):
            for y in range(9):
                number = board.get_board_item(x, y)
                if number is None:
                    return x, y
        return None
