from itertools import combinations
from functools import reduce
from math import gcd

from part_1 import Moon


def lcm(denominators):
    return reduce(lambda a, b: a * b // gcd(a, b), denominators)


def loop_until_repeat(moons, attr):
    steps = 0
    while True:

        for moon_group in combinations(moons, 2):
            moon_group[0].compare(moon_group[1])

        for moon in moons:
            moon.move()

        for moon in moons:
            if getattr(moon.initial_position, attr) == getattr(moon.position, attr) and getattr(moon.initial_velocity, attr) == getattr(moon.initial_velocity, attr):
                continue
            else:
                steps += 1
                break

        return steps


def main():
    io = Moon(-1, 0, 2)
    europa = Moon(2, -10, -7)
    ganymede = Moon(4, -8, 8)
    callisto = Moon(3, 5, -1)

    moons = [io, europa, ganymede, callisto]
    states = []

    for a in ('x', 'y', 'z'):
        states.append(loop_until_repeat(moons.copy(), a))

    print(states)


if __name__ == '__main__':
    main()

