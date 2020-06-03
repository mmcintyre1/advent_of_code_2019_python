import puzzle_input
import part_1


if __name__ == '__main__':
    path_1 = part_1.track_path(part_1.parse_path(puzzle_input.path_1))
    path_2 = part_1.track_path(part_1.parse_path(puzzle_input.path_2))

    overlap = set(path_1) & set(path_2)

    steps_group = []
    for grouping in overlap:
        path_1_steps = list(path_1).index(grouping)
        path_2_steps = list(path_2).index(grouping)
        steps_group.append(path_1_steps + path_2_steps)

    print(min(s for s in steps_group if s != 0))


