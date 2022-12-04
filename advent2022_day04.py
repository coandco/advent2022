from typing import Tuple, Set
from utils import read_data
import re

DIGITS = re.compile(r'\d+')


def line_to_sets(line: str) -> Tuple[Set, Set]:
    first_low, first_high, second_low, second_high = (int(x) for x in DIGITS.findall(line))
    return set(range(first_low, first_high+1)), set(range(second_low, second_high+1))


INPUT = [line_to_sets(x) for x in read_data().splitlines()]

if __name__ == '__main__':
    print(f"Part one: {len([x for x in INPUT if x[0].issubset(x[1]) or x[1].issubset(x[0])])}")
    print(f"Part two: {len([x for x in INPUT if x[0].intersection(x[1])])}")

