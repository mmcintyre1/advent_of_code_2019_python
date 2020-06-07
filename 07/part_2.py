from itertools import permutations
import logging
import sys

from puzzle_input import puzzle_input
from IntcodeComputer import IntCodeComputer


def main():
    input_sequences = list(permutations(range(5, 10), 5))
    all_outputs = []
    instructions = puzzle_input
    for seq in input_sequences:
        print(f"operating on {seq}")

        computers = [IntCodeComputer(instructions[:]) for _ in range(5)]
        for computer, setting in zip(computers, seq):
            computer.custom_inputs.append(setting)

        output = 0
        while not computers[-1].done:
            for computer in computers:
                output = computer.compute(output, return_on_output=True)

        all_outputs.append(output)

    print(max(all_outputs))


if __name__ == '__main__':
    # logging.basicConfig(
    #     format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     level=logging.INFO,
    #     stream=sys.stdout
    # )
    main()
