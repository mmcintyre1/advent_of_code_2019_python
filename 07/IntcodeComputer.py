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

    def __init__(self, program_input: List[int], custom_inputs):
        """
        Takes a program input list of integers, as well as setting the
        current position as 0 and registering all opcode operations in an instance-
        variable process_tree.

        :param program_input: a list of integers or program instructions
        """
        self.program_input = program_input
        self.custom_inputs = custom_inputs
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

    def get_num(self, rel_position=1, nargs=1):
        """

        :param rel_position:
        :param nargs:
        :return:
        """

        nums = []
        for _ in range(nargs):
            mode = self.get_mode(rel_position)
            if mode == 0:
                nums.append(self.program_input[self.program_input[self.current_position]])
            else:
                nums.append(self.program_input[self.current_position])

            self.current_position += 1
            rel_position += 1

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
        first_num, second_num = self.get_num(rel_position=1, nargs=2)
        self.set_num(first_num + second_num, mode=self.get_mode(3))

    def multiply(self):
        first_num, second_num = self.get_num(rel_position=1, nargs=2)
        self.set_num(first_num * second_num, mode=self.get_mode(3))

    def get_input(self):
        num = self.custom_inputs.pop(0)
        LOG.info(f"Getting variable - {num} from custom inputs")
        self.set_num(num, mode=self.get_mode(1))

    def print_code(self):
        """Prints either using a log object is one has a handler added, or
        directly to the stdout via print()"""
        formatted_msg = f"Output: {self.get_num(rel_position=1)}"
        if not len(LOG.root.handlers):
            print(formatted_msg)
        else:
            LOG.info(formatted_msg)

    def jump(self):
        if self.current_op_code[0] == 5:
            check_phrase = self.get_num(rel_position=1) != 0
        else:
            check_phrase = self.get_num(rel_position=1) == 0

        if check_phrase:
            jump_position = self.get_num(rel_position=1)
            self.current_position = jump_position
        else:
            # skip processing if failed check
            self.current_position += 1

    def compare(self):
        first_num, second_num = self.get_num(rel_position=1, nargs=2)

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
            LOG.info(f"{self.current_position} - Executing op_code - {self.current_op_code}, "
                     f"raw_code - {self.program_input[self.current_position-1]}, "
                     f"function - {self.process_tree[self.current_op_code[0]].__name__}()")
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
    instructions = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1102, 68, 5, 225, 1101, 71, 12, 225, 1, 117, 166,
                    224, 1001, 224, -100, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1001, 66,
                    36, 224, 101, -87, 224, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1101, 26,
                    51, 225, 1102, 11, 61, 224, 1001, 224, -671, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1,
                    223, 224, 223, 1101, 59, 77, 224, 101, -136, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 1, 224,
                    1, 223, 224, 223, 1101, 11, 36, 225, 1102, 31, 16, 225, 102, 24, 217, 224, 1001, 224, -1656, 224, 4,
                    224, 102, 8, 223, 223, 1001, 224, 1, 224, 1, 224, 223, 223, 101, 60, 169, 224, 1001, 224, -147, 224,
                    4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1102, 38, 69, 225, 1101, 87, 42, 225,
                    2, 17, 14, 224, 101, -355, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 2, 224, 1, 224, 223, 223,
                    1002, 113, 89, 224, 101, -979, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 7, 224, 1, 224, 223,
                    223, 1102, 69, 59, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999,
                    1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999,
                    1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1,
                    99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999,
                    1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 7, 677, 677, 224, 1002, 223, 2, 223,
                    1006, 224, 329, 1001, 223, 1, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 344, 1001,
                    223, 1, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 359, 1001, 223, 1, 223, 1107, 226,
                    677, 224, 1002, 223, 2, 223, 1006, 224, 374, 101, 1, 223, 223, 1107, 677, 226, 224, 1002, 223, 2,
                    223, 1006, 224, 389, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 404, 101, 1,
                    223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 419, 101, 1, 223, 223, 1008, 226, 226,
                    224, 102, 2, 223, 223, 1006, 224, 434, 101, 1, 223, 223, 107, 226, 226, 224, 1002, 223, 2, 223,
                    1005, 224, 449, 1001, 223, 1, 223, 108, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 464, 101, 1,
                    223, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 479, 101, 1, 223, 223, 1007, 226, 677,
                    224, 102, 2, 223, 223, 1006, 224, 494, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2, 223, 223, 1005,
                    224, 509, 101, 1, 223, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 524, 1001, 223, 1, 223,
                    8, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 539, 101, 1, 223, 223, 107, 677, 226, 224, 102, 2,
                    223, 223, 1005, 224, 554, 1001, 223, 1, 223, 8, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 569,
                    1001, 223, 1, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 584, 1001, 223, 1, 223, 1108,
                    226, 226, 224, 102, 2, 223, 223, 1005, 224, 599, 1001, 223, 1, 223, 1107, 677, 677, 224, 1002, 223,
                    2, 223, 1006, 224, 614, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 629,
                    1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 644, 1001, 223, 1, 223, 8, 677,
                    226, 224, 1002, 223, 2, 223, 1005, 224, 659, 1001, 223, 1, 223, 1008, 677, 677, 224, 1002, 223, 2,
                    223, 1006, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]
    computer = IntCodeComputer(instructions, [1])
    computer.compute()
