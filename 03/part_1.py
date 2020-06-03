import puzzle_input


def parse_path(path):
    return [p.strip() for p in path.split(",") if p.strip()]


def track_path(path):
    north_south = 0
    east_west = 0

    nodes = [(east_west, north_south)]

    # make a full traversal graph so set-wise comparison can find common points
    for block in path:
        direction = block[0]
        for _ in range(int(block[1:])):
            if direction == "U":
                north_south += 1
            elif direction == "D":
                north_south -= 1
            elif direction == "R":
                east_west += 1
            elif direction == "L":
                east_west -= 1
            nodes.append((east_west, north_south))

    return nodes


def compute_manhattan(nodes):
    overlaps = []
    for east_west, north_south in nodes:
        # filter out starting point
        if east_west == 0 and north_south == 0:
            continue
        overlaps.append(abs(east_west) + abs(north_south))
    return min(overlaps)


path_1 = track_path(parse_path(puzzle_input.path_1))
path_2 = track_path(parse_path(puzzle_input.path_2))

overlap = compute_manhattan(set(path_1) & set(path_2))
print(overlap)

