from utils import read_data, BaseCoord
from typing import NamedTuple, List
import time


class Coord(BaseCoord):
    def normalized(self):
        # Pick the closest compass point (N, NW, W, etc) to a diff coord, going no more than 1 in any direction
        return Coord(
            x=0 if self.x == 0 else self.x // abs(self.x),
            y=0 if self.y == 0 else self.y // abs(self.y)
        )

    def in_range(self) -> bool:
        return max(abs(self.x), abs(self.y)) <= 1

    def catch_up(self, other: 'Coord') -> 'Coord':
        diff = other - self
        return self if diff.in_range() else self + diff.normalized()


def move_knots(knots: List[Coord], direction: str) -> List[Coord]:
    new_knots = [knots[0] + DIRECTIONS[direction]]
    for knot in knots[1:]:
        new_knots.append(knot.catch_up(new_knots[-1]))
    return new_knots


def handle_input(raw_input: str, length: int) -> int:
    knots = [Coord(0, 0)] * length
    tail_locs = {knots[-1]}
    for line in raw_input.splitlines():
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            knots = move_knots(knots, direction)
            tail_locs.add(knots[-1])
    return len(tail_locs)


DIRECTIONS = {
    'U': Coord(x=0, y=-1),
    'R': Coord(x=1, y=0),
    'D': Coord(x=0, y=1),
    'L': Coord(x=-1, y=0)
}


def main():
    print(f"Part one: {handle_input(read_data(), length=2)}")
    print(f"Part two: {handle_input(read_data(), length=10)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic() - start}")
