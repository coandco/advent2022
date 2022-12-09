from utils import read_data
from typing import NamedTuple


def sign(x: int) -> int:
    return -1 if x < 0 else 1


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord(x=self.x-other.x, y=self.y-other.y)

    def catch_up(self, head: 'Coord') -> 'Coord':
        diff = head - self
        if max(abs(diff.x), abs(diff.y)) <= 1:
            return self
        elif min(abs(diff.x), abs(diff.y)) == 0 or diff.x == diff.y:
            return self + Coord(x=diff.x//2, y=diff.y//2)
        else:
            return self + Coord(x=sign(diff.x), y=sign(diff.y))


DIRECTIONS = {
    'U': Coord(x=0, y=-1),
    'R': Coord(x=1, y=0),
    'D': Coord(x=0, y=1),
    'L': Coord(x=-1, y=0)
}

INPUT = read_data().splitlines()

if __name__ == '__main__':
    head = tail = Coord(0, 0)
    tail_locs = {tail}
    for line in INPUT:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            head = head + DIRECTIONS[direction]
            tail = tail.catch_up(head)
            tail_locs.add(tail)
    print(f"Part one: {len(tail_locs)}")
    knots = [Coord(0, 0)] * 10
    tail_locs = {knots[-1]}
    for line in INPUT:
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            knots[0] = knots[0] + DIRECTIONS[direction]
            for i in range(1, 10):
                knots[i] = knots[i].catch_up(knots[i-1])
            tail_locs.add(knots[-1])
    print(f"Part two: {len(tail_locs)}")

