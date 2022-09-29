import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable, values in self.domains.copy().items():
            for v in values.copy():
                if len(v) != variable.length:
                    self.domains[variable].remove(v)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Get overlap if any between x and y
        overlaps = self.crossword.overlaps[x, y]

        # Keep track of whether or not revisions were made
        revisions = False

        # If there is an overlap between variables x and y
        if overlaps != None:
            # Create a set of all letters in x's overlap position
            x_letters = set([word[overlaps[0]] for word in self.domains[x]])
            # Create a set of all letters in y's overlap position
            y_letters = set([word[overlaps[1]] for word in self.domains[y]])
            # Find conflicting characters in x
            remove = x_letters - y_letters
            # Remove conficting characters from x
            for word in self.domains[x].copy():
                if word[overlaps[0]] in remove:
                    # Remove conflict
                    self.domains[x].remove(word)
                    revisions = True

        # Return True or False depending on if revisions were made or not
        return revisions

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Check optional variable
        if arcs is None:
            # Use complete list of all arcs in the problem
            arcs = [(x, y) for x in self.domains.keys()
                    for y in self.domains.keys() if x != y]

        # While queue is non-empty
        while len(arcs) != 0:
            # Pop tuple from queue
            x, y = arcs.pop(0)
            # Call revise on x and y
            if self.revise(x, y):
                # If domain wasn't changed
                if len(self.domains[x]) == 0:
                    # Continue considering the other arcs
                    return False
                # Otherwise, look at all of x's neighbors except for y
                for n in self.crossword.neighbors(x):
                    # Exception
                    if n != y:
                        # Add arcs between n and x to the queue
                        arcs.append((n, x))

        # Arc consistency is enforced and no domains are empty
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Check if all variables in the self.domain are also in assignment
        if len(self.domains) != len(assignment):
            # If not, return false
            return False

        # Else return true
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check to see if the values are distinct, if not return false
        if len(assignment) != len(set(assignment.values())):
            return False

        # Check to see if each value is of the correct length
        for k, v in assignment.items():
            if k.length != len(v):
                return False

        # Check for conflicts between neighboring variables
        for var, value in assignment.items():
            # Get neighbors to var
            for n in self.crossword.neighbors(var):
                # Determine overlap points
                overlaps = self.crossword.overlaps[var, n]
                # Check that the neighbor variable has been assigned a value
                if n in assignment:
                    # Check character at the overlap point
                    if assignment[var][overlaps[0]] != assignment[n][overlaps[1]]:
                        return False

        # Return true if all tests pass
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Keep track of all values within the domain of var and eliminations
        # caused by using each as the value for var based on neighboring values
        values = {k: 0 for k in self.domains[var]}

        # Start by looking at the values in the domain of var
        for value in self.domains[var]:
            # Next look at each neighboring variable of var
            for n in self.crossword.neighbors(var):
                # If n is not already assigned to a value
                if n not in assignment:
                    # Get the point of overlap between var and n
                    overlaps = self.crossword.overlaps[var, n]
                    # Start keeping track of choices eliminated if using 'value'
                    elim = 0
                    # Cross check value and v to see if the char at overlap is
                    # not the same resulting in an increase in an elimination
                    for v in self.domains[n]:
                        # If overlap doesn't work when using value
                        if v[overlaps[1]] != value[overlaps[0]]:
                            # Increment elim
                            elim += 1
                    # Update 'value' with number of times a choice was
                    # eliminated from 'vars' neighbor due to 'value' being
                    # used.
                    values[value] += elim

        # Use the dict values to sort each key
        sorted_values = {k: v for k, v in sorted(values.items(),
                         key=lambda item: item[1])}

        # We only want the keys in their desired order so convert keys to list
        sorted_list = list(sorted_values.keys())

        # Return the sorted list of values in ascending order
        return sorted_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Create a new dict of all var yet to be assigned
        unassigned = {k: self.domains[k] for
                      k in set(self.domains.keys()) - set(assignment.keys())}

        # Create another dict based on dict(unassigned) whose values are the
        # number of remaining values in its domain
        filtered = {k: len(v) for k, v in unassigned.items()}

        # Sort the dict of unassigned var based on number of remaining values
        sorted_values = {k: v for k, v in sorted(filtered.items(),
                         key=lambda item: item[1])}

        # Flipped technique from method 2 of https://www.geeksforgeeks.org/
        # python-find-keys-with-duplicate-values-in-dictionary/

        # FLip the dict so that the key is 'the remaining number of values'
        # described above and they values are the vars associated with that key
        flipped = {}

        # Loop through var and their counts
        for k, v in sorted_values.items():
            # Add counts as key and key as value
            if v not in flipped:
                flipped[v] = [k]
            else:
                flipped[v].append(k)

        # Get lowest count for values remaining in a var's domain
        fewest = list(flipped.keys())[0]

        # Check if there's a tie for fewest number of remaining values in domain
        if len(flipped[fewest]) != 1:

            # Create one final dict of remaining vars and determine which has
            # the most neighbors. Calling max() will return the first it finds
            # in the case of duplicates
            results = {var: len(self.crossword.neighbors(var)) for var
                       in flipped[fewest]}

            # Return chosen var
            return max(results, key=results.get)

        # If no tie
        else:
            # Return result with fewest number of remaining values in its domain
            return flipped[fewest][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # If assignement is complete
        if self.assignment_complete(assignment):
            # Return the completed assignment
            return assignment

        # Get an unassigned variable
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            # See if adding var with value is consistent
            if self.consistent(assignment):
                # If so, add to assignment
                assignment[var] = value
                result = self.backtrack(assignment)
                # If backtracking doesn't result in a failure
                if result != None:
                    # Return result
                    return result
                # If there was a failure, remove key from assignment
                assignment.pop(var, None)

        # No assignment is possible
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
