from utils import read_data
from more_itertools import windowed
from collections import Counter

INPUT = read_data()


def find_marker(signal: str, window_size: int = 4) -> int:
    for i, window in enumerate(windowed(signal, window_size)):
        # Get the most common letter (element 0) and check its count (name, count)
        if Counter(window).most_common()[0][1] == 1:
            return i + window_size
    raise Exception("Marker not found!")


print(f"Part one: {find_marker(INPUT, 4)}")
print(f"Part two: {find_marker(INPUT, 14)}")
