from Computer import IntCodeComputer
from puzzle_input import instructions
from helper import chunk

TILES = {
    0: "empty",
    1: "wall",
    2: "block",
    3: "horizontal_paddle",
    4: "ball"
}


def main():
    computer = IntCodeComputer(instructions)
    for x, y, tile in chunk(computer.compute(return_on_output=True), 3):
        print(x, y, TILES[tile])


if __name__ == '__main__':
    main()