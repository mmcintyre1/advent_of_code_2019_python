from puzzle_input import parsed_puzzle_input


def get_fuel_consumption(mass, total):
    needed_fuel = mass // 3 - 2

    if needed_fuel > 0:
        total.append(needed_fuel)
        get_fuel_consumption(needed_fuel, total)

    return sum(total)


print(sum([get_fuel_consumption(mass, []) for mass in parsed_puzzle_input]))




