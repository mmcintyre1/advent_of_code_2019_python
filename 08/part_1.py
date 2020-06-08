from itertools import islice
from typing import List

from puzzle_input import puzzle_input


def chunk(it, size):
    """Creates an iterator from a passed in iterable and builds n-sized tuples as a return."""
    it = iter(it)
    return iter(lambda: list(islice(it, size)), [])


def interpolate(input_str: str, height: int = 0, width: int = 0) -> List:
    input_ints = [int(num.strip()) for num in input_str if num.strip()]
    blocks_per_layer = height * width

    reshaped = []
    for c in chunk(input_ints, blocks_per_layer):
        reshaped.append(c)

    return reshaped


def sort_by(to_sort, sort_criteria=0):
    to_sort.sort(key=lambda x: x.count(sort_criteria))


def ones_and_twos(sorted_list):
    ones = sorted_list[0].count(1)
    twos = sorted_list[0].count(2)
    return ones * twos


if __name__ == '__main__':
    print(len(str(puzzle_input[0])))
    interpolated = interpolate(str(puzzle_input[0]), height=6, width=25)
    sort_by(interpolated)
    print(ones_and_twos(interpolated))
