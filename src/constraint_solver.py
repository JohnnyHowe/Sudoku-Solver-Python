from solver import Solver


class ConstraintSolver(Solver):
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
        board = ConstraintSolver.get_board(filename)
        if show_solving:
            print(board, end="\n"+"="*21+"\n\n")  # Print board out with a line of equal signs below it

        change = False
        while change:
            if show_solving:
                print(board, end="\n" + "=" * 21 + "\n\n")  # Print board out with a line of equal signs below it
            if not (ConstraintSolver.partial_solve_eliminate(board) or ConstraintSolver.naked_twins(board)):
                change = False

        return board

    @staticmethod
    def naked_twins(board):
        """ When in a row, column or section, if there are two cells, containing the same two values,
        then any other cell in that row, column or section cannot contain those two values.
        apply this constraint to the board.
        Parameters:
            board (Board): sudoku to partially solve
        Returns:
            change (bool): whether any changes were made
        """
        change = False
        for i in range(9):
            if ConstraintSolver.naked_twins_row(board, i) or ConstraintSolver.naked_twins_column(board, i):
                change = True
        if ConstraintSolver.naked_twins_sections(board):
            change = True
        return change

    @staticmethod
    def naked_twins_sections(board):
        """ Apply the naked twins constraint to all sections.
        Parameters:
            board (Board): sudoku to partially solve
        Returns:
            change (bool): Was anything changed?
        """
        changed = False
        for y in range(3):
            for x in range(3):
                if ConstraintSolver.naked_twins_section(board, x, y):
                    changed = True
        return changed

    @staticmethod
    def naked_twins_section(board, x, y):
        """ Apply the naked twins constraint to the section at x, y.
        More about the naked twins constraint in the naked_twins method.
        Parameters:
            board (Board): sudoku to partially solve
            x (int): x ordinate of section to check
            y (int): y ordinate of section to check
        Returns:
            change (bool): Was anything changed?
        """
        changed = False
        section = board.get_at(x, y)

        section_values = []
        for yi in range(3):
            for xi in range(3):
                section_values.append(section.get_at(xi, yi))
        indices = ConstraintSolver.value_count(section_values)

        # What cells qualify for the naked_twins constraint?
        for values, ys in indices.items():
            if len(ys) == 2 and len(values) == 2:
                # No other items in this row can have the values
                if ConstraintSolver.remove_overlap_row(section_values, values, ys):
                    changed = True

        # Apply changes
        for yi in range(3):
            for xi in range(3):
                index = xi + yi * 3
                section.set_at(section_values[index], xi, yi)
        return changed

    @staticmethod
    def naked_twins_column(board, x):
        """ Apply the naked twins constraint to the column at x.
        More about the naked twins constraint in the naked_twins method.
        Parameters:
              board (Board): sudoku to partially solve
              x (int): x ordinate of row to check
        """
        changed = False
        column = board.get_column(x)
        indices = ConstraintSolver.value_count(column)

        # What cells qualify for the naked_twins constraint?
        for values, ys in indices.items():
            if len(ys) == 2 and len(values) == 2:
                # No other items in this row can have the values
                if ConstraintSolver.remove_overlap_row(column, values, ys):
                    changed = True

        # Apply changes
        for y in range(9):
            board.set_board_item(column[y], x, y)
        return changed

    @staticmethod
    def naked_twins_row(board, y):
        """ Apply the naked twins constraint to the row at y.
        More about the naked twins constraint in the naked_twins method.
        Parameters:
              board (Board): sudoku to partially solve
              y (int): y ordinate of row to check
        """
        changed = False
        row = board.get_row(y)
        indices = ConstraintSolver.value_count(row)

        # What cells qualify for the naked_twins constraint?
        for values, xs in indices.items():
            if len(xs) == 2 and len(values) == 2:
                # No other items in this row can have the values
                if ConstraintSolver.remove_overlap_row(row, values, xs):
                    changed = True

        # Apply changes
        for x in range(9):
            board.set_board_item(row[x], x, y)
        return changed

    @staticmethod
    def value_count(values):
        """ How many times do each value in values appear?
        The returned dictionary has the keys as items from the values array and
        the values are lists of indices.
        Parameters:
            values (list): values to count
        Returns:
            counts (dictionary): count dict
        """
        indices = {}
        for x, value in enumerate(values):
            if type(value) == list:
                value_tup = tuple(value)
                if value_tup in indices:
                    indices[value_tup] += [x, ]
                else:
                    indices[value_tup] = [x]
        return indices

    @staticmethod
    def remove_overlap_row(row, to_remove, ignore):
        """ Search through all sub lists of row and remove all values from to_remove
        Parameters:
            row (list): row to remove values from
            to_remove (list): list of integers to remove from row
            ignore (list): indices to ignore
        Returns:
            change (bool): whether the list actually changed
        """
        changed = False
        for x, cell in enumerate(row):
            if type(cell) == list and x not in ignore:
                if ConstraintSolver.remove_cell_overlap(cell, to_remove):
                    changed = True
        return changed

    @staticmethod
    def remove_cell_overlap(cell, to_remove):
        """ Remove the overlap of cell and to_remove from cell.
        Parameters:
            cell (list): the cell to modify
            to_remove (list): list of integers to remove from row
        Returns:
            change (bool): whether change was made
        """
        changed = False
        for value in to_remove:
            if value in cell:
                cell.remove(value)
                changed = True
        return changed

    @staticmethod
    def partial_solve_eliminate(board):
        """ when a cell can only be one value, set it to that value.
        It is assumed that when the board, is given, the candidates are up to date
        Re-calculates candidates automatically
        Parameters:
              board (Board): sudoku to partially solve
        Returns:
            change (bool): whether any changes were made
        """
        change = False
        for y in range(9):
            for x in range(9):
                cell = board.get_board_item(x, y)
                if type(cell) == list:
                    if len(cell) == 1:
                        board.set_board_item(cell[0], x, y)
                        change = True
        ConstraintSolver.fill_candidates(board)
        return change


if __name__ == "__main__":
    import time
    print("Solving...")
    start_time = time.time()
    solved_board = ConstraintSolver.solve(show_solving=True)
    end_time = time.time()
    print("Solved sudoku:")
    print(solved_board)
    print("Completed in {}s".format(round(end_time - start_time, 3)))

    print()
    for y in range(9):
        for x in range(9):
            char = solved_board.get_board_item(x, y)
            if type(char) != int:
                char = " "
            print(char, end="")
        print()

    input()
