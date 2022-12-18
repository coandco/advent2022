import time
from collections import deque
from typing import Set, Tuple, NamedTuple, Iterator
from typing_extensions import Self

from utils import read_data, BaseCoord3D


class Coord3D(BaseCoord3D):
    def num_sides(self, grid: Set[Self]) -> int:
        return sum(x not in grid for x in self.cardinal_neighbors())

    @staticmethod
    def from_str(input_str: str):
        x, y, z = input_str.split(",")
        return Coord3D(x=int(x), y=int(y), z=int(z))


class Bounds3D(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def expand(self, n: int) -> Self:
        return Bounds3D(self.min_x-n, self.max_x+n, self.min_y-n, self.max_y+n, self.min_z-n, self.max_z+n)

    def all(self) -> Iterator[Coord3D]:
        for x in range(self.min_x, self.max_x+1):
            for y in range(self.min_y, self.max_y+1):
                for z in range(self.min_z, self.max_z+1):
                    yield Coord3D(x=x, y=y, z=z)

    @staticmethod
    def from_grid(grid: Set[Coord3D]) -> 'Bounds3D':
        min_x = min_y = min_z = 99999
        max_x = max_y = max_z = 0
        for point in grid:
            min_x, max_x = min(min_x, point.x), max(max_x, point.x)
            min_y, max_y = min(min_y, point.y), max(max_y, point.y)
            min_z, max_z = min(min_z, point.z), max(max_z, point.z)
        return Bounds3D(min_x, max_x, min_y, max_y, min_z, max_z)

    def __contains__(self, item: Coord3D) -> bool:
        return (
            self.min_x <= item.x <= self.max_x
            and self.min_y <= item.y <= self.max_y
            and self.min_z <= item.z <= self.max_z
        )


def cast(grid: Set[Coord3D]) -> Tuple[Set[Coord3D], Bounds3D]:
    bounds: Bounds3D = Bounds3D.from_grid(grid).expand(1)
    starting_point = Coord3D(x=bounds.min_x, y=bounds.min_y, z=bounds.min_z)
    cast_grid: Set[Coord3D] = set()
    work_queue = deque([starting_point])
    while len(work_queue) > 0:
        point = work_queue.pop()
        cast_grid.add(point)
        work_queue.extend(x for x in point.cardinal_neighbors() if x not in grid and x not in cast_grid and x in bounds)
    return cast_grid, bounds


def invert(cast_grid: Set[Coord3D], bounds: Bounds3D) -> Set[Coord3D]:
    inverted_grid = set()
    for point in bounds.all():
        if point not in cast_grid:
            inverted_grid.add(point)
    return inverted_grid


def main():
    grid = {Coord3D.from_str(x) for x in read_data().splitlines()}
    print(f"Part one: {sum(x.num_sides(grid) for x in grid)}")
    cast_grid, bounds = cast(grid)
    external_grid = invert(cast_grid, bounds)
    print(f"Part two: {sum(x.num_sides(external_grid) for x in external_grid)}")


if __name__ == "__main__":
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
