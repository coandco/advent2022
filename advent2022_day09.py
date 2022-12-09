from utils import read_data
from typing import NamedTuple, List


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x-other.x, y=self.y-other.y)

    def normalized(self):
        return Coord(
            x=0 if self.x == 0 else self.x // abs(self.x),
            y=0 if self.y == 0 else self.y // abs(self.y)
        )

    def in_range(self) -> bool:
        return max(abs(self.x), abs(self.y)) <= 1

    def catch_up(self, head: 'Coord') -> 'Coord':
        diff = head - self
        return self if diff.in_range() else self + diff.normalized()


def move_knots(knots: List[Coord], direction: str) -> List[Coord]:
    new_knots = [knots[0] + DIRECTIONS[direction]]
    for knot in knots[1:]:
        new_knots.append(knot.catch_up(new_knots[-1]))
    return new_knots


DIRECTIONS = {
    'U': Coord(x=0, y=-1),
    'R': Coord(x=1, y=0),
    'D': Coord(x=0, y=1),
    'L': Coord(x=-1, y=0)
}

INPUT = read_data().splitlines()

if __name__ == '__main__':
    knots = [Coord(0, 0)] * 2
    tail_locs = set()
    for line in INPUT:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            knots = move_knots(knots, direction)
            tail_locs.add(knots[-1])
    print(f"Part one: {len(tail_locs)}")
    knots = [Coord(0, 0)] * 10
    tail_locs = {knots[-1]}
    for line in INPUT:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            knots = move_knots(knots, direction)
            tail_locs.add(knots[-1])
    print(f"Part two: {len(tail_locs)}")

