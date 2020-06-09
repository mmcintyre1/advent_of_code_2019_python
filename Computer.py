import logging
import operator
import sys

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

    def __init__(self, program_input):
        self.memory = program_input
        self.custom_inputs = []
        self.current_position = 0
        self.relative_position = 0
        self.current_op_code = None
        self.current_argument_indexes = None
        self.current_arguments = None
        self.current_output = None
        self.done = False

        self.process_tree = {
            1: (self.add, 3),
            2: (self.multiply, 3),
            3: (self.get_input, 1),
            4: (self.print_code, 1),
            5: (self.jump, 2),
            6: (self.jump, 2),
            7: (self.compare, 3),
            8: (self.compare, 3),
            9: (self.adjust, 1),
            99: (self.kill, 0)
        }

        self.modes = {
            0: ("P", "POSITION"),
            1: ("I", "IMMEDIATE"),
            2: ("R", "RELATIVE")
        }

    def __index_retriever(self, mode):
        if mode == 0:
            num = self.memory[self.current_position]
        elif mode == 1:
            num = self.current_position
        elif mode == 2:
            num = self.relative_position + self.memory[self.current_position]
        else:
            raise ValueError('opcode mode not found.')

        return num, self.modes[mode][0]

    def __setter(self, index, num):
        try:
            self.memory[index] = num
        except IndexError:
            padding = [0] * (index - len(self.memory))
            self.memory = self.memory + padding + [num]

    def _set_args(self):
        self.current_arguments = []
        self.current_argument_indexes = []
        num_of_args = self.process_tree[self.current_op_code[0]][-1]

        # make sure the arguments start at one in order to get mode from opcode properly
        for position in range(1, num_of_args + 1):
            num_index, mode = self._get_num_index(position)
            self.current_argument_indexes.append(num_index)
            self.current_arguments.append((mode, self._get_num(num_index)))

    def _get_num_index(self, rel_position):
        mode = self.get_mode(rel_position)
        num = self.__index_retriever(mode)
        self.current_position += 1
        return num

    def _get_num(self, index):
        try:
            return self.memory[index]
        except IndexError:
            padding = [0] * (index - len(self.memory) + 1)
            self.memory = self.memory + padding
        return self.memory[index]

    def _set_num(self, index, num):
        self.__setter(index, num)

    def _set_op_code(self):
        params = [int(c) for c in str(self.memory[self.current_position])[-3::-1]]
        opcode = [int(str(self.memory[self.current_position])[-2:])]

        self.current_op_code = opcode + params

        self.current_position += 1

    def get_mode(self, arg_position=1):
        try:
            return self.current_op_code[arg_position]
        except IndexError:
            return 0

    def add(self):
        first_idx, second_idx, dest_index = self.current_argument_indexes
        self._set_num(dest_index, self._get_num(first_idx) + self._get_num(second_idx))

    def multiply(self):
        first_idx, second_idx, dest_index = self.current_argument_indexes
        self._set_num(dest_index, self._get_num(first_idx) * self._get_num(second_idx))

    def get_input(self):
        num = self.custom_inputs.pop(0)
        LOG.info(f"Getting variable - {num} from custom inputs")
        self._set_num(self.current_argument_indexes[0], num)

    def print_code(self):
        """Prints either using a log object is one has a handler added, or
        directly to the stdout via print()"""
        self.current_output = self._get_num(self.current_argument_indexes[0])
        formatted_msg = f"Output: {self.current_output}"
        if not len(LOG.root.handlers):
            print(formatted_msg)
        else:
            LOG.info(formatted_msg)

        return self.current_output

    def jump(self):
        if self.current_op_code[0] == 5:
            check_phrase = self._get_num(self.current_argument_indexes[0]) != 0
        else:
            check_phrase = self._get_num(self.current_argument_indexes[0]) == 0

        if check_phrase:
            self.current_position = self._get_num(self.current_argument_indexes[1])

    def compare(self):
        first_idx, second_idx, dest_index = self.current_argument_indexes

        if self.current_op_code[0] == 7:
            op = operator.lt
        else:
            op = operator.eq

        if op(self._get_num(first_idx), self._get_num(second_idx)):
            self._set_num(dest_index, 1)
        else:
            self._set_num(dest_index, 0)

    def adjust(self):
        adjustment = self._get_num(self.current_argument_indexes[0])
        self.relative_position += adjustment

    def kill(self):
        LOG.info(f"Terminating program on line {self.current_position}, "
                 f"previous op_code {self.current_op_code[0]}, "
                 f"current_output: {self.current_output}")

        LOG.info(f"Current memory: {self.memory}")

        self.done = True

    def _print_current_log(self):
        LOG.info(f"{self.current_position} - Executing op_code - {self.current_op_code}, "
                 f"function - {self.process_tree[self.current_op_code[0]][0].__name__}(), "
                 f"argument_indexes - {self.current_argument_indexes}, "
                 f"arguments - {self.current_arguments}")

    def compute(self, custom_input=None, return_on_output=False):

        if custom_input is not None:
            self.custom_inputs.append(custom_input)

        while not self.done:
            self._set_op_code()
            self._set_args()
            self._print_current_log()
            self.process_tree[self.current_op_code[0]][0]()

            if return_on_output and self.current_op_code[0] == 4:
                return self.current_output

        return self.current_output

    def reset(self):
        self.current_position = 0
        self.current_output = 0
        self.relative_position = 0


if __name__ == '__main__':
    logging.basicConfig(
        format="%(filename)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        stream=sys.stdout
    )

    computer = IntCodeComputer([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])
    computer.compute()
