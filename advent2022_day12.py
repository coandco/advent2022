from collections import deque, defaultdict
from typing import NamedTuple, Tuple, Deque, DefaultDict, Optional, Iterable, Set, List
from utils import read_data


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(x=self.x + other.x, y=self.y + other.y)


DIRECTIONS = (Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0))


class Heightmap:
    def __init__(self, raw: str):
        self.points = {}
        self.start = None
        self.end = None
        for y, line in enumerate(raw.splitlines()):
            for x, char in enumerate(line):
                if char == "S":
                    self.start = Coord(x=x, y=y)
                    self.points[self.start] = ord("a")
                elif char == "E":
                    self.end = Coord(x=x, y=y)
                    self.points[self.end] = ord("z")
                else:
                    self.points[Coord(x=x, y=y)] = ord(char)
        self.max_x = max(x.x for x in self.points)
        self.max_y = max(x.y for x in self.points)
        self.valid_dirs = {x: self.valid_directions(x) for x in self.points}
        self.reversed_valid_dirs: DefaultDict[Coord, Set[Coord]] = defaultdict(set)
        for k, v in self.valid_dirs.items():
            for point in v:
                self.reversed_valid_dirs[point].add(k)
        self.reversed_heatmap = self.generate_heatmap(self.end)

    def in_bounds(self, point: Coord):
        return (0 <= point.x <= self.max_x) and (0 <= point.y <= self.max_y)

    def valid_directions(self, point: Coord) -> Tuple[Coord]:
        return tuple(
            new_loc
            for x in DIRECTIONS
            if self.in_bounds(new_loc := point + x) and self.points[new_loc] <= self.points[point] + 1
        )

    def generate_heatmap(self, start_coord: Coord) -> DefaultDict[Coord, int]:
        heatmap: DefaultDict[Coord, int] = defaultdict(lambda: 99999)
        to_evaluate: Deque[Tuple[Coord, int]] = deque([(start_coord, 0)])
        while len(to_evaluate) > 0:
            loc, score = to_evaluate.popleft()
            if score < heatmap[loc]:
                heatmap[loc] = score
                to_evaluate.extend((x, score + 1) for x in self.reversed_valid_dirs[loc])
        return heatmap

    def get_shortest_paths(self, start_coords: Optional[Iterable] = None) -> List[int]:
        if not start_coords:
            start_coords = [self.start]
        return [self.reversed_heatmap[x] for x in start_coords]

    def all_of_height(self, height: str) -> Iterable:
        return (k for k, v in self.points.items() if v == ord(height))


def main(input_str: str):
    hmap = Heightmap(input_str)
    print(f"Part one: {hmap.get_shortest_paths()[0]}")
    print(f"Part two: {min(hmap.get_shortest_paths(hmap.all_of_height('a')))}")


if __name__ == "__main__":
    main(read_data())
