from Computer import IntCodeComputer as Computer
from puzzle_input import puzzle_input


if __name__ == '__main__':
    computer = Computer(puzzle_input)
    computer.compute(1)