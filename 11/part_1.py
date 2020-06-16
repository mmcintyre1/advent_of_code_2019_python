import typing

from Computer import IntCodeComputer
from puzzle_input import puzzle_input


class HullPainting:

    visited_positions: typing.Dict[typing.Tuple[int, int], int] = {}
    directions: typing.List[typing.Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, computer: IntCodeComputer):
        self.computer = computer
        self.current_instruction: int = 0
        self.current_direction: int = 0
        self.current_position: tuple = (0, 0)

    def change_direction(self, new_direction):
        """Changes current direction, using modulo to make sure things stay within the directional bounds."""
        if new_direction == 0:
            adder = -1
        else:
            adder = 1

        self.current_direction = (self.current_direction + adder) % 4

    def walk(self):
        """Increments current position by one based on current direction."""
        self.current_position = tuple(
            sum(x) for x in zip(self.current_position, self.directions[self.current_direction])
        )

    def paint(self):
        while not self.computer.done:
            color = self.visited_positions[self.current_position] if self.current_position in self.visited_positions else 0
            self.visited_positions[self.current_position] = self.computer.compute(custom_input=color, return_on_output=True)
            self.change_direction(self.computer.compute(return_on_output=True))
            self.walk()


def main():
    computer = IntCodeComputer(puzzle_input)
    painting = HullPainting(computer)
    painting.paint()
    print(len(painting.visited_positions))


if __name__ == '__main__':
    main()


