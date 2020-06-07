import logging
import operator
import pathlib
import sys
from typing import List


LOG = logging.getLogger(__name__)


class IntCodeComputer:
    """
    A class to process program instructions. An opcode is parsed from the current
    instruction, and then values are gathered from the subsequent argument parameters,
    so a chain like 1, 15, 16, 30 would add the numbers at index 15 and index 16 together
    and store the result at index 30.

    There are two main operating methods called immediate mode and position mode that are
    optional parameters as part of the opcode.  1 is for immediate mode and 0 is for position mode.
    Immediate mode makes the subsequent parameter literal, as in, not an index, while position mode
    takes the argument as an index.  For example, in the above example, if we change it to 01001, 15, 16, 30,
    this is opcode - 1, first parameter - immediate mode, second position, and third immediate.  The opcode
    is evaluated left to right.
    """

    def __init__(self, program_input: List[int]):
        """
        Takes a program input list of integers, as well as setting the
        current position as 0 and registering all opcode operations in an instance-
        variable process_tree.

        :param program_input: a list of integers or program instructions
        """
        self.program_input = program_input
        self.current_position = 0
        self.current_op_code = None

        self.process_tree = {
            1: self.add,
            2: self.multiply,
            3: self.get_input,
            4: self.print_code,
            5: self.jump,
            6: self.jump,
            7: self.compare,
            8: self.compare
        }

    def get_num(self, mode=0, nargs=1):
        """

        :param mode:
        :param nargs:
        :return:
        """
        nums = []
        for arg in range(nargs):
            if mode == 0:
                nums.append(self.program_input[self.program_input[self.current_position]])
            else:
                nums.append(self.program_input[self.current_position])

            self.current_position += 1
            mode = self.get_mode(mode + 1)

        if nargs == 1:
            return nums[0]

        return nums

    def set_num(self, num, mode=0):
        if mode == 0:
            self.program_input[self.program_input[self.current_position]] = num
        else:
            self.program_input[self.current_position] = num

        self.current_position += 1

    def set_op_code(self):
        """
        Reverses the string to be read left or right, then populates a list of op code instructions
        and increments the current position
        :return:
        """
        filled_op_code = "".join(reversed(str(self.program_input[self.current_position])))
        self.current_op_code = [int(filled_op_code[0])] + [int(c) for c in filled_op_code[2:]]
        self.current_position += 1

    def get_mode(self, arg_position=1):
        try:
            return self.current_op_code[arg_position]
        except IndexError:
            return 0

    def add(self):
        first_num, second_num = self.get_num(mode=self.get_mode(1), nargs=2)
        self.set_num(first_num + second_num, mode=self.get_mode(3))

    def multiply(self):
        first_num, second_num = self.get_num(mode=self.get_mode(1), nargs=2)
        self.set_num(first_num * second_num, mode=self.get_mode(3))

    def get_input(self):
        num = int(input("What is your input?"))
        self.set_num(num, mode=self.get_mode(1))

    def print_code(self):
        LOG.info(f"Output: {self.get_num(mode=self.get_mode(1))}")

    def jump(self):
        if self.current_op_code[0] == 5:
            check_phrase = self.get_num(mode=self.get_mode(1)) != 0
        else:
            check_phrase = self.get_num(mode=self.get_mode(1)) == 0

        if check_phrase:
            jump_position = self.get_num(mode=self.get_mode(2))
            self.current_position = jump_position
        else:
            # skip processing if failed check
            self.current_position += 1

    def compare(self):
        first_num, second_num = self.get_num(mode=self.get_mode(1), nargs=2)

        if self.current_op_code[0] == 7:
            op = operator.lt
        else:
            op = operator.eq

        if op(first_num, second_num):
            self.set_num(1, mode=self.get_mode(3))
        else:
            self.set_num(0, mode=self.get_mode(3))

    def compute(self):
        while self.program_input[self.current_position] != 99:
            LOG.info(f"{self.current_position} - Operating on new instructions.")
            self.set_op_code()
            LOG.info(f"{self.current_position} - Executing op_code - {self.current_op_code}")
            self.process_tree[self.current_op_code[0]]()

        LOG.info(f"Terminating program on line {self.current_position}, "
                 f"previous op_code {self.current_op_code[0]}, "
                 f"current op_code {self.program_input[self.current_position]}")


if __name__ == '__main__':
    logging.basicConfig(
        format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        stream=sys.stdout
    )
    puzzle_input = pathlib.Path('./puzzle_input.txt')
    # instructions = [int(item.strip()) for item in puzzle_input.read_text().split(",") if item.strip()]
    instructions = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                    1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                    999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    computer = IntCodeComputer(instructions)
    computer.compute()
