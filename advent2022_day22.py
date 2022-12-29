from typing import Dict, Tuple, Optional
from utils import read_data, BaseCoord as Coord

NORTH, EAST, SOUTH, WEST = (0, 1, 2, 3)
HEADING_VALUES = (3, 0, 1, 2)
DIR_OFFSETS: Tuple[Coord, ...] = (Coord(x=0, y=-1), Coord(x=1, y=0), Coord(x=0, y=1), Coord(x=-1, y=0))


class Region:
    def __init__(
        self,
        name: int,
        origin: Coord,
        adjacent_regions: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]],
        size: int = 50,
    ):
        self.name = name
        self.origin = origin
        self.size = size
        self.adjacent_regions = adjacent_regions
        self.faces = (
            [Coord(x=self.origin.x + i, y=self.origin.y) for i in range(self.size)],
            [Coord(x=self.origin.x + (self.size - 1), y=self.origin.y + i) for i in range(self.size)],
            [Coord(x=self.origin.x + i, y=self.origin.y + (self.size - 1)) for i in range(self.size)],
            [Coord(x=self.origin.x, y=self.origin.y + i) for i in range(self.size)]
        )
        self.x_range = range(self.origin.x, self.origin.x + self.size)
        self.y_range = range(self.origin.y, self.origin.y + self.size)

    def wrap(self, heading: int, point: Coord) -> Tuple['Region', int, Coord]:
        if point in self:
            return self, heading, point

        if heading == NORTH and point.y == self.origin.y - 1:
            my_slot = point.x - self.origin.x
            new_region, new_side = self.adjacent_regions[NORTH]
        elif heading == SOUTH and point.y == self.origin.y + self.size:
            my_slot = point.x - self.origin.x
            new_region, new_side = self.adjacent_regions[SOUTH]
        elif heading == WEST and point.x == self.origin.x - 1:
            my_slot = point.y - self.origin.y
            new_region, new_side = self.adjacent_regions[WEST]
        elif heading == EAST and point.x == self.origin.x + self.size:
            my_slot = point.y - self.origin.y
            new_region, new_side = self.adjacent_regions[EAST]
        else:
            raise Exception(f"Unknown transition point {point} for region {self.name}")
        # Our new heading is always 180 degrees from the side we're entering
        new_heading = (new_side + 2) % 4
        rotations_needed = (new_heading - heading) % 4
        if rotations_needed == 2:
            # We want to convert slot 0 to slot -1, slot 1 to slot -2, etc
            new_coord = REGIONS[new_region].faces[new_side][-(my_slot + 1)]
        else:
            new_coord = REGIONS[new_region].faces[new_side][my_slot]

        return REGIONS[new_region], new_heading, new_coord

    def __contains__(self, point: Coord):
        return point.x in self.x_range and point.y in self.y_range

    def __repr__(self):
        return f"Region({self.name}, {str(self.origin)})"


REGIONS = [  # id, origin,                         (NORTH   ,   EAST   ,   SOUTH    ,   WEST )
    Region(0, Coord(x=50, y=0), adjacent_regions=((5, WEST), (1, WEST), (2, NORTH), (3, WEST))),
    Region(1, Coord(x=100, y=0), adjacent_regions=((5, SOUTH), (4, EAST), (2, EAST), (0, EAST))),
    Region(2, Coord(x=50, y=50), adjacent_regions=((0, SOUTH), (1, SOUTH), (4, NORTH), (3, NORTH))),
    Region(3, Coord(x=0, y=100), adjacent_regions=((2, WEST), (4, WEST), (5, NORTH), (0, WEST))),
    Region(4, Coord(x=50, y=100), adjacent_regions=((2, SOUTH), (1, EAST), (5, EAST), (3, EAST))),
    Region(5, Coord(x=0, y=150), adjacent_regions=((3, SOUTH), (4, SOUTH), (1, NORTH), (0, NORTH))),
]


class MonkeyMap:
    def __init__(self, raw_input: str):
        lines = raw_input.splitlines()
        raw_path = lines[-1]
        self.path = raw_path.replace("L", " L ").replace("R", " R ").split(" ")
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
        for y in range(min_y, max_y + 1):
            min_for_y: int = min([p.x for p in self.cloud if p.y == y])
            max_for_y: int = max([p.x for p in self.cloud if p.y == y])
            self.hbounds[y] = range(min_for_y, max_for_y + 1)
        for x in range(min_x, max_x + 1):
            min_for_x: int = min([p.y for p in self.cloud if p.x == x])
            max_for_x: int = max([p.y for p in self.cloud if p.x == x])
            self.vbounds[x] = range(min_for_x, max_for_x + 1)
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

    def wrap(self, region: Region, heading: int, coord: Coord, cube=False) -> Tuple[Optional[Region], int, Coord]:
        if cube:
            return region.wrap(heading, coord)
        else:
            new_coord = self.wrap_y(coord) if heading in (NORTH, SOUTH) else self.wrap_x(coord)
            # We don't actually care about the region when we're doing part 1
            return None, heading, new_coord

    def follow_path(self, cube: bool = False) -> int:
        heading = EAST
        region = REGIONS[0]
        loc = region.origin
        for instruction in self.path:
            if instruction == "R":
                heading = (heading + 1) % 4
            elif instruction == "L":
                heading = (heading - 1) % 4
            else:
                for _ in range(int(instruction)):
                    new_region, new_heading, new_loc = self.wrap(region, heading, loc + DIR_OFFSETS[heading], cube)
                    if self.cloud[new_loc] == ".":
                        region, heading, loc = new_region, new_heading, new_loc
                    else:
                        break
        return (1000 * (loc.y + 1)) + (4 * (loc.x + 1)) + HEADING_VALUES[heading]


def main():
    mmap = MonkeyMap(read_data())
    print(f"Part one: {mmap.follow_path()}")
    print(f"Part two: {mmap.follow_path(cube=True)}")


if __name__ == "__main__":
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
