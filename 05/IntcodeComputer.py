import operator
import pathlib


class IntCodeComputer:
    def __init__(self, program_input):
        self.program_input = program_input
        self.current_position = 0
        self.current_op_code = None

        self.process_tree = {
            1: self.add,
            2: self.multiply,
            3: self.get_input,
            4: self.print,
            5: self.jump,
            6: self.jump,
            7: self.compare,
            8: self.compare
        }

    def get_num(self, mode=0):
        if mode == 0:
            num = self.program_input[self.program_input[self.current_position]]
        else:
            num = self.program_input[self.current_position]

        self.current_position += 1

        return num

    def set_num(self, num, mode=0):
        if mode == 0:
            self.program_input[self.program_input[self.current_position]] = num
        else:
            self.program_input[self.current_position] = num

        self.current_position += 1

    def set_op_code(self):
        filled_op_code = str(self.program_input[self.current_position]).zfill(5)
        self.current_op_code = [int(c) for c in filled_op_code[0:-2]] + [int(filled_op_code[-1])]
        self.current_position += 1

    def compute(self):
        while self.program_input[self.current_position] != 99:
            self.set_op_code()
            self.process_tree[self.current_op_code[-1]]()

    def add(self):
        first_num = self.get_num(mode=self.current_op_code[-2])
        second_num = self.get_num(mode=self.current_op_code[-3])
        self.set_num(first_num + second_num, mode=self.current_op_code[-4])

    def multiply(self):
        first_num = self.get_num(mode=self.current_op_code[-2])
        second_num = self.get_num(mode=self.current_op_code[-3])
        self.set_num(first_num * second_num, mode=self.current_op_code[-4])

    def get_input(self):
        num = int(input("What is your input?"))
        self.set_num(num, mode=self.current_op_code[-2])

    def print(self):
        print(self.get_num(mode=self.current_op_code[-2]))

    def jump(self):
        if self.current_op_code[-1] == 5:
            check_phrase = self.get_num(mode=self.current_op_code[-2]) != 0
        else:
            check_phrase = self.get_num(mode=self.current_op_code[-2]) == 0

        if check_phrase:
            jump_position = self.get_num(mode=self.current_op_code[-3])
            self.current_position = jump_position
        else:
            # skip processing if failed check
            self.current_position += 1

    def compare(self):
        first_num = self.get_num(mode=self.current_op_code[-2])
        second_num = self.get_num(mode=self.current_op_code[-3])

        if self.current_op_code[-1] == 7:
            op = operator.lt
        else:
            op = operator.eq

        if op(first_num, second_num):
            self.set_num(1, mode=self.current_op_code[-4])
        else:
            self.set_num(0, mode=self.current_op_code[-4])


if __name__ == '__main__':
    puzzle_input = pathlib.Path('./puzzle_input.txt')
    instructions = [int(item.strip()) for item in puzzle_input.read_text().split(",") if item.strip()]
    # instructions = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #                 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #                 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    computer = IntCodeComputer(instructions)
    computer.compute()
