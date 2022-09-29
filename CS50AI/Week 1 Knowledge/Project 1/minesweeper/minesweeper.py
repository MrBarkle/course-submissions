import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # If count isn't 0, mines exist.
        # If count is equal to number of cells and mines exist, all are mines.
        # If not equal, and mines exist, we don't know which cells are mines.
        if self.count == len(self.cells) and self.count != 0:
            # All are mines
            return self.cells
        else:
            # Return empty set, need more information
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If count is 0, we know that all of the cells must be safe
        if self.count == 0:
            # All are safe
            return self.cells
        else:
            # Return empty set, need more information
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If cell is included in sentence
        if cell in self.cells:
            # Update sentence to not include cell while remaining logically
            # correct given that cell is known to be a mine
            self.cells.remove(cell)
            # Decrease count when removing a known mine
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If cell is included in sentence
        if cell in self.cells:
            # Update sentence to not include cell given that cell is known to
            # be safe
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base based on the value of
        # `cell` and `count`
        new_sentence = Sentence(self.find_neighbors(cell), count)
        # We’ll only want our sentences to be about cells that are not yet known
        # to be either safe or mines
        self.knowledge.append(new_sentence)

        # Mark any additional cells as safe or as mines if it can be concluded
        # based on the AI's knowledge base
        for sentence in self.knowledge:
            # Find known mines
            mines = sentence.known_mines()
            # If mines found
            if len(mines) != 0:
                # Keep track of mines
                self.mines = self.mines.union(mines)
            # Find known safes
            safes = sentence.known_safes()
            # If safes found
            if len(safes) != 0:
                # Keep track of safes
                self.safes = self.safes.union(safes)
            # Mark new finds while avoiding changes during iteration
            for c in sentence.cells.copy():
                if c in mines:
                    # Mark new mines
                    self.mark_mine(c)
                if c in safes:
                    # Mark new safes
                    self.mark_safe(c)

        # Add any new sentences to the AI's knowledge base if they can be
        # inferred from existing knowledge
        update_knowledge = []
        # Iterate over knowledge base
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                # Check if sentence 1 is a subset of sentence 2
                if s1.cells.issubset(s2.cells):
                    # Infer new sentence based on math described in project desc
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    new_sentence = Sentence(new_cells, new_count)
                    update_knowledge.append(new_sentence)
        # Update old knowledge base with sentences from new knowledge base
        for sentence in update_knowledge:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)

    def find_neighbors(self, cell):
        """
        Given a cell, return a list of its undetermined neighbors on the board.
        """
        i, j = cell

        # All possible neighbors
        check = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1),
                 (i+1, j-1), (i+1, j), (i+1, j+1)]
        # Running list of neighbors
        neighbors = []
        # Check which neighbors exist
        for n in check:
            # Don't add clicked neighbors to the list
            if n not in self.moves_made:
                # Make sure neighbor is valid on this board
                if n[0] in range(0, self.height) and n[1] in range(0, self.width):
                    neighbors.append(n)
        # Return list
        return neighbors

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # If known safe moves exist
        if len(self.safes) != 0:
            # Loop over each known safe move
            for move in self.safes:
                # If the move has not yet been made
                if move not in self.moves_made:
                    # Return safe move
                    return move
        # No safe moves to make
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Create list of all restricted moves
        restricted = self.moves_made.union(self.mines)
        # Create list of all available moves
        # List comprehension should be faster when creating lists vs for loop
        choice = random.choice([[(i, j) for i in range(0, self.height)
                                 for j in range(0, self.width)
                                 if (i, j) not in restricted]])
        # If there is a choice to make
        if len(choice) != 0:
            # Return the random choice
            return choice[0]
        # Else None
        else:
            return None
