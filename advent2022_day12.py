from collections import deque, defaultdict
from typing import Tuple, Deque, DefaultDict, Optional, Iterable, List
from utils import read_data, BaseCoord as Coord


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
        self.valid_dirs = {x: self.valid_directions(x) for x in self.points}
        self.heatmap = self.generate_heatmap(self.end)

    def valid_directions(self, point: Coord) -> Tuple[Coord]:
        neighbors = (x for x in point.cardinal_neighbors() if x in self.points)
        return tuple(x for x in neighbors if self.points[x] >= (self.points[point] - 1))

    def generate_heatmap(self, start_coord: Coord) -> DefaultDict[Coord, int]:
        heatmap: DefaultDict[Coord, int] = defaultdict(lambda: 99999)
        to_evaluate: Deque[Tuple[Coord, int]] = deque([(start_coord, 0)])
        while len(to_evaluate) > 0:
            loc, score = to_evaluate.popleft()
            if score < heatmap[loc]:
                heatmap[loc] = score
                to_evaluate.extend((x, score + 1) for x in self.valid_dirs[loc])
        return heatmap

    def all_of_height(self, height: str) -> Iterable:
        return (k for k, v in self.points.items() if v == ord(height))


def main(input_str: str):
    hmap = Heightmap(input_str)
    print(f"Part one: {hmap.heatmap[hmap.start]}")
    print(f"Part two: {min(hmap.heatmap[x] for x in hmap.all_of_height('a'))}")


if __name__ == "__main__":
    main(read_data())
