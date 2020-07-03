
class Section:
    """ Class to represent a section of the sudoku board.
    Splits the section into 9 other sections. """

    def __init__(self):
        """ Initialize the Section, sets each slot to None. """
        self._slots = [None, ] * 9

    def get_at(self, x, y):
        """ Get the item in the slot at (x, y).
        x and y must be between 0 and 2 (inclusive).

        Parameters:
            x (int): x ordinate
            y (int): y ordinate
        Returns:
            item (object): item at (x, y)
        """
        if not (0 <= x <= 2 and 0 <= y <= 2):
            raise IndexError("Can't get item at ({}, {})".format(x, y))
        return self._slots[x + y * 3]

    def set_at(self, item, x, y):
        """ Set the item at (x, y) to item.
        Parameters:
            item (object): object to set item to at the position (x, y)
            x (int): x ordinate
            y (int): y ordinate
        """
        self._slots[x + y * 3] = item


class Board(Section):
    """ Class to represent the board,
    Is really just a section class but each slot is another section rather than a number. """

    def __init__(self):
        Section.__init__(self)
        self.set_sections()

    def load_board(self, filename="game.txt"):
        """ Load the board at filename into this
        The file is to be layed out in a 9x9 grid of characters directly representing the game.
        Blanks are to be left as spaces. """
        file = open(filename, "r")
        board_raw = file.read()
        file.close()
        for y, line in enumerate(board_raw.splitlines()):
            for x, char in enumerate(line):
                if x >= 9:
                    break
                if char != " ":
                    self.set_board_item(int(char), x, y)

    def get_copy(self):
        """ Return a copy of the board. """
        new_board = Board()
        for x in range(9):
            for y in range(9):
                new_board.set_board_item(self.get_board_item(x, y), x, y)
        return new_board

    def set_sections(self):
        """ Set all the sections of self to new sections. """
        for x in range(3):
            for y in range(3):
                self.set_at(Section(), x, y)

    def set_board_item(self, number, x, y):
        """ Set the item at x, y on the board.
        x and y are to between 0 and 8 (inclusive)

        Parameters:
            number (int): number to set
            x (int): x ordinate
            y (int): y ordinate
        """
        self.get_at(x // 3, y // 3).set_at(number, x % 3, y % 3)

    def get_board_item(self, x, y):
        """ Get the item at x, y on the board.
        x and y are to between 0 and 8 (inclusive)

        Parameters:
            x (int): x ordinate
            y (int): y ordinate
        Returns:
            item (number): the number on the board at (x, y)
        """
        return self.get_at(x // 3, y // 3).get_at(x % 3, y % 3)

    def is_solved(self):
        """ Is the board solved?
        Is solved if it is valid and there are no blank spots. """
        for x in range(9):
            for y in range(9):
                if self.get_board_item(x, y) is None:
                    return False    # There's a blank spot!
        # Only gets to this line if there are no blanks
        return self.is_valid()

    def is_valid(self):
        """ Is the board valid?
        Does it violate any of the constraints?
        - is there two or more of the same numbers in the same section
        - are there two or more of the same numbers in the same line
        """
        # All vertical lines
        for x in range(9):
            if not self.is_line_valid_vertical(x):
                return False
        # All horizontal lines
        for y in range(9):
            if not self.is_line_valid_horizontal(y):
                return False
        # All sections
        for x in range(3):
            for y in range(3):
                if not self.is_section_valid(x, y):
                    return False
        return True

    def is_line_valid_horizontal(self, y):
        """ Is the horizontal line valid?
        Line is valid if no number is repeated twice or more.
        Returns:
            valid (bool): whether the line is valid
        """
        taken_numbers = [0, ] * 9
        for x in range(9):
            number = self.get_board_item(x, y)
            if number is not None:
                index = int(number) - 1
                if taken_numbers[index]:
                    return False
                taken_numbers[index] = 1
        return True

    def is_line_valid_vertical(self, x):
        """ Is the vertical line valid?
        Line is valid if no number is repeated twice or more.
        Returns:
            valid (bool): whether the line is valid
        """
        taken_numbers = [0, ] * 9
        for y in range(9):
            number = self.get_board_item(x, y)
            if number is not None:
                index = int(number) - 1
                if taken_numbers[index]:
                    return False
                taken_numbers[index] = 1
        return True

    def is_section_valid(self, section_x, section_y):
        """ Is the section valid?
        invalid if there are two or more of the same number in the section. """
        section = self.get_at(section_x, section_y)
        taken_numbers = [0, ] * 9
        for x in range(3):
            for y in range(3):
                number = section.get_at(x, y)
                if number is not None:
                    index = number - 1
                    if taken_numbers[index] > 0:
                        return False
                    taken_numbers[index] = 1
        return True

    def __str__(self):
        """ Create a nice string representation of the board. """
        string = ""
        for y in range(9):
            for x in range(9):

                section = self.get_at(x // 3, y // 3)
                number = section.get_at(x % 3, y % 3)

                if x % 3 == 0 and x != 0:
                    # print("|", end=" ")
                    string += "| "

                if number is None:
                    char = " "
                else:
                    char = str(number)
                # print(char, end=" ")
                string += char + " "

            # Print a new horizontal line to separate sections
            # If no new line is needed, print a new line
            if y % 3 == 2 and y != 8:
                # print("\n" + "-" * 21)
                string += "\n" + ("-" * 21) + "\n"
            else:
                # print()
                string += "\n"

        return string[:-1]  # Remove the newline
