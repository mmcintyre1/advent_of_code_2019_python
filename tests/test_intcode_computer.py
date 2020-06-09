import pytest

from Computer import IntCodeComputer as Computer


@pytest.mark.parametrize(
    "test_input,expected", [
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99])
    ]
)
def test_add_and_multiply(test_input, expected):
    computer = Computer(test_input)
    computer.compute()
    assert computer.memory == expected


@pytest.mark.parametrize(
    "test_input,expected", [
        (8, 1),
        (9, 0),
        (100, 0),
        (2, 0)
    ]
)
def test_input(test_input, expected):
    computer = Computer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    assert computer.compute(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected", [
        (8, 1000),
        (9, 1001),
        (10, 1001),
        (100, 1001),
        (2, 999),
        (0, 999)
    ]
)
def test_larger_input(test_input, expected):
    computer = Computer([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                         1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                         999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])

    assert computer.compute(test_input) == expected
