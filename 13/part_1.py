from Computer import IntCodeComputer
from helper import chunk
from puzzle_input import instructions


class Ball:
    def __init__(self, starting_position, trajectory):
        self.x, self.y = starting_position
        self.trajectory = trajectory
        self.in_play = True

    def move(self):
        self.x, self.y = tuple(sum(x) for x in zip((self.x, self.y), self.trajectory))

    def reverse(self, x=True, y=True):
        if x:
            self.trajectory[0] = -self.trajectory[0]
        if y:
            self.trajectory[1] = -self.trajectory[1]


class BreakoutGame:
    tiles = {
        0: " ",
        1: "|",
        2: "$",
        3: "-",
        4: "*"
    }

    def __init__(self, computer):
        self.graph_instructions = []
        self.starting_position = None
        self.parse_instructions(computer)

        self.trajectory = (-1, 1)

        self.max_x = max(x[0] for x in self.graph_instructions)
        self.max_y = max(x[1] for x in self.graph_instructions)

        self.ball = Ball(self.starting_position, self.trajectory)
        self.draw_board()

    def parse_instructions(self, computer):
        for x, y, tile in chunk(computer.compute(return_on_output=True), 3):
            if tile == 4:
                self.starting_position = x, y
            self.graph_instructions.append((x, y, tile))

    def draw_board(self):
        self.board = [["" for _ in range(self.max_x + 1)] for _ in range(self.max_y + 1)]

        for inst in self.graph_instructions:
            x, y, tile = inst
            self.board[y][x] = self.tiles[tile]

        for row in self.board:
            print(''.join(row))

    def play(self):
        while self.ball.in_play:
            current_tile = self.board[self.ball.y][self.ball.x][-1]
            print(self.ball.x, self.ball.y)

            if self.ball.y == self.max_y:
                self.ball.in_play = False

            if current_tile in ("|", "$", "-") and self.ball.y != 0:
                if current_tile == "$":
                    self.board[self.ball.x][self.ball.y] = ""
                self.ball.reverse()

            elif current_tile == "|" and self.ball.y == 0:
                self.ball.reverse(x=False)

            self.ball.move()


def main():
    computer = IntCodeComputer(instructions)
    breakout = BreakoutGame(computer)
    total = 0
    for row in breakout.board:
        total += sum(1 for x in row if x == "$")




if __name__ == '__main__':
    main()
