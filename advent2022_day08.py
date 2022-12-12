from utils import read_data, Coord, CARDINAL_NEIGHBORS_2D
from typing import Dict
from math import prod


class Forest:
    def __init__(self, grid: Dict[Coord, int]):
        self.grid = grid

    def coords_to_edge(self, start: Coord, step: Coord):
        current_coord = start + step
        while current_coord in self.grid:
            yield current_coord
            current_coord = current_coord + step

    def tree_is_visible_from_direction(self, coord: Coord, step: Coord) -> bool:
        tree_height = self.grid[coord]
        return all(self.grid[c] < tree_height for c in self.coords_to_edge(coord, step))

    def tree_is_visible(self, coord: Coord) -> bool:
        return any(self.tree_is_visible_from_direction(coord, step) for step in CARDINAL_NEIGHBORS_2D)

    def count_visible_trees(self) -> int:
        return sum(self.tree_is_visible(x) for x in self.grid)

    def viewing_distance_in_direction(self, coord: Coord, step: Coord) -> int:
        trees_visible = 0
        my_height = self.grid[coord]
        for trees_visible, to_check in enumerate(self.coords_to_edge(coord, step), start=1):
            if self.grid[to_check] >= my_height:
                break
        return trees_visible

    def viewing_score(self, coord: Coord):
        return prod(self.viewing_distance_in_direction(coord, x) for x in CARDINAL_NEIGHBORS_2D)

    def best_viewing_score(self):
        return max(self.viewing_score(x) for x in self.grid)


def parse_input(raw_input: str) -> Dict[Coord, int]:
    tree_cloud = {}
    for y, line in enumerate(raw_input.splitlines()):
        for x, height in enumerate(line):
            tree_cloud[Coord(x=x, y=y)] = int(height)
    return tree_cloud


if __name__ == '__main__':
    trees = Forest(parse_input(read_data()))
    print(f"Part one: {trees.count_visible_trees()}")
    print(f"Part two: {trees.best_viewing_score()}")
