import logging
import sys
from itertools import permutations

from puzzle_input import puzzle_input
from IntcodeComputer import IntCodeComputer


def get_output(computer, instructions, thruster_sequence):
    current_output = 0
    for code in thruster_sequence:
        current_output = computer.compute(instructions, [code, current_output])

    return current_output


def main():
    computer = IntCodeComputer()
    input_sequences = list(permutations(range(5), 5))

    max_output = 0
    for seq in input_sequences:
        output = get_output(computer, puzzle_input, seq)
        if output > max_output:
            max_output = output

    print(max_output)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        stream=sys.stdout
    )
    main()
