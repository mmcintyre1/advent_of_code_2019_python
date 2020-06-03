import operator

from puzzle_input import puzzle_input

opcodes = {
    1: operator.add,
    2: operator.mul
}

puzzle_input[1] = 12
puzzle_input[2] = 2

for idx, opcode in enumerate(puzzle_input[::4]):
    if opcode == 99:
        break
    puzzle_input[puzzle_input[3 + (idx * 4)]] = opcodes[opcode](puzzle_input[puzzle_input[1 + (idx * 4)]],
                                                                puzzle_input[puzzle_input[2 + (idx * 4)]])

print(puzzle_input)
