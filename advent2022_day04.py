from typing import Tuple, Set
from utils import read_data
import re

DIGITS = re.compile(r'\d+')


def line_to_ranges(line: str) -> Tuple[range, range]:
    first_low, first_high, second_low, second_high = (int(x) for x in DIGITS.findall(line))
    return range(first_low, first_high+1), range(second_low, second_high+1)


def ranges_are_subsets(range1: range, range2: range) -> bool:
    # If the start/end of either range is contained in the other, one's a subset of the other
    return (range1.start in range2 and range1[-1] in range2) or (range2.start in range1 and range2[-1] in range1)


def ranges_overlap(range1: range, range2: range) -> bool:
    # Try to construct a range with the greater of the two starts and the lesser of the two ends
    # If they don't overlap, the range will end up empty (and thus evaluate to False)
    return bool(range(max(range1.start, range2.start), min(range1[-1], range2[-1])+1))


# INPUT = [line_to_sets(x) for x in read_data().splitlines()]


def main():
    INPUT = [line_to_ranges(x) for x in read_data().splitlines()]
    print(f"Part one: {len([x for x in INPUT if ranges_are_subsets(*x)])}")
    print(f"Part two: {len([x for x in INPUT if ranges_overlap(*x)])}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")


