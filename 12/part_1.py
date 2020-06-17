from __future__ import annotations

from itertools import combinations

# test comment
class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"x={self.x}, y={self.y}, z={self.z}"

    def __add__(self, other: Vector) -> Vector:
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return Vector(x, y, z)


class Moon:
    def __init__(self, x: int, y: int, z: int):
        self.position: Vector = Vector(x, y, z)
        self.velocity: Vector = Vector(0, 0, 0)

        self.initial_position = Vector(x, y, z)
        self.initial_velocity = Vector(0, 0, 0)

    def move(self):
        self.position += self.velocity

    def add_one(self, attr: str):
        current_count = getattr(self.velocity, attr)
        setattr(self.velocity, attr, current_count + 1)

    def minus_one(self, attr: str):
        current_count = getattr(self.velocity, attr)
        setattr(self.velocity, attr, current_count - 1)

    def compare(self, other: Moon):
        for attr in ('x', 'y', 'z'):
            if getattr(self.position, attr) == getattr(other.position, attr):
                pass
            else:
                if getattr(self.position, attr) < getattr(other.position, attr):
                    self.add_one(attr)
                    other.minus_one(attr)
                else:
                    self.minus_one(attr)
                    other.add_one(attr)

    def get_kinetic_energy(self) -> int:
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    def get_potential_energy(self) -> int:
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    def get_total_energy(self) -> int:
        return self.get_kinetic_energy() * self.get_potential_energy()


if __name__ == "__main__":
    io = Moon(13, -13, -2)
    europa = Moon(16, 2, -15)
    ganymede = Moon(7, -18, -12)
    callisto = Moon(-3, -8, -8)

    moons = [io, europa, ganymede, callisto]

    for _ in range(1000000000):
        for moon_group in combinations(moons, 2):
            moon_group[0].compare(moon_group[1])

        for moon in moons:
            moon.move()

    total_energy = 0
    for moon in moons:
        total_energy += moon.get_total_energy()

    print(total_energy)
