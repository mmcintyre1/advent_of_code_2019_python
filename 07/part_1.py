import logging
import sys
from itertools import permutations

from IntcodeComputer import IntCodeComputer
from puzzle_input import puzzle_input


def main():
    input_sequences = list(permutations(range(5), 5))

    max_output = 0
    for seq in input_sequences:
        # setup of classes
        computers = [IntCodeComputer(puzzle_input[:]) for _ in range(5)]
        for computer, setting in zip(computers, seq):
            computer.custom_inputs.append(setting)

        # compute outputs
        output = 0
        for computer in computers:
            output = computer.compute(output)

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
