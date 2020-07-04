from solver import Solver

class ContraintSolver(Solver):
    """ Solve the sudoku by treating it as a constraint problem. """

    @staticmethod
    def solve(filename="game.txt", show_solving=False):
        """ Solve the sudoku at filename and return it.
        Parameters:
            filename (string): filename that sudoku is saved in
            show_solving (bool): Whether to show the solving of the sudoku (when possible)
        Returns:
            sudoku (Board): The solved sudoku (or None if not possible)
        """
        board = ContraintSolver.get_board(filename)
        if show_solving:
            print(board, end="\n"+"="*21+"\n")  # Print board out with a line of equal signs below it
        ContraintSolver.partial_solve(board)
        if show_solving:
            print(board, end="\n"+"="*21+"\n")  # Print board out with a line of equal signs below it

    @staticmethod
    def partial_solve(board):
        """ With only basic reasoning, partially solve the board.
        This means when a cell can only be one value, set it to that value.
        This continues until no change is found
        It is assumed that when the board, is given, the candidates are up to date

        Note: this may fully solve the puzzle, may also solve no part of it

        Parameters:
              board (Board): sudoku to partially solve
        """
        change = True
        while change:
            change = False
            for y in range(9):
                for x in range(9):
                    cell = board.get_board_item(x, y)
                    if type(cell) == list:
                        if len(cell) == 1:
                            board.set_board_item(cell[0], x, y)
                            change = True
            ContraintSolver.fill_candidates(board)


if __name__ == "__main__":
    # import time
    # print("Solving...")
    # start_time = time.time()
    solved_board = ContraintSolver.solve(show_solving=True)
    # end_time = time.time()
    # print("Solved sudoku:")
    # print(solved_board)
    # print("Completed in {}s".format(round(end_time - start_time, 3)))
    # input()
