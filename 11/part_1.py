from Computer import IntCodeComputer
from puzzle_input import puzzle_input

computer = IntCodeComputer(puzzle_input)

current_position = (0, 0)
visited_positions = {}

instruction = 0
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
current_direction = 0

while not computer.done:
    color = computer.compute(custom_input=instruction, return_on_output=True)
    direction = computer.compute(return_on_output=True)

    if direction == 0:
        adder = -1
    else:
        adder = 1

    current_direction = (current_direction + adder) % 4
    current_position = tuple(sum(x) for x in zip(current_position, directions[current_direction]))
    visited_positions[current_position] = color

    instruction = color

print(visited_positions)


