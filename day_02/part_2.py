import operator

from puzzle_input import puzzle_input

opcodes = {
    1: operator.add,
    2: operator.mul
}


def process(program, noun, verb):
    program[1] = noun
    program[2] = verb

    for idx, opcode in enumerate(program[::4]):
        if opcode == 99:
            break
        program[program[3 + (idx * 4)]] = opcodes[opcode](program[program[1 + (idx * 4)]],
                                                          program[program[2 + (idx * 4)]])

    return program[0]


for noun in range(100):
    for verb in range(100):
        try:
            value = process(puzzle_input.copy(), noun, verb)
            if value == 19690720:
                print(100 * noun + verb)
        except KeyError:
            pass
