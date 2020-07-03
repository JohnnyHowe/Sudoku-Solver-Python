from board import Board


class BacktrackSolver:
    """ Solve the sudoku at "game.txt" by backtracking.
    This method is pretty much a depth-first search. """

    def __init__(self, filename="game.txt", show_solving=False):
        """ Load up the board, solve it. """
        self.board = Board()
        self.board.load_board(filename)

        print(self.board)
        print("=" * 21)
        BacktrackSolver.backtrack(self.board, show_solving)
        print(self.board)

    @staticmethod
    def backtrack(board, show_solving=False):
        """ Given the game board, solve it with backtracking
        Parameters:
            board (Board): game board to backtrack from
            show_solving (boolean): Spit out each iteration of the board to the console?
        Returns:
            valid (boolean): Whether it was solved or not
        """
        if show_solving:
            print(board)
            print("=" * 21)
        pos = BacktrackSolver.first_blank(board)

        if pos is None:
            # Board is full!
            return True

        for number in range(1, 10):
            board.set_board_item(number, pos[0], pos[1])
            # print(board)

            if board.is_valid():
                solved = BacktrackSolver.backtrack(board, show_solving)
                if solved:
                    return True

        board.set_board_item(None, pos[0], pos[1])  # Reset the number
        return False

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
    BacktrackSolver(show_solving=True)
