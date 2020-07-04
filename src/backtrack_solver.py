# from abc import ABC, abstractmethod
from solver import Solver


class BacktrackSolver(Solver):
    """ Solve the sudoku at "game.txt" by backtracking.
    This method is pretty much a depth-first search. """

    @staticmethod
    def solve(filename="game.txt", show_solving=False):
        """ Solve the sudoku at filename and return it.
        Parameters:
            filename (string): filename that sudoku is saved in
            show_solving (bool): Whether to show the solving of the sudoku (when possible)
        Returns:
            sudoku (Board): The solved sudoku (or None if not possible)
        """
        board = BacktrackSolver.get_board(filename)
        BacktrackSolver.backtrack(board, (-1, 0), show_solving)
        return board

    @staticmethod
    def backtrack(board, last_pos, show_solving=False):
        """ Given the game board, solve it with backtracking
        Parameters:
            board (Board): game board to backtrack from
            last_pos (tuple): last searched coordinate
            show_solving (boolean): Spit out each iteration of the board to the console?
        Returns:
            valid (boolean): Whether it was solved or not
        """
        if show_solving:
            print(board, end="\n"+"="*21+"\n")  # Print board out with a line of equal signs below it

        next_blank = BacktrackSolver.get_next_blank(board, last_pos)
        if next_blank is None:  # No more blanks = we complete
            return True
        else:
            x, y = next_blank
        candidates = board.get_board_item(x, y)

        for candidate in candidates:
            board.set_board_item(candidate, x, y)
            if board.is_valid():
                if BacktrackSolver.backtrack(board, (x, y), show_solving):
                    return True

        # If this code is reached, then this branch is a failure
        board.set_board_item(candidates, x, y)
        return False

    @staticmethod
    def get_next_blank(board, last_pos):
        """ Find the position of the next blank spot on the board.
        Parameters:
            board (Board): game board to find first blank on.
            last_pos (tuple): last position searched, start from next pos
        Returns:
            position (tuple): first blank pos after last_pos. None is returned if the board is full
        """
        x, y = last_pos
        while not (y >= 8 and x >= 8):
            x += 1
            if x >= 9:  # New line
                y += 1
                x -= 9
            if type(board.get_board_item(x, y)) == list:
                return x, y
        return None


if __name__ == "__main__":
    import time
    print("Solving...")
    start_time = time.time()
    solved_board = BacktrackSolver.solve(show_solving=True)
    end_time = time.time()
    print("Solved sudoku:")
    print(solved_board)
    print("Completed in {}s".format(round(end_time - start_time, 3)))

    for y in range(9):
        for x in range(9):
            print(solved_board.get_board_item(x, y), end="")
        print()

    input()
