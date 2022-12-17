import time
from typing import Iterator, NamedTuple, Set, Tuple, Optional, Type, Dict, List
from typing_extensions import Self

from utils import read_data, BaseCoord as Coord


JET_DIRECTIONS = {"<": Coord(x=-1, y=0), ">": Coord(x=1, y=0)}


class BaseShape(NamedTuple):
    origin: Coord

    def points(self) -> Iterator[Coord]:
        raise NotImplementedError()

    def next_shape(self) -> Type["BaseShape"]:
        raise NotImplementedError()

    def move(self, offset: Coord) -> Self:
        return self.__class__(origin=self.origin + offset)

    @staticmethod
    def _height() -> int:
        return 1

    @classmethod
    def spawn_new(cls, board_height: int) -> 'BaseShape':
        return cls(origin=Coord(x=2, y=board_height-3-cls._height()))


class HorizontalLine(BaseShape):
    def points(self) -> Iterator[Coord]:
        for x in range(4):
            yield self.origin + Coord(x=x, y=0)

    def next_shape(self) -> Type[BaseShape]:
        return Plus


class Plus(BaseShape):
    def points(self) -> Iterator[Coord]:
        yield self.origin + Coord(x=1, y=0)
        for x in range(3):
            yield self.origin + Coord(x=x, y=1)
        yield self.origin + Coord(x=1, y=2)

    def next_shape(self) -> Type[BaseShape]:
        return BackwardsL

    @staticmethod
    def _height() -> int:
        return 3


class BackwardsL(BaseShape):
    def points(self) -> Iterator[Coord]:
        yield self.origin + Coord(x=2, y=0)
        yield self.origin + Coord(x=2, y=1)
        for x in range(3):
            yield self.origin + Coord(x=x, y=2)

    def next_shape(self) -> Type["BaseShape"]:
        return VerticalLine

    @staticmethod
    def _height() -> int:
        return 3


class VerticalLine(BaseShape):
    def points(self) -> Iterator[Coord]:
        for y in range(4):
            yield self.origin + Coord(x=0, y=y)

    def next_shape(self) -> Type["BaseShape"]:
        return Square

    @staticmethod
    def _height() -> int:
        return 4


class Square(BaseShape):
    def points(self) -> Iterator[Coord]:
        for x in range(2):
            for y in range(2):
                yield self.origin + Coord(x=x, y=y)

    def next_shape(self) -> Type["BaseShape"]:
        return HorizontalLine

    @staticmethod
    def _height() -> int:
        return 2


def jets(input_str: str) -> Iterator[Coord]:
    while True:
        yield from (JET_DIRECTIONS[x] for x in input_str)


def shapes() -> Iterator[Type[BaseShape]]:
    while True:
        yield from [HorizontalLine, Plus, BackwardsL, VerticalLine, Square]


def drop_shape(
    board: Set[Coord], board_height: int, shape: Type[BaseShape], jet_directions: Iterator[Coord]
) -> Tuple[Set[Coord], int]:
    # Create the shape
    active_shape = shape.spawn_new(board_height)
    while True:
        # Apply the jet
        next_dir = next(jet_directions)
        moved_shape = active_shape.move(next_dir)
        if all(x.x in range(7) and x not in board for x in moved_shape.points()):
            active_shape = moved_shape

        # Attempt to move down
        moved_shape = active_shape.move(Coord(x=0, y=1))
        if any(x.y >= 0 or x in board for x in moved_shape.points()):
            board.update(active_shape.points())
            new_height = min(active_shape.origin.y, board_height)
            return board, new_height
        else:
            active_shape = moved_shape


def print_board(board: Set[Coord], board_height: int, active_shape: Optional[BaseShape] = None):
    active_set = set(active_shape.points()) if active_shape else set()
    for y in range(board_height, 1):
        for x in range(7):
            current = Coord(x=x, y=y)
            print("#" if current in board or current in active_set else ".", end='')
        print("\n", end='')
    print("-------")


def find_cycle(raw_jets: str) -> Tuple[List[int], int, int]:
    board = set()
    board_height = 0
    jet_iter = jets(raw_jets)
    shapes_iter = shapes()
    diffs: List[int] = []
    seen_diffsets: Dict[Tuple[int], Tuple[int, int]] = {}
    for i in range(1, 1000000000001):
        old_height = board_height
        board, board_height = drop_shape(board, board_height, next(shapes_iter), jet_iter)
        diffs.append(abs(board_height - old_height))
        # Arbitrarily picked 25 as the length of diffs to use to find the cycle after 20 was too short
        diffset = tuple(diffs[-25:])
        if diffset in seen_diffsets:
            offset, offset_height = seen_diffsets[diffset]
            return list(diffs)[offset-i:], offset, offset_height
        else:
            seen_diffsets[diffset] = (i, abs(board_height))


def run_sim_to_i(i: int, cycle: List[int], offset: int, offset_height: int) -> int:
    assert i > offset
    num_cycles = (i - offset) // len(cycle)
    leftover = (i - offset) % len(cycle)
    return offset_height + (num_cycles * sum(cycle)) + sum(cycle[:leftover])


def main():
    cycle, offset, offset_height = find_cycle(read_data())
    print(f"Part one: {run_sim_to_i(2022, cycle, offset, offset_height)}")
    print(f"Part two: {run_sim_to_i(1000000000000, cycle, offset, offset_height)}")


if __name__ == '__main__':
    start = time.monotonic()
    main()
    print(f"Time: {time.monotonic()-start}")
