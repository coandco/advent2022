from utils import read_data
from more_itertools import windowed
from collections import Counter


def find_marker(signal: str, window_size: int = 4) -> int:
    for i, window in enumerate(windowed(signal, window_size)):
        # Get the most common letter (element 0) and check its count (name, count)
        if Counter(window).most_common()[0][1] == 1:
            return i + window_size
    raise Exception("Marker not found!")


def main():
    print(f"Part one: {find_marker(read_data(), 4)}")
    print(f"Part two: {find_marker(read_data(), 14)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
