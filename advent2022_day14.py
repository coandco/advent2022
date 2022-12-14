from typing import List, Set, Iterator, Optional
from more_itertools import windowed

from utils import read_data, Coord as CoordBase


class Coord(CoordBase):
    y: int
    x: int

    def line(self, other: 'Coord') -> Iterator['Coord']:
        if self.x == other.x:
            for y in range(min(self.y, other.y), max(self.y, other.y)+1):
                yield Coord(x=self.x, y=y)
        elif self.y == other.y:
            for x in range(min(self.x, other.x), max(self.x, other.x)+1):
                yield Coord(x=x, y=self.y)
        else:
            raise Exception("Can only draw a line if x or y are equal")

    @staticmethod
    def from_string(raw_string: str) -> 'Coord':
        raw_x, raw_y = raw_string.split(",", maxsplit=1)
        return Coord(x=int(raw_x), y=int(raw_y))


def parse_data(lines: List[str]) -> Set[Coord]:
    walls = set()
    # Filter out empty lines
    for line in (x for x in lines if x):
        for first, second in windowed(line.split(" -> "), n=2):
            walls.update(Coord.from_string(first).line(Coord.from_string(second)))
    return walls


class FullException(Exception):
    pass


class SandSim:
    def __init__(self, walls: Set[Coord], start: Coord = Coord(x=500, y=0)):
        self.original_walls = walls.copy()
        self.walls = walls.copy()
        self.sand = set()
        self.occlusion = walls.copy()
        self.start = start
        self.min_x, self.max_x = min(point.x for point in self.walls) - 1, max(point.x for point in self.walls) + 1
        # We want our min_y to include the start
        self.min_y, self.max_y = self.start.y, max(point.y for point in self.walls)

    def add_sand_grain(self, floor: bool = False) -> Optional[Coord]:
        # If we're full of sand up to the start, no more can be added
        if self.start in self.occlusion:
            return None
        current_point = self.start
        while current_point.y <= self.max_y:
            new_point = current_point + Coord(x=0, y=1)
            if new_point not in self.occlusion:
                current_point = new_point
                continue
            new_point = current_point + Coord(x=-1, y=1)
            if new_point not in self.occlusion:
                current_point = new_point
                continue
            new_point = current_point + Coord(x=1, y=1)
            if new_point not in self.occlusion:
                current_point = new_point
                continue
            # If we've reached this point, the sand is blocked and we need to add it to our maps
            return current_point
        # If we've reached this point, we're either at the floor or are falling off the bottom
        return current_point if floor else None

    def run_sim(self, floor: bool = False) -> int:
        self.walls = self.original_walls.copy()
        self.sand = set()
        self.occlusion = self.walls.copy()
        while new_grain := self.add_sand_grain(floor=floor):
            self.sand.add(new_grain)
            self.occlusion.add(new_grain)
        return len(self.sand)

    def print_state(self, floor: bool = False):
        min_x, max_x = self.min_x, self.max_x
        min_y, max_y = self.min_y, self.max_y
        if floor:
            min_x, max_x = min(point.x for point in self.sand), max(point.x for point in self.sand)
            min_y, max_y = 0, self.max_y+1
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                point = Coord(x=x, y=y)
                char = " "
                if point == self.start:
                    char = "+"
                elif point in self.walls:
                    char = "#"
                elif point in self.sand:
                    char = "o"
                print(char, end='')
            print("\n", end='')


def main():
    sand_sim = SandSim(parse_data(read_data().splitlines()))
    print(f"Part one: {sand_sim.run_sim()}")
    sand_sim.print_state()
    print(f"Part two: {sand_sim.run_sim(floor=True)}")
    sand_sim.print_state(floor=True)


if __name__ == '__main__':
    main()