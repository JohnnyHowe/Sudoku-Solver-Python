from constraint_solver import ConstraintSolver
from backtrack_solver import BacktrackSolver


class ConstraintBacktrackSolver(ConstraintSolver, BacktrackSolver):

    @staticmethod
    def solve(filename="game.txt", show_solving=False):
        """ Solve the sudoku at filename and return it.
        Parameters:
            filename (string): filename that sudoku is saved in
            show_solving (bool): Whether to show the solving of the sudoku (when possible)
        Returns:
            sudoku (Board): The solved sudoku (or None if not possible)
        """
        board = ConstraintBacktrackSolver.get_board(filename)

        print("Using constraints...")
        change = False
        while change:
            if show_solving:
                print(board, end="\n" + "=" * 21 + "\n\n")  # Print board out with a line of equal signs below it
            if not (ConstraintSolver.partial_solve_eliminate(board) or ConstraintSolver.naked_twins(board)):
                change = False
        print("Backtracking...")
        BacktrackSolver.backtrack(board, (-1, 0), show_solving)
        return board


if __name__ == "__main__":
    import time
    print("Solving...")
    start_time = time.time()
    solved_board = ConstraintBacktrackSolver.solve(show_solving=False)
    end_time = time.time()
    print("Solved sudoku:")
    print(solved_board)
    print("Completed in {}s".format(round(end_time - start_time, 3)))

    for y in range(9):
        for x in range(9):
            print(solved_board.get_board_item(x, y), end="")
        print()
    input()