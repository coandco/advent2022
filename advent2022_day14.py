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
        self.start_cache = [start]
        self.min_x, self.max_x = min(point.x for point in self.walls) - 1, max(point.x for point in self.walls) + 1
        # We want our min_y to include the start
        self.min_y, self.max_y = self.start.y, max(point.y for point in self.walls)

    def add_sand_grain(self, floor: bool = False) -> Optional[Coord]:
        # If we're full of sand up to the start, no more can be added
        if self.start in self.occlusion:
            return None
        current_point = self.start_cache[-1]
        while current_point.y <= self.max_y:
            new_point = current_point + Coord(x=0, y=1)
            if new_point not in self.occlusion:
                self.start_cache.append(new_point)
                current_point = new_point
                continue
            new_point = current_point + Coord(x=-1, y=1)
            if new_point not in self.occlusion:
                self.start_cache.append(new_point)
                current_point = new_point
                continue
            new_point = current_point + Coord(x=1, y=1)
            if new_point not in self.occlusion:
                self.start_cache.append(new_point)
                current_point = new_point
                continue
            # If we've reached this point, the sand is blocked and we need to add it to our maps
            return current_point
        # If we've reached this point, we're either at the floor or are falling off the bottom
        if floor:
            return current_point
        else:
            return None

    def run_sim(self, floor: bool = False) -> int:
        self.walls = self.original_walls.copy()
        self.sand = set()
        self.occlusion = self.walls.copy()
        self.start_cache = [self.start]
        while new_grain := self.add_sand_grain(floor=floor):
            self.start_cache.pop()
            self.sand.add(new_grain)
            self.occlusion.add(new_grain)
        return len(self.sand)


def main():
    sand_sim = SandSim(parse_data(read_data().splitlines()))
    print(f"Part one: {sand_sim.run_sim()}")
    print(f"Part two: {sand_sim.run_sim(floor=True)}")


if __name__ == '__main__':
    main()
