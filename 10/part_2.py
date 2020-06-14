from part_1 import AsteroidBelt
from puzzle_input import puzzle_input


def main():
    row_length = len(puzzle_input.split()[0])
    parsed = [x.strip() for x in list(puzzle_input) if x.strip()]

    grid = AsteroidBelt(parsed, row_length)
    matching_node, max_visible_asteroids = grid.get_visible()

    angles = sorted(
        ((grid.get_angle(matching_node, end), end) for end in grid.asteroids),
        key=lambda x: (x[0], abs(matching_node.x - x[1].x) + abs(matching_node.y - x[1].y))
    )

    idx = 0
    last = angles.pop(idx)
    last_angle = last[0]
    cnt = 1

    while cnt < 200 and angles:
        if idx >= len(angles):
            idx = 0
            last_angle = None
        if last_angle == angles[idx][0]:
            idx += 1
            continue
        last = angles.pop(idx)
        last_angle = last[0]
        cnt += 1
    print('vaporized {}: {} {}'.format(cnt, last[1], last[1].x * 100 + last[1].y))


if __name__ == '__main__':
    main()
