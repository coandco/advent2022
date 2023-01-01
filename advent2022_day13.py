from typing import List, Union
from utils import read_data
from itertools import zip_longest
from more_itertools import chunked
import json


class Packet:
    def __init__(self, packet: Union[List, int]):
        self.packet = packet

    def __lt__(self, other: 'Packet') -> bool:
        return self.cmp(other) == -1

    def __eq__(self, other: 'Packet') -> bool:
        return self.cmp(other) == 0

    def cmp(self, other: 'Packet') -> int:
        if isinstance(self.packet, int) and isinstance(other.packet, int):
            return (self.packet > other.packet) - (self.packet < other.packet)
        if isinstance(self.packet, list) and isinstance(other.packet, list):
            for sub_first, sub_second in zip_longest(self.packet, other.packet, fillvalue=None):
                if sub_first is None:
                    return -1
                if sub_second is None:
                    return 1
                comparison = Packet(sub_first).cmp(Packet(sub_second))
                if comparison == 0:
                    continue
                return comparison
            return 0
        if isinstance(self.packet, list) and isinstance(other.packet, int):
            return self.cmp(Packet([other.packet]))
        if isinstance(self.packet, int) and isinstance(other.packet, list):
            return Packet([self.packet]).cmp(other)
        raise Exception("Shouldn't reach this")


def main():
    INPUT = [Packet(json.loads(x)) for x in read_data().splitlines() if x]
    print(f"Part one: {sum(i + 1 for i, x in enumerate(chunked(INPUT, 2)) if x[0] < x[1])}")
    part_two_data = sorted(INPUT + [Packet([[2]])] + [Packet([[6]])])
    print(f"Part two: {(part_two_data.index(Packet([[2]])) + 1) * (part_two_data.index(Packet([[6]])) + 1)}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")





