"""Make Sudoku puzzles: fill a complete 9 x 9 grid, then empty some squares. Fewer clues = harder."""
import random

# How many of the 81 numbers stay visible in each mode.
MODES = {"beginner": 42, "medium": 34, "hard": 27}


def full_grid():
    """Return a complete, valid grid (9 rows of 9 numbers), filled in a random order."""
    grid = [[0] * 9 for _ in range(9)]

    def allowed(row, col, number):
        if number in grid[row]:                                   # already in this row
            return False
        if any(grid[r][col] == number for r in range(9)):         # already in this column
            return False
        top, left = 3 * (row // 3), 3 * (col // 3)                # already in this 3 x 3 box
        return all(grid[r][c] != number for r in range(top, top + 3) for c in range(left, left + 3))

    def fill(cell=0):
        if cell == 81:
            return True
        row, col = divmod(cell, 9)
        for number in random.sample(range(1, 10), 9):
            if allowed(row, col, number):
                grid[row][col] = number
                if fill(cell + 1):
                    return True
                grid[row][col] = 0
        return False

    fill()
    return grid


def new_puzzle(mode):
    """A puzzle for the mode: a full grid with some squares set to 0, which means empty.

    A puzzle can have more than one solution, so the game accepts any grid that follows the rules.
    """
    grid = full_grid()
    for cell in random.sample(range(81), 81 - MODES[mode]):
        row, col = divmod(cell, 9)
        grid[row][col] = 0
    return grid
