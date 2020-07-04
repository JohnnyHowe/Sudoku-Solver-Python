from abc import ABC, abstractmethod
from board import Board


class Solver(ABC):
    """ Just an abstract class for the other solvers,
    doesn't do any good by itself.
    Contains helper methods
    """

    @staticmethod
    @abstractmethod
    def solve(filename="game.txt", show_solving=False):
        """ Solve the sudoku at filename and return it.
        Parameters:
            filename (string): filename that sudoku is saved in
            show_solving (bool): Whether to show the solving of the sudoku (when possible)
        Returns:
            sudoku (Board): The solved sudoku (or None if not possible)
        """
        pass

    @staticmethod
    def get_board(filename):
        """ Load the board at filename, fill in initial candidates and return it
        Returns:
            board (Board): sudoku at filename
        """
        board = Board()
        board.load_board(filename)
        Solver.fill_candidates(board)
        return board

    @staticmethod
    def fill_candidates(board):
        """ Fill in all blanks in board with of possible candidates.
        A cell is counted as blank if it does not contain an integer.
        Parameters:
            board (Board): sudoku to fill in
        """
        blanks = Solver.get_blanks(board)
        for x, y in blanks:
            candidates = Solver.get_candidates(board, x, y)
            board.set_board_item(candidates, x, y)

    @staticmethod
    def get_blanks(board):
        """ Finds all the blank spots in the sudoku at self.board.
        A cell is considered blank if it does not contain an integer
        Parameters:
              board (Board): sudoku to find blanks from
        Returns:
            blanks (list): list of x, y pairs corresponding to all blanks in the board.
        """
        blanks = []  # an array of x, y pairs
        for y in range(9):
            for x in range(9):
                number = board.get_board_item(x, y)
                if type(number) != int:
                    blanks.append((x, y))
        return blanks

    @staticmethod
    def get_candidates(board, x, y):
        """ What values can go in the cell at (x, y) on the board?
        Parameters:
              board (Board): sudoku to find candidates for
              x (int): x ordinate of cell
              y (int): y ordinate of cell
        Returns:
            candidates (list): list (of ints) of candidates for cell at (x, y)
        """
        candidates = []
        for candidate in range(1, 10):
            board.set_board_item(candidate, x, y)
            if board.is_valid():
                candidates.append(candidate)
        board.set_board_item(None, x, y)  # Change board back to original state
        return candidates

    @staticmethod
    def add_confirmed_candidates(board):
        """ If there is a list of candidates with only 1 value, set the cell to that value.
        "If there's only one thing it can be, why wait?"
        Parameters:
            board (Board): sudoku to find candidates for
        Returns:
            change (bool): Whether any change was made.
        """
        change = False
        for x in range(9):
            for y in range(9):
                cell = board.get_board_item(x, y)
                if type(cell) == list:
                    if len(cell) == 1:
                        board.set_board_item(cell[0], x, y)
                        change = True
        return change

