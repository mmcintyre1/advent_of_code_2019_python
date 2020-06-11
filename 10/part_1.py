from itertools import islice
from typing import List, Iterable, Any


def chunk(it: Iterable, size: int) -> Iterable:
    """Creates an iterator from a passed in iterable and builds n-sized tuples as a return."""
    it = iter(it)
    return iter(lambda: list(islice(it, size)), [])


class Grid:
    grid = []

    def __init__(self, raw_input: List, ncols: int = 0) -> None:
        self.make_grid(raw_input, ncols)

    def __str__(self):
        return '\n'.join([''.join(['{:3}'.format(item) for item in row])
                          for row in self.grid])

    def make_grid(self, i: List, ncols: int) -> None:
        for row in chunk(i, ncols):
            self.grid.append(row)

    def get(self, x: int, y: int) -> Any:
        return self.grid[x][y]


def main():
    test_input = """
    #.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c
    """
    row_length = len(test_input.split()[0])
    parsed = [x.strip() for x in list(test_input) if x.strip()]

    grid = Grid(parsed, row_length)
    print(grid)


if __name__ == '__main__':
    main()
