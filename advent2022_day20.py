from utils import read_data
from collections import deque
from typing import Deque, NamedTuple


class Node(NamedTuple):
    index: int
    value: int


class File:
    def __init__(self, raw_input: str, key: int = 1):
        self.numlist: Deque[Node] = deque([Node(i, int(x) * key) for i, x in enumerate(raw_input.splitlines())])

    def decrypt_file(self):
        for i in range(len(self.numlist)):
            index_of_node = [x.index for x in self.numlist].index(i)
            self.numlist.rotate(-index_of_node)
            node = self.numlist.popleft()
            amount_to_rotate = node.value % len(self.numlist)
            self.numlist.rotate(-amount_to_rotate)
            self.numlist.append(node)

    def get_coordinates(self):
        zero_index = [x.value for x in self.numlist].index(0)
        self.numlist.rotate(-zero_index)
        list_len = len(self.numlist)
        return sum(self.numlist[(1000 * (x + 1)) % list_len].value for x in range(3))


def main():
    efile = File(read_data())
    efile.decrypt_file()
    print(f"Part one: {efile.get_coordinates()}")
    efile = File(read_data(), key=811589153)
    for _ in range(10):
        efile.decrypt_file()
    print(f"Part two: {efile.get_coordinates()}")


if __name__ == "__main__":
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
