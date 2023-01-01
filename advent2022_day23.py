from collections import Counter
from typing import Set, Dict

from utils import read_data, BaseCoord as Coord, ALL_NEIGHBORS_2D


DIRECTIONS = [
    (Coord(x=0, y=-1), Coord(x=-1, y=-1), Coord(x=1, y=-1)),
    (Coord(x=0, y=1), Coord(x=-1, y=1), Coord(x=1, y=1)),
    (Coord(x=-1, y=0), Coord(x=-1, y=-1), Coord(x=-1, y=1)),
    (Coord(x=1, y=0), Coord(x=1, y=-1), Coord(x=1, y=1))
]


class WanderingElves:
    def __init__(self, raw_input: str):
        self.round: int = 0
        self.elves: Set[Coord] = set()
        for y, line in enumerate(raw_input.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    self.elves.add(Coord(x=x, y=y))

    def run_round(self):
        propositions: Dict[Coord, Coord] = {}
        for elf in self.elves:
            adjacent_elves = {x: elf + x in self.elves for x in ALL_NEIGHBORS_2D}
            # If there are no adjacent elves, stay still
            if not any(adjacent_elves.values()):
                propositions[elf] = elf
                continue
            else:
                for i in range(4):
                    if not any(adjacent_elves[x] for x in DIRECTIONS[(self.round + i) % 4]):
                        propositions[elf] = elf + DIRECTIONS[(self.round + i) % 4][0]
                        break
            if elf not in propositions:
                propositions[elf] = elf

        counts = Counter(propositions.values())
        self.elves = {v if counts[v] == 1 else k for k, v in propositions.items()}
        self.round += 1


    def print_board(self):
        min_x, max_x = min(x.x for x in self.elves), max(x.x for x in self.elves)
        min_y, max_y = min(x.y for x in self.elves), max(x.y for x in self.elves)
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                print("#" if Coord(x=x, y=y) in self.elves else ".", end='')
            print("\n", end='')
        print("-----")

    def get_empty_tiles(self) -> int:
        min_x, max_x = min(x.x for x in self.elves), max(x.x for x in self.elves)
        min_y, max_y = min(x.y for x in self.elves), max(x.y for x in self.elves)
        rect_size = len(range(min_x, max_x+1)) * len(range(min_y, max_y+1))
        return rect_size - len(self.elves)

    def run_until_stopped(self) -> int:
        while True:
            old_board = self.elves.copy()
            self.run_round()
            if old_board == self.elves:
                return self.round


def main():
    elves = WanderingElves(read_data())
    for i in range(10):
        elves.run_round()
    print(f"Part 1: {elves.get_empty_tiles()}")
    elves = WanderingElves(read_data())
    print(f"Part 2: {elves.run_until_stopped()}")


if __name__ == '__main__':
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
