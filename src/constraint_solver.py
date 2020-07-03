from board import Board
import pygame


class GUI:
    def __init__(self):
        self.window_width = 400
        self.window = pygame.display.set_mode((self.window_width, ) * 2)

    def run(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()

    def update(self, board):
        self.run()
        self.window.fill((255, 255, 255))
        pygame.display.flip()


class ContraintSolver:
    """ Solve the sudoku by treating it as a constraint problem. """

    def __init__(self, filename="game.txt", show_solving=False):
        """ Load up the board, solve it. """
        self.board = Board()
        self.board.load_board(filename)

        self.gui = GUI()
        self.gui.run()

        # print(self.board)
        # print("=" * 21)
        self.solve()
        # print(self.board)
        # print("NOT IMPLIMENTED YET")

    def get_blanks(self):
        """ Finds all the blank spots in the sudoku at self.board.
        Returns:
            blanks (list): list of x, y pairs corresponding to all blanks in the board.
        """
        blanks = []  # an array of x, y pairs
        for y in range(9):
            for x in range(9):
                number = self.board.get_board_item(x, y)
                if number is None:
                    blanks.append((x, y))
        return blanks

    def get_candidates(self):
        """ For each blank spot in the game board, find the possible candidates.
        Returns:
            candidates (dictionary): keys: position (x, y), values: list of candidates (int between 1 and 9 (inclusive)
        """
        blanks = self.get_blanks()
        options = {}
        for x, y in blanks:
            options[(x, y)] = []
            # Test numbers 1-9
            for candidate in range(1, 10):
                self.board.set_board_item(candidate, x, y)
                if self.board.is_valid():
                    options[(x, y)].append(candidate)
            self.board.set_board_item(None, x, y)  # Change board back to original state
        return options

    def insert_definite_candidates(self, candidates):
        """ If a cell only has one candidate, insert it.
        Parameters:
            candidates (dictionary): dict returned by get_candidates
        Returns:
            inserts (int): Number of candidates inserted.
        """
        inserts = 0
        for pos, candidates in candidates.items():
            if len(candidates) == 0:     # Impossible
                raise ValueError("Sudoku not possible to solve")
            if len(candidates) == 1:
                inserts += 1
                self.board.set_board_item(candidates[0], pos[0], pos[1])
        return inserts

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
