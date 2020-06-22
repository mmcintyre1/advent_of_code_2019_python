from Computer import IntCodeComputer
from helper import chunk
from puzzle_input import instructions


def part_1():
    computer = IntCodeComputer(instructions)
    total = sum(1 for _, _, tile in chunk(computer.compute(return_on_output=True), 3) if tile == 2)
    return total


def part_2():
    ball_x = paddle_x = None
    computer = IntCodeComputer(instructions, lambda: (ball_x > paddle_x) - (ball_x < paddle_x))
    computer.memory[0] = 2

    points = 0
    while not computer.done:
        for x, y, tile in chunk(computer.compute(return_on_output=True), 3):
            paddle_x = x if tile == 3 else paddle_x
            ball_x = x if tile == 4 else ball_x
            points = tile if (x, y) == (-1, 0) else points
        return points


def main():
    print(f"Part 1: {part_1()}")
    print(f"Part 2: {part_2()}")


if __name__ == '__main__':
    main()
