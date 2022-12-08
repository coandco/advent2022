from utils import read_data
from typing import NamedTuple, List
from math import prod


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Coord'):
        return Coord(x=self.x+other.x, y=self.y+other.y)


DIRECTIONS = (Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1))


class Forest:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.bounds = Bounds(min_x=0, max_x=len(grid[0])-1, min_y=0, max_y=len(grid)-1)

    def tree_is_visible_from_direction(self, coord: Coord, step: Coord) -> bool:
        tree_height = self.grid[coord.y][coord.x]
        return all(self.grid[c.y][c.x] < tree_height for c in self.bounds.coords_to_edge(coord, step))

    def tree_is_visible(self, coord: Coord) -> bool:
        return any(self.tree_is_visible_from_direction(coord, step) for step in DIRECTIONS)

    def count_visible_trees(self) -> int:
        return len([x for x in self.bounds.all_coords() if self.tree_is_visible(x)])

    def viewing_distance_in_direction(self, coord: Coord, step: Coord) -> int:
        trees_visible = 0
        my_height = self.grid[coord.y][coord.x]
        for to_check in self.bounds.coords_to_edge(coord, step):
            trees_visible += 1
            if self.grid[to_check.y][to_check.x] >= my_height:
                break
        return trees_visible

    def viewing_score(self, coord: Coord):
        return prod(self.viewing_distance_in_direction(coord, x) for x in DIRECTIONS)

    def best_viewing_score(self):
        return max(self.viewing_score(x) for x in self.bounds.all_coords())


class Bounds(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def all_coords(self):
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                yield Coord(x=x, y=y)

    def coords_to_edge(self, start: Coord, step: Coord):
        current_coord = start + step
        while current_coord in self:
            yield current_coord
            current_coord = current_coord + step

    def __contains__(self, item: Coord):
        return (self.min_x <= item.x <= self.max_x) and (self.min_y <= item.y <= self.max_y)


INPUT = [[int(x) for x in y] for y in read_data().splitlines()]

if __name__ == '__main__':
    trees = Forest(INPUT)
    print(f"Part one: {trees.count_visible_trees()}")
    print(f"Part two: {trees.best_viewing_score()}")

