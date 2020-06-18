import copy
from functools import reduce
from itertools import combinations
from math import gcd

from part_1 import Moon


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


def loop_until_repeat(m, attr):
    moons = copy.deepcopy(m)
    steps = 1
    states = set()

    while True:
        states.add(get_axis(moons, attr))

        for moon_group in combinations(moons, 2):
            moon_group[0].compare(moon_group[1])

        for moon in moons:
            moon.move()

        current_pos = get_axis(moons, attr)
        if current_pos in states:
            return steps
        else:
            steps += 1


def get_axis(moons, axis):
    return tuple((getattr(moon.position, axis), getattr(moon.velocity, axis)) for moon in moons)


def main():
    test_moons_a = [
        Moon(-8, -10, 0),
        Moon(5, 5, 10),
        Moon(2, -7, 3),
        Moon(9, -8, -3)
    ]

    test_moons_b = [
        Moon(-1, 0, 2),
        Moon(2, -10, -7),
        Moon(4, -8, 8),
        Moon(3, 5, -1)
    ]

    moons = [
        Moon(13, -13, -2),
        Moon(16, 2, -15),
        Moon(7, -18, -12),
        Moon(-3, -8, -8)
    ]
    states = []

    for a in ('x', 'y', 'z'):
        states.append(loop_until_repeat(moons, a))
    print(lcm(states))


if __name__ == '__main__':
    main()
