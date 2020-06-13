from dataclasses import dataclass
from itertools import islice
import math
from typing import List, Iterable, Any

from puzzle_input import puzzle_input


def chunk(it: Iterable, size: int) -> Iterable:
    """Creates an iterator from a passed in iterable and builds n-sized tuples as a return."""
    it = iter(it)
    return iter(lambda: list(islice(it, size)), [])


@dataclass
class Node:
    x: int
    y: int


def get_angle(start: Node, end: Node):
    """Calculates the angle between two sets of x, y coordinates."""
    result = math.atan2(end.x - start.x, start.y - end.y) * 180 / math.pi
    if result < 0:
        return 360 + result
    return result


class AsteroidBelt:
    grid = []

    def __init__(self, raw_input: List, ncols: int = 0) -> None:
        self.make_grid(raw_input, ncols)
        self.asteroids = []

        self.find_asteroids()

    def __str__(self):
        return '\n'.join([''.join(['{:3}'.format(item) for item in row])
                          for row in self.grid])

    def make_grid(self, i: List, ncols: int) -> None:
        for row in chunk(i, ncols):
            self.grid.append(row)

    def get(self, x: int, y: int) -> Any:
        return self.grid[x][y]

    def find_asteroids(self):
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                if node == "#":
                    self.asteroids.append(Node(x=x, y=y))

    def get_visible(self, ):
        """Iterates through all asteroids in two loops, comparing one location to all other
        locations, and creates a set of angles computed.  Since two Nodes will be 'inline' if
        they share the same angle, the set will filter out asteroids 'behind' other asteroids."""
        matching_node = None
        max_visible = 0
        for start_asteroid in self.asteroids:
            current_count = len(
                {get_angle(start_asteroid, end_asteroid) for end_asteroid in self.asteroids if
                 start_asteroid != end_asteroid}
            )
            if current_count > max_visible:
                max_visible = current_count
                matching_node = start_asteroid

        return matching_node, max_visible


def main():
    row_length = len(puzzle_input.split()[0])
    parsed = [x.strip() for x in list(puzzle_input) if x.strip()]

    grid = AsteroidBelt(parsed, row_length)
    matching_node, max_visible_asteroids = grid.get_visible()
    print(matching_node, max_visible_asteroids)


if __name__ == '__main__':
    main()
