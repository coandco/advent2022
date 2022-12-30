from collections import defaultdict, deque
from typing import Set, DefaultDict, Deque, Tuple
from math import lcm

from utils import read_data, BaseCoord as Coord


class Blizzards:
    def __init__(self, raw_input: str):
        self.walls: Set[Coord] = set()
        self.upward: DefaultDict[int, Set[int]] = defaultdict(set)
        self.rightward: DefaultDict[int, Set[int]] = defaultdict(set)
        self.downward: DefaultDict[int, Set[int]] = defaultdict(set)
        self.leftward: DefaultDict[int, Set[int]] = defaultdict(set)
        for y, line in enumerate(raw_input.splitlines(), start=-1):
            for x, char in enumerate(line, start=-1):
                if char == "#":
                    self.walls.add(Coord(x=x, y=y))
                elif char == ">":
                    self.rightward[y].add(x)
                elif char == "<":
                    self.leftward[y].add(x)
                elif char == "^":
                    self.upward[x].add(y)
                elif char == "v":
                    self.downward[x].add(y)
        self.min_x, self.max_x = min(x.x for x in self.walls), max(x.x for x in self.walls)
        self.min_y, self.max_y = min(x.y for x in self.walls), max(x.y for x in self.walls)
        self.width = self.max_x
        self.height = self.max_y
        # Seal in the start and end, so we don't try going past them
        self.walls.update(Coord(x=x, y=-2) for x in range(-1, 3))
        self.walls.update(Coord(x=x, y=self.max_y+1) for x in range(self.max_x-2, self.max_x+1))

    def occupied(self, coord: Coord, depth: int = 0):
        left_offset, right_offset = (coord.x + depth) % self.width, (coord.x - depth) % self.width
        up_offset, down_offset = (coord.y + depth) % self.height, (coord.y - depth) % self.height
        return (
            left_offset in self.leftward[coord.y]
            or right_offset in self.rightward[coord.y]
            or up_offset in self.upward[coord.x]
            or down_offset in self.downward[coord.x]
        )

    def pathfind(self, starting_depth: int = 0, reverse: bool = False) -> int:
        start_loc: Coord = Coord(x=0, y=-1)
        end_loc: Coord = Coord(x=self.max_x - 1, y=self.max_y)
        if reverse:
            start_loc, end_loc = end_loc, start_loc
        work_queue: Deque[Tuple[Coord, int]] = deque([(start_loc, starting_depth)])
        min_time: int = 99999
        seen_states: Set[Tuple[Coord, int]] = set()
        repeat = lcm(self.width, self.height)
        while len(work_queue) > 0:
            loc, depth = work_queue.popleft()
            if loc == end_loc:
                min_time = min(depth, min_time)
                continue
            if depth > min_time:
                continue
            if (loc, depth % repeat) not in seen_states:
                seen_states.add((loc, depth % repeat))
                work_queue.extend(
                    (x, depth + 1)
                    for x in loc.cardinal_neighbors()
                    if x not in self.walls and not self.occupied(x, depth + 1)
                )
                if loc not in self.walls and not self.occupied(loc, depth + 1):
                    work_queue.append((loc, depth+1))
        return min_time


def main():
    blizzards = Blizzards(read_data())
    there_time = blizzards.pathfind()
    print(f"Part one: {there_time}")
    back_time = blizzards.pathfind(there_time, reverse=True)
    there_again_time = blizzards.pathfind(back_time)
    print(f"Part two: {there_again_time}")


if __name__ == "__main__":
    import time
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
