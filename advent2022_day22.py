from typing import Set, Dict
from itertools import zip_longest, chain
from utils import read_data, BaseCoord as Coord
import re

DIGITS = re.compile(r"\d+")
TURN_LETTERS = re.compile(r"[LR]")


DIRECTIONS = {
    'N': Coord(x=0, y=-1),
    'E': Coord(x=1, y=0),
    'S': Coord(x=0, y=1),
    'W': Coord(x=-1, y=0)
}


TURNS = {
    'L': {
        'N': 'W',
        'E': 'N',
        'S': 'E',
        'W': 'S'
    },
    'R': {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N'
    }
}

HEADING_VALUES = {
    'N': 3,
    'E': 0,
    'S': 1,
    'W': 2
}


class MonkeyMap:
    def __init__(self, raw_input: str):
        lines = raw_input.splitlines()
        raw_path = lines[-1]
        self.path = [
            x
            for x in chain(*zip_longest(DIGITS.findall(raw_path), TURN_LETTERS.findall(raw_path)))
            if x is not None
        ]
        lines = lines[:-2]
        self.cloud: Dict[Coord, str] = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in (".", "#"):
                    self.cloud[Coord(x=x, y=y)] = char

        self.hbounds: Dict[int, range] = {}
        self.vbounds: Dict[int, range] = {}
        min_x, max_x = min(x.x for x in self.cloud), max(x.x for x in self.cloud)
        min_y, max_y = min(x.y for x in self.cloud), max(x.y for x in self.cloud)
        for y in range(min_y, max_y+1):
            min_for_y: int = min([p.x for p in self.cloud if p.y == y])
            max_for_y: int = max([p.x for p in self.cloud if p.y == y])
            self.hbounds[y] = range(min_for_y, max_for_y+1)
        for x in range(min_x, max_x+1):
            min_for_x: int = min([p.y for p in self.cloud if p.x == x])
            max_for_x: int = max([p.y for p in self.cloud if p.x == x])
            self.vbounds[x] = range(min_for_x, max_for_x+1)
        # Extend the bounds out one in each direction to support wrapping
        self.hbounds[min_y - 1] = self.hbounds[min_y]
        self.hbounds[max_y + 1] = self.hbounds[max_y]
        self.vbounds[min_x - 1] = self.vbounds[min_x]
        self.vbounds[max_x + 1] = self.vbounds[max_x]

    def in_bounds(self, coord: Coord) -> bool:
        return coord.x in self.hbounds[coord.y] and coord.y in self.vbounds[coord.x]

    def wrap_x(self, coord: Coord) -> Coord:
        new_x = ((coord.x - self.hbounds[coord.y].start) % len(self.hbounds[coord.y])) + self.hbounds[coord.y].start
        return Coord(x=new_x, y=coord.y)

    def wrap_y(self, coord: Coord) -> Coord:
        new_y = ((coord.y - self.vbounds[coord.x].start) % len(self.vbounds[coord.x])) + self.vbounds[coord.x].start
        return Coord(x=coord.x, y=new_y)

    def wrap(self, heading: str, coord: Coord):
        if heading in ('E', 'W'):
            return self.wrap_x(coord)
        elif heading in ('N', 'S'):
            return self.wrap_y(coord)
        raise NotImplementedError(f"Unknown heading {heading}")

    def follow_path(self) -> int:
        heading = 'E'
        loc = Coord(x=self.hbounds[0].start, y=0)
        for instruction in self.path:
            if instruction in ('L', 'R'):
                heading = TURNS[instruction][heading]
            else:
                for _ in range(int(instruction)):
                    new_coord = self.wrap(heading, loc + DIRECTIONS[heading])
                    if self.cloud[new_coord] == ".":
                        loc = new_coord
                    else:
                        break
        return (1000*(loc.y+1)) + (4*(loc.x+1)) + HEADING_VALUES[heading]


TEST = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def main():
    mmap = MonkeyMap(read_data())
    print(f"Part one: {mmap.follow_path()}")


if __name__ == "__main__":
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
