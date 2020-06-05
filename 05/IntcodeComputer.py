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
            4: self.print
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
        # num = int(input("What is your input?"))
        self.set_num(1, mode=0)

    def print(self):
        print(self.get_num(mode=0))


if __name__ == '__main__':
    puzzle_input = pathlib.Path('./puzzle_input.txt')
    instructions = [int(item.strip()) for item in puzzle_input.read_text().split(",") if item.strip()]
    computer = IntCodeComputer(instructions)
    computer.compute()
